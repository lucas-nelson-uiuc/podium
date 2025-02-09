from typing import Callable, Optional, Self

from dataclasses import dataclass

import functools
import operator

import narwhals as nw
from narwhals.typing import DataFrameT, IntoExpr


@dataclass
class Validator:
    name: str
    description: str
    validator: Callable

    def __validate__(self, data: DataFrameT) -> None:
        return self.validator(data)

    def validate(self, data: DataFrameT) -> None:
        invalid_obs = self.__validate__(data)
        try:
            assert invalid_obs.is_empty()
            log_level = "success"
            log_msg = "All column(s) passed the validation."
        except AssertionError:
            log_level = "failure"
            log_msg = "At least one column failed the validation."
            print(invalid_obs)
        finally:
            print(f"{self.name} | {log_level}: {log_msg}")


@dataclass
class FieldValidator(Validator):
    """Base class for field validator."""

    def _construct_validator(
        self, *column: str, strict: bool, invert: bool
    ) -> IntoExpr:
        """Apply validator to column(s) with optional parameters."""
        compare_op = operator.and_ if strict else operator.or_
        query = functools.reduce(compare_op, map(self.validator, column))
        return operator.inv(query) if invert else query

    def bind(self, *args: tuple, **kwargs: dict) -> "FieldValidator":
        """Partially define validator with arguments."""
        return FieldValidator(
            name=self.name,
            description=self.description,
            validator=self.validator(*args, **kwargs),
        )

    def construct(
        self,
        *column: str,
        strict: Optional[bool] = False,
        invert: Optional[bool] = False,
        **kwargs: dict,
    ) -> "FieldValidator":
        """Construct validator with required inputs."""
        return FieldValidator(
            name=self.name,
            description=self.description,
            validator=self._construct_validator(
                *column, strict=strict, invert=invert, **kwargs
            ),
        )

    def __validate__(self, data: DataFrameT) -> None:
        return nw.from_native(data).filter(self.validator).to_native()


@dataclass
class DataFrameValidator(Validator):
    pass


@dataclass
class SchemaValidator(Validator):
    pass
