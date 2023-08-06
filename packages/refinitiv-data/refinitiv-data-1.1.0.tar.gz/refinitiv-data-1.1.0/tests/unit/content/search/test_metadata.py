from refinitiv.data.content.search import metadata


def test_workspace():
    assert hasattr(metadata, "Definition")


def test_attributes():
    # given
    excepted_attributes = [
        "_view",
        #
        "_kwargs",
        "_data_type",
        "_content_type",
        "_provider",
    ]

    # when
    definition = metadata.Definition(view=...)
    attributes = list(definition.__dict__.keys())

    # then
    assert len(attributes) == len(excepted_attributes)
    assert set(attributes) == set(excepted_attributes)


def test_definition_metadata_repr():
    # given
    definition = metadata.Definition(view=...)
    obj_id = hex(id(definition))
    expected_value = f"<refinitiv.data.content.search.metadata.Definition object at {obj_id} {{view='Ellipsis'}}>"

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value
