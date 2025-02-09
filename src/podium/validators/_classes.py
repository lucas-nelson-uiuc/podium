from typing import Callable, Optional

from dataclasses import dataclass

import functools
import operator

import narwhals as nw
from narwhals.typing import DataFrameT, IntoExpr, IntoDataFrame


@dataclass
class Validator:
    name: str
    description: str
    validator: Callable

    def __validate__(self, data: DataFrameT) -> IntoDataFrame:
        raise NotImplementedError("Method not yet implemented.")

    def __is_valid__(self, data: DataFrameT) -> bool:
        raise NotImplementedError("Method not yet implemented.")

    def validate(self, data: DataFrameT) -> None:
        invalid_obs = self.__validate__(data)
        try:
            assert self.__is_valid__(invalid_obs)
            log_level = "success"
            log_msg = "All column(s) passed the validation."
        except AssertionError:
            log_level = "failure"
            log_msg = "At least one column failed the validation."
            print(invalid_obs)
        except Exception as e:
            raise e
        finally:
            print(f"{self.name} | {log_level}: {log_msg}")


@dataclass
class FieldValidator(Validator):
    """Base class for field validator."""

    def __validate__(self, data: DataFrameT) -> None:
        return nw.from_native(data).filter(self.validator)

    def __is_valid__(self, data: DataFrameT) -> bool:
        return data.is_empty()

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


@dataclass
class DataFrameValidator(Validator):
    """Base class for DataFrame validator."""

    def __validate__(self, data: DataFrameT) -> DataFrameT:
        return self.validator(nw.from_native(data))

    def __is_valid__(self, data: DataFrameT) -> bool:
        return not data.any()

    def bind(self, *args: tuple, **kwargs: dict) -> "DataFrameValidator":
        """Partially define validator with arguments."""
        return DataFrameValidator(
            name=self.name,
            description=self.description,
            validator=self.validator(*args, **kwargs),
        )
        

@dataclass
class RelationshipValidator(DataFrameValidator):
    """Base class for DataFrame Relationship validator."""

    def __is_valid__(self, data: DataFrameT) -> bool:
        return data.is_empty()


@dataclass
class SchemaValidator(Validator):
    def __validate__(self, schema: DataFrameT) -> DataFrameT:
        return self.validator(schema)

    def __is_valid__(self, schema: DataFrameT) -> DataFrameT:
        return schema.len() > 1
