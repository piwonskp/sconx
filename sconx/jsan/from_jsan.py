import functools


def reconstruct_array(schema, values):
    return map(functools.partial(from_jsan, schema["items"]), values)


def reconstruct_dict(schema, values):
    props = schema["properties"]
    keys = sorted(props.keys())

    kv = zip(keys, values)
    attributes = map(lambda tup: from_jsan(props[tup[0]], tup[1]), kv)

    return dict(zip(keys, attributes))


def from_jsan(schema, values):
    val_type = schema.get("type")
    if val_type == "object" or schema.get("properties"):
        return reconstruct_dict(schema, values)
    if val_type == "array":
        return reconstruct_array(schema, values)
    return values
