from typing import Callable, Optional

from dataclasses import dataclass, field

import functools
import operator

import narwhals as nw
from narwhals.typing import DataFrameT, IntoExpr, IntoDataFrame

from podium_lib.describe import get_default_args, update_description


class Validator:
    """Base class for validator constructor."""

    def __init__(self, name: str, validator: Callable = None, description: str = None):
        self.name = name
        self.validator = validator
        if description is None:
            self.description = validator.__doc__ or "Missing description"

    def __podium_validate__(self, data: DataFrameT) -> IntoDataFrame:
        raise NotImplementedError("Method not yet implemented.")

    def __podium_is_valid__(self, data: DataFrameT) -> bool:
        raise NotImplementedError("Method not yet implemented.")

    def describe(self) -> str:
        return self.description

    def bind(self, *args, **kwargs) -> "Validator":
        """Update validator according to parameters."""
        return self.__class__(
            name=self.name,
            description=update_description(
                self.description,
                *args,
                defaults=get_default_args(self.validator),
                **kwargs,
            ),
            validator=self.validator(*args, **kwargs),
        )

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


class FieldValidator(Validator):
    """Base class for field validator."""

    def __podium_validate__(self, data: DataFrameT) -> None:
        return nw.from_native(data).filter(self.validator)

    def __podium_is_valid__(self, data: DataFrameT) -> bool:
        return data.is_empty()

    def _construct_validator(
        self, *column: str, strict: bool, invert: bool
    ) -> IntoExpr:
        """Apply validator to column(s) with optional parameters."""
        compare_op = operator.and_ if strict else operator.or_
        query = functools.reduce(compare_op, map(self.validator, column))
        return operator.inv(query) if invert else query

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


class DataFrameValidator(Validator):
    """Base class for DataFrame validator."""

    def __podium_validate__(self, data: nw.DataFrame) -> nw.DataFrame:
        return self.validator(nw.from_native(data))

    def __podium_is_valid__(self, data: nw.DataFrame) -> bool:
        return not data.any()


class RelationshipValidator(DataFrameValidator):
    """Base class for DataFrame Relationship validator."""

    def __podium_is_valid__(self, data: nw.DataFrame) -> bool:
        return data.is_empty()


class SchemaValidator(Validator):
    def __podium_validate__(self, schema: nw.Schema):
        return self.validator(schema)

    def __podium_is_valid__(self, schema: nw.Schema) -> bool:
        return schema.len() > 1
