from typing import Callable
from dataclasses import dataclass, field

import narwhals as nw


@dataclass(kw_only=True)
class Converter:
    """Base converter class."""

    name: str
    description: str = field(default=None)
    converter: Callable

    def __post_init__(self):
        if self.description is None:
            self.description = self.converter.__doc__ or "Missing description"

    def __convert__(self):
        raise NotImplementedError("Method not yet implemented.")

    def convert(self, data: nw.DataFrame) -> nw.DataFrame:
        return self.__convert__(data)


@dataclass
class FieldConverter(Converter):
    def __convert__(self, column: nw.Expr) -> nw.Expr:
        return self.converter(column)

    def bind(self, *args: tuple, **kwargs: dict) -> "FieldConverter":
        return FieldConverter(
            name=self.name,
            description=self.description,
            converter=self.converter(*args, **kwargs),
        )


@dataclass
class DataFrameConverter(Converter):
    def __convert__(self, data: nw.DataFrame) -> nw.DataFrame:
        return self.converter(data)

    def bind(self, *args: tuple, **kwargs: dict) -> "DataFrameConverter":
        return DataFrameConverter(
            name=self.name,
            description=self.description,
            converter=self.converter(*args, **kwargs),
        )
