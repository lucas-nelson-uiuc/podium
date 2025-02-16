import narwhals as nw


def _as_schema(schema):
    if isinstance(schema, nw.Schema):
        return schema
    if isinstance(schema, nw.DataFrame):
        return schema.schema
    raise ValueError("Unable to extract schema from object.")
