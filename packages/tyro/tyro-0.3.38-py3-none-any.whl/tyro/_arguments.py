"""Rules for taking high-level field definitions and lowering them into inputs for
argparse's `add_argument()`."""
from __future__ import annotations

import argparse
import dataclasses
import enum
import functools
import itertools
import shlex
from typing import Any, Dict, Mapping, Optional, Sequence, Set, Tuple, TypeVar, Union

import rich.markup
import shtab

from . import _fields, _instantiators, _resolver, _strings
from ._typing import TypeForm
from .conf import _markers

try:
    # Python >=3.8.
    from functools import cached_property
except ImportError:
    # Python 3.7.
    from backports.cached_property import cached_property  # type: ignore


@dataclasses.dataclass(frozen=True)
class ArgumentDefinition:
    """Structure containing everything needed to define an argument."""

    dest_prefix: str  # True prefix. (eg for the argument's dest field)
    name_prefix: str  # User-facing prefix.
    subcommand_prefix: str  # Prefix for nesting.
    field: _fields.FieldDefinition
    type_from_typevar: Dict[TypeVar, TypeForm[Any]]

    def add_argument(
        self, parser: Union[argparse.ArgumentParser, argparse._ArgumentGroup]
    ) -> None:
        """Add a defined argument to a parser."""

        # Get keyword arguments, with None values removed.
        kwargs = dataclasses.asdict(self.lowered)
        kwargs.pop("instantiator")
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        name_or_flag = kwargs.pop("name_or_flag")
        if len(name_or_flag) == 0:
            name_or_flag = _strings.dummy_field_name

        # We're actually going to skip the default field: if an argument is unset, the
        # MISSING value will be detected in _calling.py and the field default will
        # directly be used. This helps reduce the likelihood of issues with converting
        # the field default to a string format, then back to the desired type.
        kwargs["default"] = _fields.MISSING_NONPROP

        # Apply overrides in our arg configuration object.
        # Note that the `name` field is applied when the field object is instantiated!
        if self.field.argconf.metavar is not None:
            kwargs["metavar"] = self.field.argconf.metavar

        # Add argument! Note that the name must be passed in as a position argument.
        arg = parser.add_argument(name_or_flag, **kwargs)

        # Do our best to tab complete paths.
        # There will be false positives here, but if choices is unset they should be
        # harmless.
        if "choices" not in kwargs:
            name_suggests_dir = (
                # The conditions are intended to be conservative; if a directory path is
                # registered as a normal file one that's OK, the reverse on the other
                # hand will be overly restrictive.
                self.field.name.endswith("_dir")
                or self.field.name.endswith("_directory")
                or self.field.name.endswith("_folder")
            )
            name_suggests_path = (
                self.field.name.endswith("_file")
                or self.field.name.endswith("_path")
                or self.field.name.endswith("_filename")
                or name_suggests_dir
            )
            complete_as_path = (
                # Catch types like Path, List[Path], Tuple[Path, ...] etc.
                "Path" in str(self.field.typ)
                # For string types, we require more evidence.
                or ("str" in str(self.field.typ) and name_suggests_path)
            )
            if complete_as_path:
                arg.complete = shtab.DIRECTORY if name_suggests_dir else shtab.FILE  # type: ignore

    @cached_property
    def lowered(self) -> LoweredArgumentDefinition:
        """Lowered argument definition, generated by applying a sequence of rules."""
        rules = (
            _rule_handle_defaults,
            _rule_handle_boolean_flags,
            _rule_recursive_instantiator_from_type,
            _rule_convert_defaults_to_strings,
            _rule_generate_helptext,
            _rule_set_name_or_flag_and_dest,
            _rule_positional_special_handling,
            _rule_static_cast_choices_to_patched_list,
        )
        return functools.reduce(
            lambda lowered, rule: rule(self, lowered),
            rules,
            LoweredArgumentDefinition(),
        )


@dataclasses.dataclass(frozen=True)
class LoweredArgumentDefinition:
    """Contains fields meant to be passed directly into argparse."""

    # Action that is called on parsed arguments. This handles conversions from strings
    # to our desired types.
    #
    # The main reason we use this instead of the standard 'type' argument is to enable
    # mixed-type tuples.
    instantiator: Optional[_instantiators.Instantiator] = None

    def is_fixed(self) -> bool:
        """If the instantiator is set to `None`, even after all argument
        transformations, it means that we don't have a valid instantiator for an
        argument. We then mark the argument as 'fixed', with a value always equal to the
        field default."""
        return self.instantiator is None

    # From here on out, all fields correspond 1:1 to inputs to argparse's
    # add_argument() method.
    name_or_flag: str = ""
    default: Optional[Any] = None
    dest: Optional[str] = None
    required: bool = False
    action: Optional[str] = None
    nargs: Optional[Union[int, str]] = None
    choices: Optional[Set[Any]] = None
    # Note: unlike in vanilla argparse, our metavar is always a string. We handle
    # sequences, multiple arguments, etc, manually.
    metavar: Optional[str] = None
    help: Optional[str] = None


def _rule_handle_defaults(
    arg: ArgumentDefinition,
    lowered: LoweredArgumentDefinition,
) -> LoweredArgumentDefinition:
    """Set `required=True` if a default value is set."""

    # Mark lowered as required if a default is set.
    if arg.field.default in _fields.MISSING_SINGLETONS:
        return dataclasses.replace(lowered, default=None, required=True)

    return dataclasses.replace(lowered, default=arg.field.default)


def _rule_handle_boolean_flags(
    arg: ArgumentDefinition,
    lowered: LoweredArgumentDefinition,
) -> LoweredArgumentDefinition:
    if _resolver.apply_type_from_typevar(arg.field.typ, arg.type_from_typevar) is not bool:  # type: ignore
        return lowered

    if (
        arg.field.default in _fields.MISSING_SINGLETONS
        or arg.field.is_positional()
        or _markers.FlagConversionOff in arg.field.markers
        or _markers.Fixed in arg.field.markers
    ):
        # Treat bools as a normal parameter.
        return lowered
    elif arg.field.default is False:
        # Default `False` => --flag passed in flips to `True`.
        return dataclasses.replace(
            lowered,
            action="store_true",
            instantiator=lambda x: x,  # argparse will directly give us a bool!
        )
    elif arg.field.default is True:
        # Default `True` => --no-flag passed in flips to `False`.
        return dataclasses.replace(
            lowered,
            action="store_false",
            instantiator=lambda x: x,  # argparse will directly give us a bool!
        )

    assert False, (
        f"Expected a boolean as a default for {arg.field.name}, but got"
        f" {lowered.default}."
    )


def _rule_recursive_instantiator_from_type(
    arg: ArgumentDefinition,
    lowered: LoweredArgumentDefinition,
) -> LoweredArgumentDefinition:
    """The bulkiest bit: recursively analyze the type annotation and use it to determine
    how to instantiate it given some string from the commandline.

    Important: as far as argparse is concerned, all inputs are strings.

    Conversions from strings to our desired types happen in the instantiator; this is a
    bit more flexible, and lets us handle more complex types like enums and multi-type
    tuples."""
    if _markers.Fixed in arg.field.markers:
        return dataclasses.replace(
            lowered,
            instantiator=None,
            metavar="{fixed}",
            required=False,
            default=_fields.MISSING_PROP,
        )
    if lowered.instantiator is not None:
        return lowered
    try:
        instantiator, metadata = _instantiators.instantiator_from_type(
            arg.field.typ,  # type: ignore
            arg.type_from_typevar,
        )
    except _instantiators.UnsupportedTypeAnnotationError as e:
        if arg.field.default in _fields.MISSING_SINGLETONS:
            raise _instantiators.UnsupportedTypeAnnotationError(
                "Unsupported type annotation for the field"
                f" {_strings.make_field_name([arg.name_prefix, arg.field.name])}. To"
                " suppress this error, assign the field a default value."
            ) from e
        else:
            # For fields with a default, we'll get by even if there's no instantiator
            # available.
            return dataclasses.replace(
                lowered,
                metavar="{fixed}",
                required=False,
                default=_fields.MISSING_PROP,
            )

    return dataclasses.replace(
        lowered,
        instantiator=instantiator,
        choices=metadata.choices,
        nargs=metadata.nargs,
        metavar=metadata.metavar,
    )


def _rule_convert_defaults_to_strings(
    arg: ArgumentDefinition,
    lowered: LoweredArgumentDefinition,
) -> LoweredArgumentDefinition:
    """Sets all default values to strings, as required as input to our instantiator
    functions. Special-cased for enums."""

    def as_str(x: Any) -> Tuple[str, ...]:
        if isinstance(x, str):
            return (x,)
        elif isinstance(x, enum.Enum):
            return (x.name,)
        elif isinstance(x, Mapping):
            return tuple(itertools.chain(*map(as_str, itertools.chain(*x.items()))))
        elif isinstance(x, Sequence):
            return tuple(itertools.chain(*map(as_str, x)))
        else:
            return (str(x),)

    if (
        lowered.default is None
        or lowered.default in _fields.MISSING_SINGLETONS
        or lowered.action is not None
    ):
        return lowered
    else:
        return dataclasses.replace(lowered, default=as_str(lowered.default))


# This can be turned off when we don't want rich-based formatting. (notably for
# completion scripts)
#
# TODO: the global state here is gross. Should be revisited.
USE_RICH = True


# TODO: this function is also called outside of _arguments.py. Should be revisited.
def _rich_tag_if_enabled(x: str, tag: str) -> str:
    x = rich.markup.escape(_strings.strip_ansi_sequences(x))
    return x if not USE_RICH else f"[{tag}]{x}[/{tag}]"


def _rule_generate_helptext(
    arg: ArgumentDefinition,
    lowered: LoweredArgumentDefinition,
) -> LoweredArgumentDefinition:
    """Generate helptext from docstring, argument name, default values."""

    # If the suppress marker is attached, hide the argument.
    if _markers.Suppress in arg.field.markers or (
        _markers.SuppressFixed in arg.field.markers and lowered.is_fixed()
    ):
        return dataclasses.replace(lowered, help=argparse.SUPPRESS)

    help_parts = []

    primary_help = arg.field.helptext

    if primary_help is None and _markers.Positional in arg.field.markers:
        primary_help = _strings.make_field_name([arg.name_prefix, arg.field.name])

    if primary_help is not None and primary_help != "":
        # Note that the percent symbol needs some extra handling in argparse.
        # https://stackoverflow.com/questions/21168120/python-argparse-errors-with-in-help-string
        primary_help = primary_help.replace("%", "%%")
        help_parts.append(_rich_tag_if_enabled(primary_help, "helptext"))

    default = lowered.default
    if lowered.is_fixed():
        # For fixed args, we'll be missing the lowered default. Use field default
        # instead.
        assert default in _fields.MISSING_SINGLETONS
        default = arg.field.default

    if not lowered.required:
        # Include default value in helptext. We intentionally don't use the % template
        # because the types of all arguments are set to strings, which will cause the
        # default to be casted to a string and introduce extra quotation marks.
        if lowered.instantiator is None:
            # Intentionally not quoted via shlex, since this can't actually be passed
            # in via the commandline.
            default_text = f"(fixed to: {str(arg.field.default)})"
        elif lowered.action == "store_true":
            default_text = f"(sets: {arg.field.name}=True)"
        elif lowered.action == "store_false":
            default_text = f"(sets: {arg.field.name}=False)"
        elif arg.field.default is _fields.EXCLUDE_FROM_CALL:
            default_text = "(unset by default)"
        elif lowered.nargs is not None and hasattr(default, "__iter__"):
            # For tuple types, we might have default as (0, 1, 2, 3).
            # For list types, we might have default as [0, 1, 2, 3].
            # For set types, we might have default as {0, 1, 2, 3}.
            #
            # In all cases, we want to display (default: 0 1 2 3), for consistency with
            # the format that argparse expects when we set nargs.
            assert default is not None  # Just for type checker.
            default_parts = map(shlex.quote, map(str, default))
            default_text = f"(default: {' '.join(default_parts)})"
        else:
            default_text = f"(default: {shlex.quote(str(default))})"
        help_parts.append(_rich_tag_if_enabled(default_text, "helptext_default"))
    else:
        help_parts.append(_rich_tag_if_enabled("(required)", "helptext_required"))

    return dataclasses.replace(lowered, help=" ".join(help_parts))


def _rule_set_name_or_flag_and_dest(
    arg: ArgumentDefinition,
    lowered: LoweredArgumentDefinition,
) -> LoweredArgumentDefinition:
    # Positional arguments: no -- prefix.
    if arg.field.is_positional():
        name_or_flag = _strings.make_field_name([arg.name_prefix, arg.field.name])
    # Negated booleans.
    elif lowered.action == "store_false":
        name_or_flag = "--" + _strings.make_field_name(
            [arg.name_prefix, "no-" + arg.field.name]
        )
    # Prefix keyword arguments with --.
    else:
        name_or_flag = "--" + _strings.make_field_name(
            [arg.name_prefix, arg.field.name]
        )

    # Strip.
    if name_or_flag.startswith("--") and arg.subcommand_prefix != "":
        # This will run even when unused because we want the assert.
        strip_prefix = "--" + arg.subcommand_prefix + "."
        assert name_or_flag.startswith(strip_prefix)
        if _markers.OmitSubcommandPrefixes in arg.field.markers:
            name_or_flag = "--" + name_or_flag[len(strip_prefix) :]

    return dataclasses.replace(
        lowered,
        name_or_flag=name_or_flag,
        dest=_strings.make_field_name([arg.dest_prefix, arg.field.name]),
    )


def _rule_positional_special_handling(
    arg: ArgumentDefinition,
    lowered: LoweredArgumentDefinition,
) -> LoweredArgumentDefinition:
    if not arg.field.is_positional():
        return lowered

    metavar = lowered.metavar
    if lowered.required:
        nargs = lowered.nargs
    else:
        if metavar is not None:
            metavar = "[" + metavar + "]"
        if lowered.nargs == 1:
            # Optional positional arguments. Note that this needs to be special-cased in
            # _calling.py.
            nargs = "?"
        else:
            # If lowered.nargs is either + or an int.
            nargs = "*"

    return dataclasses.replace(
        lowered,
        dest=None,
        required=None,  # Can't be passed in for positionals.
        metavar=metavar,
        nargs=nargs,
    )


class _PatchedList(list):
    """Custom list type, for avoiding "default not in choices" errors when the default
    is set to MISSING_NONPROP.

    This solves a choices error raised by argparse in a very specific edge case:
    literals in containers as positional arguments."""

    def __init__(self, li):
        super(_PatchedList, self).__init__(li)

    def __contains__(self, x: Any) -> bool:
        return list.__contains__(self, x) or x is _fields.MISSING_NONPROP


def _rule_static_cast_choices_to_patched_list(
    arg: ArgumentDefinition,
    lowered: LoweredArgumentDefinition,
) -> LoweredArgumentDefinition:
    return dataclasses.replace(
        lowered,
        choices=_PatchedList(lowered.choices) if lowered.choices is not None else None,
    )
