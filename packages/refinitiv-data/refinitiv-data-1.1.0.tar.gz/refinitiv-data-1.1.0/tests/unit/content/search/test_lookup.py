from refinitiv.data.content.search import lookup


def test_workspace():
    assert hasattr(lookup, "Definition")


def test_attributes():
    # given
    excepted_attributes = [
        "_view",
        "_select",
        "_scope",
        "_terms",
        "_extended_params",
        #
        "_kwargs",
        "_data_type",
        "_content_type",
        "_provider",
    ]

    # when
    definition = lookup.Definition(view=..., scope="", terms="", select="")
    attributes = list(definition.__dict__.keys())

    # then
    assert len(attributes) == len(excepted_attributes)
    assert set(attributes) == set(excepted_attributes)


def test_definition_lookup_repr():
    # given
    definition = lookup.Definition(view=..., scope="", terms="", select="")
    obj_id = hex(id(definition))
    expected_value = f"<refinitiv.data.content.search.lookup.Definition object at {obj_id} {{view='Ellipsis', terms='', scope='', select=''}}>"

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value
