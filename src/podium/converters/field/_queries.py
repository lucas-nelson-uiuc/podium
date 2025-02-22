from narwhals.typing import ExprT

from podium.utils import _as_expr


def len_chars(column: ExprT) -> ExprT:
    return _as_expr(column).str.len_chars()


def replace(pattern: str, value: str, *, literal: bool = False, n: int = 1) -> ExprT:
    """Replace first matching regex/literal $pattern with $value."""

    def _replace(column: ExprT) -> ExprT:
        return _as_expr(column).str.replace(pattern, value, literal=literal, n=n)

    return _replace


def replace_all(pattern: str, value: str, *, literal: bool = False) -> ExprT:
    """Replace all matching regex/literal $pattern with $value."""

    def _replace(column: ExprT) -> ExprT:
        return _as_expr(column).str.replace_all(pattern, value, literal=literal)

    return _replace


def strip_chars(characters: str | None = None) -> ExprT:
    """Remove leading and trailing spaces ($characters)."""

    def _strip_chars(column: ExprT) -> ExprT:
        return _as_expr(column).str.strip_chars(characters)

    return _strip_chars


def to_datetime(format: str | None = None) -> ExprT:
    """Convert to Datetime dtype (format=$format)."""

    def _to_datetime(column: ExprT) -> ExprT:
        return _as_expr(column).str.to_datetime(format=format)

    return _to_datetime


def to_lowercase(column: ExprT) -> ExprT:
    """Transform string to lowercase variant."""
    return _as_expr(column).str.to_lowercase()


def to_uppercase(column: ExprT) -> ExprT:
    """Transform string to uppercase variant."""
    return _as_expr(column).str.to_uppercase()
