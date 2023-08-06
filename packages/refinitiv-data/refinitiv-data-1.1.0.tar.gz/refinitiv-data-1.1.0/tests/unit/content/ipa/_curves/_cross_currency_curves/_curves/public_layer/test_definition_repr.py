from refinitiv.data.content.ipa.curves._cross_currency_curves import curves


def test_definition_repr():
    # given
    definition = curves.Definition()
    expected_value = (
        f"<refinitiv.data.content.ipa.curves._cross_currency_curves.curves.Definition "
        f"object at {hex(id(definition))}>"
    )

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value
