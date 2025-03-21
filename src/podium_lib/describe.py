import sys
import inspect
import string
from typing import Iterable


def get_default_args(func):
    """Return default arguments from function."""
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def get_identifiers(template: string.Template) -> Iterable[str]:
    """
    Extract identifiers from template.

    NOTE: can be removed once python < 3.10 is no longer supported
    """

    def _get_identifiers(template: string.Template):
        import re

        pattern = f"{template.delimiter}({template.idpattern})"
        return set(
            m.group(1)
            for m in re.finditer(pattern, template.template, flags=template.flags)
        )

    if sys.version_info >= (3, 11):
        return string.Template.get_identifiers(template)
    else:
        return _get_identifiers(template)


def update_description(description: str, *args, defaults: dict = None, **kwargs) -> str:
    """Update description using provided parameters."""
    template = string.Template(description)
    mapping = dict()

    if defaults is not None:
        mapping |= defaults

    if args:
        identifiers = get_identifiers(template)
        mapping |= {i: v for i, v in zip(identifiers[: len(args)], args)}

    if kwargs:
        mapping |= kwargs

    return template.safe_substitute(mapping)
