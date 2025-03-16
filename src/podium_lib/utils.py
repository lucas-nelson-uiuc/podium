import narwhals as nw
from narwhals.typing import IntoExpr


def _as_expr(column: str | IntoExpr) -> IntoExpr:
    """Coerce column-like object to expression."""
    if not isinstance(column, IntoExpr):
        column = nw.col(column)
    return column
