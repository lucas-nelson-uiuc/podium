from typing import Optional, Callable

import narwhals as nw

from podium_lib.model.field import Field


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

        def assign_value(name: str, dtype: type, field: Optional[dict]):
            """Handle field creation based on class definition."""
            if field is None:
                field = dict()
            if isinstance(field, Field):
                field = field.to_dict()

            field = {"name": name, "dtype": dtype} | field
            return Field(**field)

        return {
            field: assign_value(name=field, dtype=dtype, field=cls.__dict__.get(field))
            for field, dtype in cls.schema().items()
        }

    @classmethod
    def __preprocess__(cls, data: nw.DataFrame) -> nw.DataFrame:
        """Perform optional processing function to run before conversions."""
        return data

    @classmethod
    def __postprocess__(cls, data: nw.DataFrame) -> nw.DataFrame:
        """Perform optional processing function to run after conversions."""
        return data

    @classmethod
    def convert(cls, data: nw.DataFrame) -> nw.DataFrame:
        """Apply field-level conversions to data."""
        conversions = [field.convert() for field in cls.workflow().values()]
        return (
            nw.from_native(data)
            .pipe(cls.__preprocess__)
            .with_columns(*conversions)
            .pipe(cls.__postprocess__)
            .to_native()
        )

    @classmethod
    def validate(cls, data: nw.DataFrame) -> nw.DataFrame:
        """Run all provided validations against a DataFrame."""
        data = nw.from_native(data)
        for field in cls.workflow().values():
            if field.validator:
                try:
                    validator = field.validator.construct(field.alias)
                    validator.validate(data)
                except Exception as e:
                    raise e
