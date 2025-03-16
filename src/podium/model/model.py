from typing import Optional, Callable

import narwhals as nw

from podium.model.field import Field


class Model:
    """Base class representing data-expression workflow."""

    @classmethod
    def schema(cls, predicate: Callable | None = None) -> dict:
        """Return class schema."""
        schema = cls.__annotations__
        if predicate is None:
            return schema
        return list(filter(predicate, schema))

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
