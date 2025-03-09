from typing import Literal
import narwhals as nw


def drop_nulls(subset: str | list[str] | None = None) -> nw.DataFrame:
    """Drop rows that contain null values (subset=$subset)."""

    def _drop_nulls(data: nw.DataFrame):
        return data.drop_nulls(subset=subset)

    return _drop_nulls


def unique(
    subset: str | list[str] | None = None,
    keep: Literal["any", "first", "last", "none"] = "any",
    maintain_order: bool = False,
) -> nw.DataFrame:
    """Drop duplicate rows from DataFrame (subset=$subset, keep=$keep, maintain_order=$maintain_order)."""

    def _unique(data: nw.DataFrame):
        return data.unique(subset=subset, keep=keep, maintain_order=maintain_order)

    return _unique
