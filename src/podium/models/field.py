from typing import Any, Callable, Optional

import functools

import narwhals as nw
from narwhals.typing import IntoExpr


class Field:
    def __init__(
        self,
        name: str,
        dtype: Any,
        alias: str = None,
        description: str = None,
        default: Any = None,
        factory: Callable[[Any], Any] = None,
        converter: Callable[[Any], Any] = None,
        validator: Callable[[Any], Any] = None,
        # metadata: dict[str, Any] = None,
    ):
        if (default is not None) and (factory is not None):
            raise ValueError("Cannot pass default and factory.")

        self.name = name
        self.dtype = dtype
        self.alias = alias or name
        self.description = description
        self.default = default or factory
        self.converter = converter
        self.validator = validator
        # self.metadata = metadata

    def __repr__(self) -> str:
        return f"PodiumField(name={self.name}, dtype={self.dtype})"

    def _cast_dtype(self, column: IntoExpr) -> IntoExpr:
        """Cast column to target data type."""
        assert issubclass(self.dtype, nw.dtypes.DType)
        return column.cast(self.dtype)

    def _apply_converter(self, column: IntoExpr) -> IntoExpr:
        """Transform column according to defined converter(s)."""
        if isinstance(self.converter, Callable):
            return self.converter(column)
        return functools.reduce(
            lambda expr, func: expr.pipe(func), self.converter, column
        )

    def convert(self, column_exists: Optional[bool] = True) -> IntoExpr:
        """Construct expression using field definition."""

        if column_exists:
            column = nw.col(self.name)
        else:
            column = nw.lit(self.default)

        if self.dtype:
            column = self._cast_dtype(column)

        if self.default:
            if isinstance(self.default, Callable):
                column = self.default(column)
            else:
                column = column.fill_null(value=self.default)

        if self.converter:
            column = self._apply_converter(column)

        return column.alias(self.alias)

    # def _apply_validator(self, column: IntoExpr) -> IntoExpr:
    #     """Assert validator(s) are true for all values in column."""
    #     if isinstance(self.validator, Callable):
    #         return self.validator(column)
    #     return functools.reduce(
    #         operator.and_, map(lambda func: func(column), self.validator)
    #     )

    # def validate(self) -> IntoExpr:
    #     column = nw.col(self.alias)
    #     validator_expr = self._apply_validator(column)
    #     return operator.inv(validator_expr)
