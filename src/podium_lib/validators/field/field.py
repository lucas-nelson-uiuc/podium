from podium_lib.validators._classes import FieldValidator
from podium_lib.validators.field import _predicates


between_values = FieldValidator(
    name="Within Range",
    validator=_predicates.is_between,
)

duplicate_values = FieldValidator(
    name="Duplicate Values",
    validator=_predicates.is_duplicate,
)

finite_values = FieldValidator(
    name="Finite Values",
    validator=_predicates.is_finite,
)

contains_values = FieldValidator(
    name="Contains Values",
    validator=_predicates.is_in,
)

nan_values = FieldValidator(
    name="NaN Values",
    validator=_predicates.is_nan,
)

null_values = FieldValidator(
    name="Null Values",
    validator=_predicates.is_null,
)

unique_values = FieldValidator(
    name="Distinct Values",
    validator=_predicates.is_unique,
)


matches_pattern = FieldValidator(
    name="Matches Pattern",
    validator=_predicates.matches_pattern,
)

matches_suffix = FieldValidator(
    name="Matches Suffix",
    validator=_predicates.ends_with,
)

matches_prefix = FieldValidator(
    name="Matches Prefix",
    validator=_predicates.starts_with,
)

min_length = FieldValidator(
    name="Minimum Length",
    validator=_predicates.min_length,
)

max_length = FieldValidator(
    name="Maximum Length",
    validator=_predicates.max_length,
)
