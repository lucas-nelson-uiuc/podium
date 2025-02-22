from typing import Callable
from dataclasses import dataclass, field

import narwhals as nw

from podium.describe import get_default_args, update_description


@dataclass(kw_only=True)
class Converter:
    """Base converter class."""

    name: str
    description: str = field(default=None)
    converter: Callable

    def __post_init__(self):
        if self.description is None:
            self.description = self.converter.__doc__ or "Missing description"

    def __podium_convert__(self):
        raise NotImplementedError("Method not yet implemented.")

    def bind(self, *args: tuple, **kwargs: dict) -> "FieldConverter":
        return FieldConverter(
            name=self.name,
            description=update_description(
                self.description,
                *args,
                defaults=get_default_args(self.converter),
                **kwargs,
            ),
            converter=self.converter(*args, **kwargs),
        )

    def convert(self, data: nw.DataFrame) -> nw.DataFrame:
        return self.__podium_convert__(data)


@dataclass
class FieldConverter(Converter):
    def __podium_convert__(self, column: nw.Expr) -> nw.Expr:
        return self.converter(column)


@dataclass
class DataFrameConverter(Converter):
    def __podium_convert__(self, data: nw.DataFrame) -> nw.DataFrame:
        return self.converter(data)
