import string
from podium_lib import describe

import pytest


class TestDescribe:
    """Test describe module."""

    @pytest.mark.parametrize(
        "template,expected",
        [
            ("Increment number by 10", []),
            ("Increment number by $increment", ["increment"]),
            (
                "Increment number by $increment and $scale",
                ["increment", "scale"],
            ),
            ("Increment number by $$not_a_variable", []),
            ("Cost is $$$price", ["price"]),
            ("Name: $$first, Value: $value", ["value"]),
            ("Value: $var and $Var", ["var", "Var"]),
            ("Hello ${name}", ["name"]),
            ("Hello ${first_name} and ${lastName}", ["first_name", "lastName"]),
            (
                "Path: $$HOME/$USER",
                ["USER"],
            ),
        ],
    )
    def test_get_identifiers(
        self,
        template: str,
        expected: list[str],
    ):
        """Test identifier extraction."""
        template = string.Template(template)
        identifiers = describe.get_identifiers(template)
        assert set(identifiers).difference(expected) == set()

    @pytest.mark.parametrize(
        "template,parameters,expected",
        [
            (
                "Increment number by $increment",
                dict(),
                "Increment number by $increment",
            ),
            (
                "Increment number by $increment",
                dict(random=11),
                "Increment number by $increment",
            ),
            (
                "Increment number by $increment",
                dict(increment=10),
                "Increment number by 10",
            ),
            (
                "Increment number by $increment and $scale",
                dict(increment=10, scale=4),
                "Increment number by 10 and 4",
            ),
        ],
    )
    def test_description_update(
        self,
        template: str,
        parameters: dict,
        expected: str,
    ):
        """Test description update."""
        updated_template = describe.update_description(template, **parameters)
        assert updated_template == expected
