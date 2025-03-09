from typing import Optional

import narwhals as nw

from podium_lib.model.field import Field


# @dataclass
# class Model:
#     """Podium Model class."""

#     @classmethod
#     def fields(cls, criteria: Callable = None) -> Sequence[Field]:
#         """Extract fields from class with optional criteria."""
#         fields = [getattr(cls, model_field) for model_field in cls.__dataclass_fields__]
#         if criteria is None:
#             return fields
#         return list(filter(criteria, fields))

#     @classmethod
#     def document(
#         cls, attributes: Sequence[str] = None, criteria: Callable = None
#     ) -> Sequence[dict]:
#         """Return documentation of class."""
#         return [
#             field.document(attributes=attributes)
#             for field in cls.fields(criteria=criteria)
#         ]

#     @classmethod
#     def __preprocess__(cls, data: DataFrameT) -> DataFrameT:
#         """Process dataframe prior to conversion and validation."""
#         return data

#     @classmethod
#     def __postprocess__(cls, data: DataFrameT) -> DataFrameT:
#         """Process dataframe after applying conversion and valdiation."""
#         return data

#     @classmethod
#     def convert(cls, data: DataFrameT) -> DataFrameT:
#         """Apply field-level converters to all fields in model."""
#         return data.with_columns(
#             *(
#                 podium_field.convert(column_exists=podium_field.name in data.columns)
#                 for podium_field in cls.fields()
#             )
#         )

#     # @classmethod
#     # def validate(cls, data: DataFrameT) -> None:
#     #     for podium_field in cls.fields():
#     #         if podium_field.validator is None:
#     #             pass
#     #         column = nw.col(podium_field.alias)
#     #         invalid_obs = data.select(column).filter(podium_field.validator(column))
#     #         try:
#     #             assert invalid_obs.is_empty()
#     #             log_level = "SUCCESS"
#     #             log_msg = "All observations passed the validator(s)."
#     #         except AssertionError:
#     #             log_level = "FAILURE"
#     #             log_msg = "At least one observation failed the validator(s)."
#     #             cls.__tracing__.errors[podium_field.name] = (
#     #                 podium_field.validator,
#     #                 invalid_obs,
#     #             )
#     #         finally:
#     #             print(f"{podium_field.name} | {log_level}: {log_msg}")


class Model:
    """Base class representing data-expression workflow."""

    @classmethod
    def schema(cls) -> dict:
        """Return class schema."""
        return cls.__annotations__

    @classmethod
    def workflow(cls) -> dict:
        """Return planned query of operations."""

        def assign_value(alias: str, dtype: type, field: Optional[dict]):
            """Handle field creation based on class definition."""
            if field is None:
                field = dict()
            if isinstance(field, Field):
                field = field.to_dict()

            field = {"alias": alias, "dtype": dtype} | field
            return Field(**field)

        return {
            field: assign_value(alias=field, dtype=dtype, field=cls.__dict__.get(field))
            for field, dtype in cls.schema().items()
        }

    @classmethod
    def convert(cls, data: nw.DataFrame) -> nw.DataFrame:
        """Apply field-level conversions to data."""
        conversions = {name: field.convert() for name, field in cls.workflow()}
        return (
            data.pipe(cls.__preprocess__)
            .with_columns(**conversions)
            .pipe(cls.__postprocess__)
        )

    @classmethod
    def validate(cls, data: nw.DataFrame) -> nw.DataFrame:
        """Run all provided validations against a DataFrame."""
        for name, field in cls.workflow():
            if field.validator:
                try:
                    field.validator.validate(data)
                    level = "success"
                    msg = "All observations passed"
                except AssertionError as e:
                    level = getattr(field.validator, "level", "error")
                    msg = "At least one observation failed"
                except Exception as e:
                    raise e
                finally:
                    # TODO: replace with logging module
                    print(f"{level.upper()} | {msg}")

    @classmethod
    def __preprocess__(cls, data: nw.DataFrame) -> nw.DataFrame:
        """Perform optional processing function to run before conversions."""
        return data

    @classmethod
    def __postprocess__(cls, data: nw.DataFrame) -> nw.DataFrame:
        """Perform optional processing function to run after conversions."""
        return data
