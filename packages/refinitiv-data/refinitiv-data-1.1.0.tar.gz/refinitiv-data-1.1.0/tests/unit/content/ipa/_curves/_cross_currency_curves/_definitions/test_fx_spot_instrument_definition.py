from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FxSpotInstrumentDefinition,
)


def test_fx_spot_instrument_definition():
    # given
    expected_dict = {
        "instrumentCode": "string",
        "syntheticInstrumentCode": "string",
        "template": "string",
    }

    # when
    testing_obj = FxSpotInstrumentDefinition(
        instrument_code="string",
        synthetic_instrument_code="string",
        template="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.instrument_code == "string"
    assert testing_obj.synthetic_instrument_code == "string"
    assert testing_obj.template == "string"
