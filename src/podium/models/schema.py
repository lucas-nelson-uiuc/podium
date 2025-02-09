from typing import Sequence, Callable

from dataclasses import dataclass

import narwhals as nw
from narwhals.typing import DataFrameT

from podium.models.field import Field


@dataclass
class Schema:
    @classmethod
    def fields(cls, criteria: Callable = None) -> Sequence[Field]:
        fields = [
            getattr(cls, schema_field) for schema_field in cls.__dataclass_fields__
        ]
        if criteria is None:
            return fields
        return list(filter(criteria, fields))

    @classmethod
    def __preprocess__(cls, data: DataFrameT) -> DataFrameT:
        return data

    @classmethod
    def __postprocess__(cls, data: DataFrameT) -> DataFrameT:
        return data

    @classmethod
    def convert(cls, data: DataFrameT) -> DataFrameT:
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
