from typing import Callable

import narwhals as nw
from narwhals.typing import DataFrameT, IntoDataFrame, IntoExpr


def _as_frame(data: DataFrameT) -> IntoDataFrame:
    if not isinstance(data, nw.DataFrame):
        data = nw.from_native(data)
    return data


def is_duplicated(columns: IntoExpr) -> Callable:
    """Check for any duplicate observations across all column(s)."""

    def _is_duplicated(data: DataFrameT) -> IntoDataFrame:
        return _as_frame(data).select(columns).is_duplicated()

    return _is_duplicated


def is_unique(columns: IntoExpr) -> Callable:
    """Check for any duplicate observations across all column(s)."""

    def _is_unique(data: DataFrameT) -> IntoDataFrame:
        return _as_frame(data).select(columns).is_unique()

    return _is_unique


def is_one_to_one(*keys: IntoExpr, value: IntoExpr) -> Callable:
    """Check that all observations between $keys and $value are one-to-one."""

    def _is_one_to_one(data: DataFrameT) -> IntoDataFrame:
        distinct_values = (
            _as_frame(data)
            .group_by(*keys)
            .agg(nw.col(value).n_unique().alias("Distinct Count"))
        )
        return distinct_values.filter(nw.col("Distinct Count") > 1)

    return _is_one_to_one


def is_one_to_many(key: IntoExpr, *values: IntoExpr) -> Callable:
    """Check that all observations between $key and $values are one-to-many."""

    def _is_one_to_many(data: DataFrameT) -> IntoDataFrame:
        distinct_values = (
            _as_frame(data)
            .group_by(key)
            .agg(
                nw.concat_str(*values, separator="|").unique().alias("Distinct Values"),
                nw.concat_str(*values, separator="|")
                .n_unique()
                .alias("Distinct Count"),
            )
        )
        return distinct_values.filter(nw.col("Distinct Count") > 1)

    return _is_one_to_many


def is_many_to_one(*keys: IntoExpr, value: IntoExpr) -> Callable:
    """Check that all observations between $keys and $value are many-to-one."""

    def _is_many_to_one(data: DataFrameT) -> IntoDataFrame:
        distinct_values = (
            _as_frame(data)
            .group_by(value)
            .agg(
                nw.concat_str(*keys, separator="|").unique().alias("Distinct Values"),
                nw.concat_str(*keys, separator="|").n_unique().alias("Distinct Count"),
            )
        )
        return distinct_values.filter(nw.col("Distinct Count") > 1)

    return _is_many_to_one
