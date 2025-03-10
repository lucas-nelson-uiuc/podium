import narwhals as nw
from typing import Callable
import pytest
from podium_lib import validators as pv
from podium_lib.validators._classes import Validator


class TestValidator:
    """Base class for testing field validator."""

    def test_initialization(self):
        """Test initialization."""
        Validator(name="Test Validator", validator=lambda x: True)
        Validator(
            name="Test Validator",
            validator=lambda x: True,
            description="Test description",
        )
        assert True

    @pytest.mark.parametrize(
        "validator,parameters,expected_description",
        [
            (
                pv.field.between_values,
                {"lower_bound": 1, "upper_bound": 2},
                "Check that column contains values between 1 and 2 (bounded both).",
            )
        ],
    )
    def test_description_update(
        self, validator: Validator, parameters: dict, expected_description: str
    ):
        """Test description update."""
        bound_validator = validator.bind(**parameters)
        assert bound_validator.description == expected_description
        assert isinstance(bound_validator, Validator)
        assert isinstance(bound_validator.validator, Callable)
