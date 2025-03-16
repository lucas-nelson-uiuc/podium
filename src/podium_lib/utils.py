import narwhals as nw
from narwhals.typing import IntoExpr


def _as_expr(column: IntoExpr) -> IntoExpr:
    """Coerce column-like object to expression."""
    if not isinstance(column, nw.Expr):
        column = nw.col(column)
    return column
