from narwhals.typing import IntoExpr

from podium_lib.utils import _as_expr


def len_chars(column: IntoExpr) -> IntoExpr:
    return _as_expr(column).str.len_chars()


def replace(pattern: str, value: str, *, literal: bool = False, n: int = 1) -> IntoExpr:
    """Replace first matching regex/literal $pattern with $value."""

    def _replace(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.replace(pattern, value, literal=literal, n=n)

    return _replace


def replace_all(pattern: str, value: str, *, literal: bool = False) -> IntoExpr:
    """Replace all matching regex/literal $pattern with $value."""

    def _replace(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.replace_all(pattern, value, literal=literal)

    return _replace


def strip_chars(characters: str | None = None) -> IntoExpr:
    """Remove leading and trailing spaces ($characters)."""

    def _strip_chars(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.strip_chars(characters)

    return _strip_chars


def to_datetime(format: str | None = None) -> IntoExpr:
    """Convert to Datetime dtype (format=$format)."""

    def _to_datetime(column: IntoExpr) -> IntoExpr:
        return _as_expr(column).str.to_datetime(format=format)

    return _to_datetime


def to_lowercase(column: IntoExpr) -> IntoExpr:
    """Transform string to lowercase variant."""
    return _as_expr(column).str.to_lowercase()


def to_uppercase(column: IntoExpr) -> IntoExpr:
    """Transform string to uppercase variant."""
    return _as_expr(column).str.to_uppercase()
