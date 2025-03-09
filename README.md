# Podium

Class-based data-expression framework.

## Installation

```bash
# with Astral uv
uv pip install podium

# with pip
pip install podium

# get latest version
git clone https://github.com/lucas-nelson-uiuc/podium.git
```

## Getting Started

```python
from podium import Model, Field

housing_data = podium.load("california_housing") # TODO: support this method


# create your first class
class CaliforniaHousing(Model):
    latitude: float
    longitude: float

print(CaliforniaHousing.schema())


# add converters and validators to your fields
from podium import validators as pv, converters as pc

class CaliforniaHousing(Model):
    latitude: float = Field(
        converter=pc.field.round(0),
        validator=pv.field.between(32, 42)
    )
    longitude: float = Field(
        converter=pc.field.round(0),
        validator=pv.field.between(114, 124)
    )

print(CaliforniaHousing.workflow())
CaliforniaHousing.validate(housing_data)
```

## Why Podium?

*In theory*, Podium aims to reduce the need to know a DataFrame's API to express
your expectations of a data object.

Say you need to create a column that assigns a default value.

```python
import polars as pl
from pyspark.sql import functions as F, types as T

# with polars
data.with_columns(
    minimal_field=pl.lit("Minimal Value"),
    another_minimal_field=pl.col("amf").fill_null("Missing Value"),
    complex_field=pl.col("not_so_minimal_field").str.to_lowercase(),
)
assert data.filter(~pl.col("complex_field").str.matches(r"^[a-z]{8}$")).is_empty()
assert data.filter(~pl.col("complex_field").unique()).is_empty()

# with pyspark
data.withColumns({
    "minimal_field": F.lit("Minimal Value"),
    "another_minimal_field": F.when(F.col("amf").isNull(), F.lit("Missing Value")).otherwise(F.col("amf")),
    "complex_field": F.lower(F.col("not_so_minimal_field"))
})
assert data.filter(~F.col("complex_field").rlike(r"^[a-z]{8}$")).isEmpty()
assert data.groupby("complex_field").count().filter(F.col("count") > 1).isEmpty()
```

Podium removes the complexity of constructing fields by providing an expressive,
class-based framework that handles the implementation for you. All you need to
do is specify your expectations of your DataFrame:

```python
# with Podium (narwhals)
from podium import Model, Field, converter, validator


class TemplateModel(Model):
    # some fields require minimal expectations
    minimal_field: str = Field(default="Minimal Value")
    amf: str = Field(alias="another_minimal_field", default="Missing Value")
    # other fields require more-than-minimal expectations
    not_so_minimal_field: str = Field(
        alias="complex_field",
        converter=converter.field.to_lowercase,
        validator=(
            validator.field.matches_pattern.bind(pattern=r"^[a-z]{8}$"),
            validator.field.unique_values,
        ),
    )
```

To apply your schema against a data object, simply call:

```python
# convert all fields in data according to model
Sample.convert(data)

# validate all fields in data according to model
Sample.validate(data)
```

## Inspiration

The name of this package came about in the following manner:
- This package implements `narwhals` - a group of narwhals is considered a **pod**
- This package is an opinionated workflow orchestrator, so a podium seems a
fitting environment to share these opinions
