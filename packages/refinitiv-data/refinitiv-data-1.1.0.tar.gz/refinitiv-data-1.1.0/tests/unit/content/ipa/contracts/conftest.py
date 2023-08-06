def has_property_names_in_class(cls, expected_property_names):
    if isinstance(expected_property_names, dict):
        expected_property_names = list(expected_property_names.keys())
    return set(get_property_names(cls)) == set(expected_property_names)


def get_property_names(cls):
    return [p for p in dir(cls) if isinstance(getattr(cls, p, None), property)]
