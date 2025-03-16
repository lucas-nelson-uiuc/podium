import narwhals as nw
from narwhals.typing import IntoExpr, IntoExprT


def _as_expr(column: str | IntoExprT) -> IntoExpr:
    """Coerce column-like object to expression."""
    if not isinstance(column, IntoExprT):
        column = nw.col(column)
    return column
