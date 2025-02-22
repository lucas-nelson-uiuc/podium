# Podium

Class-based workflow constructor.

## Example

*In theory*, Podium aims to reduce the need to know a DataFrame's API to express
your expectations of a data object.

Say you need to create a column that assigns a default value.

```python
import polars as pl
from pyspark.sql import functions as F, types as T

# with polars
data.with_columns(
    today=pl.lit(datetime.date.today()),
    fruit=pl.when(pl.col('fruit').is_null()).then('apple').otherwise('banana'),
    units_sold=pl.col('fruit').count().cast(pl.Int64),
)

# with pyspark
data.withColumns({
    "today": F.lit(datetime.date.today()),
    "fruit": F.when(F.col("fruit").isNull(), F.lit("apple")).otherwise(F.lit("banana")),
    "units_sold": F.col("fruit").count().cast(T.IntegerType())
})
```

Podium removes the complexity of creating these fields:

```python
# with Podium (narwhals)
from dataclasses import dataclass
from podium import Model, Field


class FruitMarket(Model):
    today: datetime.date = PodiumField(default=datetime.date.today())
    fruit: str = PodiumField(default="apple")
    units_sold: int = PodiumField(converter=nw.col("fruit").count())
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
