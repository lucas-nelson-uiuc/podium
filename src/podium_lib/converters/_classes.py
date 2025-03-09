from typing import Callable
from dataclasses import dataclass, field

import narwhals as nw

from podium_lib.describe import get_default_args, update_description


class Converter:
    """Base converter class."""

    def __init__(
        self,
        name: str,
        converter: Callable,
        description: str = None,
    ):
        self.name = name
        self.converter = converter
        if description is None:
            self.description = converter.__doc__ or "Missing description"
        else:
            self.description = description

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


class FieldConverter(Converter):
    def __podium_convert__(self, column: nw.Expr) -> nw.Expr:
        return self.converter(column)


class DataFrameConverter(Converter):
    def __podium_convert__(self, data: nw.DataFrame) -> nw.DataFrame:
        return self.converter(data)
