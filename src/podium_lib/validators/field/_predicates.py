from typing import Any, Literal, Callable

from narwhals.typing import IntoExpr

from podium_lib.utils import _as_expr


def is_between(
    lower_bound: Any | IntoExpr,
    upper_bound: Any | IntoExpr,
    closed: Literal["left", "right", "none", "both"] = "both",
) -> IntoExpr:
    """Check that column contains values between $lower_bound and $upper_bound (bounded $closed)."""

    def _is_between(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).is_between(lower_bound, upper_bound, closed)

    return _is_between


def is_duplicate(column: IntoExpr) -> IntoExpr:
    """Check that column contains duplicated values."""
    return _as_expr(column).is_duplicated()


def is_finite(column: IntoExpr) -> IntoExpr:
    """Check that column contains finite values."""
    return _as_expr(column).is_finite()


def is_in(other: Any) -> Callable:
    """Check that column contains $other values."""

    def _is_in(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).is_in(other)

    return _is_in


def is_nan(column: IntoExpr) -> IntoExpr:
    """Check that column contains NaN values."""
    return _as_expr(column).is_nan()


def is_null(column: IntoExpr) -> IntoExpr:
    """Check that column contains null values."""
    return _as_expr(column).is_null()


def is_unique(column: IntoExpr) -> IntoExpr:
    """Check that column contains no duplicated values."""
    return _as_expr(column).is_unique()


def ends_with(suffix: str) -> IntoExpr:
    """Check that column ends with '$suffix'."""

    def _ends_with(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.ends_with(suffix=suffix)

    return _ends_with


def starts_with(prefix: str) -> IntoExpr:
    """Check that column starts with '$prefix'."""

    def _starts_with(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.starts_with(prefix=prefix)

    return _starts_with


def matches_pattern(pattern: str, literal: bool = False) -> IntoExpr:
    """Check that column matches '$pattern'."""

    def _matches_pattern(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.contains(pattern, literal=literal)

    return _matches_pattern


def min_length(length: int) -> IntoExpr:
    """Check that column does is no shorter than $length characters."""

    def _min_length(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.len_chars() >= length

    return _min_length


def max_length(length: int) -> IntoExpr:
    """Check that column does is no longer than $length characters."""

    def _max_length(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.len_chars() <= length

    return _max_length
