from typing import Sequence, Callable

from dataclasses import dataclass

from narwhals.typing import DataFrameT

from podium.model.field import Field


@dataclass
class Model:
    """Podium Model class."""

    @classmethod
    def fields(cls, criteria: Callable = None) -> Sequence[Field]:
        """Extract fields from class with optional criteria."""
        fields = [getattr(cls, model_field) for model_field in cls.__dataclass_fields__]
        if criteria is None:
            return fields
        return list(filter(criteria, fields))

    @classmethod
    def document(
        cls, attributes: Sequence[str] = None, criteria: Callable = None
    ) -> Sequence[dict]:
        """Return documentation of class."""
        return [
            field.document(attributes=attributes)
            for field in cls.fields(criteria=criteria)
        ]

    @classmethod
    def __preprocess__(cls, data: DataFrameT) -> DataFrameT:
        """Process dataframe prior to conversion and validation."""
        return data

    @classmethod
    def __postprocess__(cls, data: DataFrameT) -> DataFrameT:
        """Process dataframe after applying conversion and valdiation."""
        return data

    @classmethod
    def convert(cls, data: DataFrameT) -> DataFrameT:
        """Apply field-level converters to all fields in model."""
        return data.with_columns(
            *(
                podium_field.convert(column_exists=podium_field.name in data.columns)
                for podium_field in cls.fields()
            )
        )

    # @classmethod
    # def validate(cls, data: DataFrameT) -> None:
    #     for podium_field in cls.fields():
    #         if podium_field.validator is None:
    #             pass
    #         column = nw.col(podium_field.alias)
    #         invalid_obs = data.select(column).filter(podium_field.validator(column))
    #         try:
    #             assert invalid_obs.is_empty()
    #             log_level = "SUCCESS"
    #             log_msg = "All observations passed the validator(s)."
    #         except AssertionError:
    #             log_level = "FAILURE"
    #             log_msg = "At least one observation failed the validator(s)."
    #             cls.__tracing__.errors[podium_field.name] = (
    #                 podium_field.validator,
    #                 invalid_obs,
    #             )
    #         finally:
    #             print(f"{podium_field.name} | {log_level}: {log_msg}")
