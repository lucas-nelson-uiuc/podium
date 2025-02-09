from typing import Callable
from dataclasses import dataclass

import narwhals as nw


@dataclass
class Converter:
    """Base converter class."""

    name: str
    description: str
    converter: Callable

    def __convert__(self):
        raise NotImplementedError("Method not yet implemented.")


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

    # def construct(self, column: str) -> "FieldConverter": # TODO: allow multiple columns?
    #     return FieldConverter(
    #         name=self.name,
    #         description=self.description,
    #         converter=self.converter(column)
    #     )
