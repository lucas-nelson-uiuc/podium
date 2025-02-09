from typing import Any, Literal, Callable

import narwhals as nw
from narwhals.typing import IntoExpr

from podium.utils import _as_expr


def replace(*args, **kwargs) -> IntoExpr:
    """Transform expression to replace characters."""

    def _replace(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.replace(*args, **kwargs)

    return _replace


def replace_all(*args, **kwargs) -> IntoExpr:
    """Transform expression to replace all instances."""

    def _replace_all(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.replace_all(*args, **kwargs)

    return _replace_all


def to_datetime(*args, **kwargs) -> IntoExpr:
    """Transform expression as datetime string."""

    def _to_datetime(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.to_datetime(*args, **kwargs)

    return _to_datetime


def to_lowercase(column: IntoExpr) -> IntoExpr:
    """Transform expression as lowercase string."""
    return _as_expr(column).str.to_lowercase()


def to_uppercase(column: IntoExpr) -> IntoExpr:
    """Transform expression as uppercase string."""
    return _as_expr(column).str.to_uppercase()
