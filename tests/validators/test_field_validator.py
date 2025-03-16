import narwhals as nw
from typing import Callable
import pytest
from podium_lib import validators as pv
from podium_lib.validators import FieldValidator


class TestFieldValidator:
    """Base class for testing field validator."""

    @pytest.mark.parametrize(
        "instance,parameters",
        [
            (
                pv.field.between_values,
                {"lower_bound": 1, "upper_bound": 2},
            ),
            (pv.field.duplicate_values, None),
        ],
    )
    def test_construction(self, instance: FieldValidator, parameters: dict):
        """Test construction."""
        if parameters is not None:
            instance = instance.bind(**parameters)
        assert isinstance(instance.construct("test").validator, nw.Expr)
