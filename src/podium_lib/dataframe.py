from dataclasses import dataclass, field

import narwhals as nw


@dataclass
class DataFrame:
    """Base class for Podium DataFrame."""

    _data: nw.DataFrame
    config: dict

    def data(self):
        """Return internal dataframe."""
        return self._data
