import narwhals as nw

from podium_lib.dataframe.config import PodiumConfig


class PodiumDataFrame(nw.DataFrame):
    """Base class for podium-supported DataFrame."""

    def __podium_config__(config: PodiumConfig) -> "PodiumDataFrame":
        """Configure dataframe."""
        pass
