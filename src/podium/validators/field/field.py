from podium.validators._classes import FieldValidator
from podium.validators.field import _predicates


between_values = FieldValidator(
    name="Within Range",
    description=_predicates.is_between.__doc__,
    validator=_predicates.is_between,
)

duplicate_values = FieldValidator(
    name="Duplicate Values",
    description=_predicates.is_duplicate.__doc__,
    validator=_predicates.is_duplicate,
)

finite_values = FieldValidator(
    name="Finite Values",
    description=_predicates.is_finite.__doc__,
    validator=_predicates.is_finite,
)

contains_values = FieldValidator(
    name="Contains Values",
    description=_predicates.is_in.__doc__,
    validator=_predicates.is_in,
)

nan_values = FieldValidator(
    name="NaN Values",
    description=_predicates.is_nan.__doc__,
    validator=_predicates.is_nan,
)

null_values = FieldValidator(
    name="Null Values",
    description=_predicates.is_null.__doc__,
    validator=_predicates.is_null,
)

unique_values = FieldValidator(
    name="Distinct Values",
    description=_predicates.is_unique.__doc__,
    validator=_predicates.is_unique,
)


matches_pattern = FieldValidator(
    name="Matches Pattern",
    description=_predicates.matches_pattern.__doc__,
    validator=_predicates.matches_pattern,
)

matches_suffix = FieldValidator(
    name="Matches Suffix",
    description=_predicates.ends_with.__doc__,
    validator=_predicates.ends_with,
)

matches_prefix = FieldValidator(
    name="Matches Prefix",
    description=_predicates.starts_with.__doc__,
    validator=_predicates.starts_with,
)

min_length = FieldValidator(
    name="Minimum Length",
    description=_predicates.min_length.__doc__,
    validator=_predicates.min_length,
)

max_length = FieldValidator(
    name="Maximum Length",
    description=_predicates.max_length.__doc__,
    validator=_predicates.max_length,
)
