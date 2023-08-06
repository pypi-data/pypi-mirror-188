from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FxForwardInstrumentDefinition,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions._enums import (
    QuotationMode,
)


def test_fx_forward_instrument_definition():
    # given
    expected_dict = {
        "instrumentCode": "string",
        "tenor": "string",
        "quotationMode": "Outright",
        "isNonDeliverable": True,
        "syntheticInstrumentCode": "string",
        "template": "string",
    }

    # when
    testing_obj = FxForwardInstrumentDefinition(
        instrument_code="string",
        tenor="string",
        quotation_mode=QuotationMode.OUTRIGHT,
        is_non_deliverable=True,
        synthetic_instrument_code="string",
        template="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.instrument_code == "string"
    assert testing_obj.tenor == "string"
    assert testing_obj.quotation_mode == QuotationMode.OUTRIGHT
    assert testing_obj.is_non_deliverable is True
    assert testing_obj.synthetic_instrument_code == "string"
    assert testing_obj.template == "string"
