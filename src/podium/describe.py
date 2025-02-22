import inspect
import string


def get_default_args(func):
    """Return default arguments from function."""
    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def update_description(description: str, *args, defaults: dict = None, **kwargs) -> str:
    """Update description using provided parameters."""
    template = string.Template(description)
    identifiers = template.get_identifiers()
    mapping = dict()
    if defaults is not None:
        mapping |= defaults
    if args:
        mapping |= {i: v for i, v in zip(identifiers[: len(args)], args)}
    if kwargs:
        mapping |= kwargs
    return template.safe_substitute(mapping)
