# Podium

Class-based data-expression framework.

## Installation

```bash
# with Astral uv
uv pip install podium-lib

# with pip
pip install podium-lib

# get latest version
git clone https://github.com/lucas-nelson-uiuc/podium-lib.git
```

## Getting Started

```python
import podium_lib
from podium_lib import Model, Field

housing_data = podium_lib.load("california_housing") # TODO: support this method


# create your first class
class CaliforniaHousing(Model):
    latitude: float
    longitude: float

print(CaliforniaHousing.schema())


# add converters and validators to your fields
from podium_lib import validators as pv, converters as pc

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

Podium has a few simple - yet powerful - goals in mind:
- Reduce the need to know how to interact with data objects (e.g. DataFrame APIs)
- Simplify the ability to express expectations of your data objects

## Inspiration

The name of this package came about in the following manner:
- This package implements `narwhals` - a group of narwhals is considered a **pod**
- This package is an opinionated workflow orchestrator, so a podium seems a
fitting environment to share these opinions
