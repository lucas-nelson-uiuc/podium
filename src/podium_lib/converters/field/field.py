from podium_lib.converters._classes import FieldConverter
from podium_lib.converters.field import _queries


replace = FieldConverter(
    name="Replace Values",
    converter=_queries.replace,
)

replace_all = FieldConverter(
    name="Replace All Values",
    converter=_queries.replace_all,
)

to_datetime = FieldConverter(
    name="Cast Datetime",
    converter=_queries.to_datetime,
)

to_lowercase = FieldConverter(
    name="Convert to Lowercase",
    converter=_queries.to_lowercase,
)

to_uppercase = FieldConverter(
    name="Convert to Uppercase",
    converter=_queries.to_uppercase,
)
