from typing import Literal
import narwhals as nw


def drop_nulls(subset: str | list[str] | None = None) -> nw.DataFrame:
    """Remove all null values across specified subset."""

    def _drop_nulls(data: nw.DataFrame):
        return data.drop_nulls(subset=subset)

    return _drop_nulls


def unique(
    subset: str | list[str] | None = None,
    keep: Literal["any", "first", "last", "none"] = "any",
    maintain_order: bool = False,
) -> nw.DataFrame:
    """Retain all values across specified subset."""

    def _unique(data: nw.DataFrame):
        return data.unique(subset=subset, keep=keep, maintain_order=maintain_order)

    return _unique
