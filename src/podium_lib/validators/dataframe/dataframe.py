from podium_lib.validators._classes import DataFrameValidator, RelationshipValidator
from podium_lib.validators.dataframe import _predicates


duplicate_rows = DataFrameValidator(
    name="Duplicate Observations",
    validator=_predicates.is_duplicated,
)

unique_rows = DataFrameValidator(
    name="Unique Observations",
    validator=_predicates.is_unique,
)

one_to_one_relationship = RelationshipValidator(
    name="One-to-One Relationship",
    validator=_predicates.is_one_to_one,
)

one_to_many_relationship = RelationshipValidator(
    name="One-to-Many Relationship",
    validator=_predicates.is_one_to_many,
)

many_to_one_relationship = RelationshipValidator(
    name="Many-to-One Relationship",
    validator=_predicates.is_many_to_one,
)
