from podium.validators._classes import DataFrameValidator, RelationshipValidator
from podium.validators.dataframe import _predicates


duplicate_rows = DataFrameValidator(
    name="Duplicate Observations",
    description=_predicates.is_duplicated.__doc__,
    validator=_predicates.is_duplicated,
)

unique_rows = DataFrameValidator(
    name="Unique Observations",
    description=_predicates.is_unique.__doc__,
    validator=_predicates.is_unique,
)

one_to_one_relationship = RelationshipValidator(
    name="One-to-One Relationship",
    description=_predicates.is_one_to_one.__doc__,
    validator=_predicates.is_one_to_one,
)

one_to_many_relationship = RelationshipValidator(
    name="One-to-Many Relationship",
    description=_predicates.is_one_to_many.__doc__,
    validator=_predicates.is_one_to_many,
)

many_to_one_relationship = RelationshipValidator(
    name="Many-to-One Relationship",
    description=_predicates.is_many_to_one.__doc__,
    validator=_predicates.is_many_to_one,
)
