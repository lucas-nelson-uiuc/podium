from typing import Any, Literal, Callable

import narwhals as nw
from narwhals.typing import IntoExpr


def _as_expr(column: str | nw.Expr) -> IntoExpr:
    """Coerce column-like object to expression."""
    if not isinstance(column, nw.Expr):
        column = nw.col(column)
    return column


def is_between(
    lower_bound: Any | IntoExpr,
    upper_bound: Any | IntoExpr,
    closed: Literal["left", "right", "none", "both"] = "both",
) -> IntoExpr:
    """Check that column contains values between the boundaries."""

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
    """Check that column contains `other` values."""

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
