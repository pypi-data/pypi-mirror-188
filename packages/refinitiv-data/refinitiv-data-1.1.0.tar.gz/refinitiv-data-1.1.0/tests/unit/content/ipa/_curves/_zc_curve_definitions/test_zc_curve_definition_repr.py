from refinitiv.data.content.ipa.curves import zc_curve_definitions


def test_zc_curves_definitions_repr():
    # given
    definition = zc_curve_definitions.Definitions(universe=[])
    expected_value = (
        f"<refinitiv.data.content.ipa.curves.zc_curve_definitions.Definitions "
        f"object at {hex(id(definition))}>"
    )

    # when
    testing_value = repr(definition)

    # then
    assert testing_value == expected_value
