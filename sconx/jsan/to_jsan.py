def dict_to_jsan(obj):
    attrs = sorted(obj.keys())
    return list(map(lambda attr_name: to_jsan(obj[attr_name]), attrs))


def to_jsan(values):
    if isinstance(values, list):
        return list(map(to_jsan, values))
    if isinstance(values, dict):
        return dict_to_jsan(values)
    return values
