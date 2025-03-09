# Podium

Class-based data-expression framework.

## Example

*In theory*, Podium aims to reduce the need to know a DataFrame's API to express
your expectations of a data object.

Say you need to create a column that assigns a default value.

```python
import polars as pl
from pyspark.sql import functions as F, types as T

# with polars
data.with_columns(
    minimal_field=pl.lit("Minimal Value"),
    another_minimal_field=pl.when(pl.col("amf").is_null()).then('Another Minimal Value').otherwise(pl.col("amf")),
    complex_field=pl.col("not_so_minimal_field").str.to_lowercase(),
)
assert data.filter(~pl.col("complex_field").str.matches(r"^[a-z]{8}$")).is_empty()
assert data.filter(~pl.col("complex_field").unique()).is_empty()

# with pyspark
data.withColumns({
    "minimal_field": F.lit("Minimal Value"),
    "another_minimal_field": F.when(F.col("amf").isNull(), F.lit("Another Minimal Value")).otherwise(F.col("amf")),
    "complex_field": F.lower(F.col("not_so_minimal_field"))
})
assert data.filter(~F.col("complex_field").rlike(r"^[a-z]{8}$")).isEmpty()
assert data.groupby("complex_field").count().filter(F.col("count") > 1).isEmpty()
```

Podium removes the complexity of creating these fields:

```python
# with Podium (narwhals)
from podium import Model, Field, converter, validator


@dataclass
class TemplateModel(Model):
    # some fields require minimal expectations
    minimal_field: str = Field(default="Minimal Value")
    amf: str = Field(alias="another_minimal_field", default="Another Minimal Value")
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
