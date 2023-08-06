from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    CrossCurrencyInstrumentDefinition,
)


def test_cross_currency_instrument_definition():
    # given
    expected_dict = {
        "instrumentCode": "string",
        "tenor": "string",
        "isNonDeliverable": True,
        "syntheticInstrumentCode": "string",
        "template": "string",
    }

    # when
    testing_obj = CrossCurrencyInstrumentDefinition(
        instrument_code="string",
        tenor="string",
        is_non_deliverable=True,
        synthetic_instrument_code="string",
        template="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.instrument_code == "string"
    assert testing_obj.tenor == "string"
    assert testing_obj.is_non_deliverable is True
    assert testing_obj.synthetic_instrument_code == "string"
    assert testing_obj.template == "string"
