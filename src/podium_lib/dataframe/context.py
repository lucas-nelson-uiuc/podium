from typing import Sequence
from podium_lib.logging import Handler


class Context:
    """Base class for configuring PodiumDataFrame objects."""

    def __init__(self):
        name: str
        description: str
        handler: Handler | Sequence[Handler]
