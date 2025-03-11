import narwhals as nw

from podium_lib.dataframe.context import PodiumConfig


class DataFrame(nw.DataFrame):
    """Base class for podium-supported DataFrame."""

    def __podium_config__(config: PodiumConfig) -> "DataFrame":
        """Configure dataframe."""
        pass
