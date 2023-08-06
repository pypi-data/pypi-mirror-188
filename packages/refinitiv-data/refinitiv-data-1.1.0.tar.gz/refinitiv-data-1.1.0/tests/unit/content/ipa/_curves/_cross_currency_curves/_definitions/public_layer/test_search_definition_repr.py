from refinitiv.data.content.ipa.curves._cross_currency_curves.definitions import search


def test_search_definition_repr():
    # given
    definition = search.Definition()
    expected_value = (
        f"<refinitiv.data.content.ipa.curves._cross_currency_curves.definitions.search.Definition "
        f"object at {hex(id(definition))}>"
    )

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value
