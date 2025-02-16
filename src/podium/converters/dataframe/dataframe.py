from podium.converters._classes import DataFrameConverter
from podium.converters.dataframe import _queries


drop_nulls = DataFrameConverter(name="Drop Nulls", converter=_queries.drop_nulls)

unique = DataFrameConverter(name="Unique Values", converter=_queries.unique)
