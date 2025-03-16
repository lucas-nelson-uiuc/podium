import difflib
from typing import Any
from podium_lib import Model, Field


def is_equal(*object: Any, attr: str | None = None) -> None:
    """Validate that objects are equal."""
    if len(object) < 2:
        raise ValueError(
            f"Expected at least two objects to compare, received {len(object)}"
        )

    if attr is not None:
        if not all(hasattr(obj, attr) for obj in object):
            raise AttributeError(f"Not all objects have the attribute `{attr}`")
        object = list(
            getattr(obj, attr).__call__() for obj in object
        )  # TODO: revisit the call method

    assert all(obj == object[0] for obj in object)


def assert_field_equal(*field: Field) -> None:
    """Validate that fields are equal."""
    assert all(isinstance(obj, Field) for obj in field)
    is_equal(*field)


def assert_schema_equal(*model: Model) -> None:
    """Validate that schemas are equal."""
    assert all(isinstance(obj, Model) for obj in model)
    is_equal(*model, attr="schema")


def assert_workflow_equal(*model: Model) -> None:
    """Validate that workflows are equal."""
    assert all(isinstance(obj, Model) for obj in model)
    is_equal(*model, attr="workflow")
