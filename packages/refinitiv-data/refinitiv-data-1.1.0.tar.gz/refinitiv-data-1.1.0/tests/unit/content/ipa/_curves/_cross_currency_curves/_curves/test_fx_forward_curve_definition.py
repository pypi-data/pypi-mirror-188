from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    FxForwardCurveDefinition,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    CrossCurrencyCurveDefinitionPricing,
)
from refinitiv.data.content.ipa._curves import ZcCurveDefinition


def test_fx_forward_curve_definition():
    # given
    expected_dict = {
        "baseCurrency": "string",
        "baseIndexName": "string",
        "crossCurrencyDefinitions": [{}],
        "curveTenors": ["string1", "string2"],
        "interestRateCurveDefinitions": [{}],
        "isNonDeliverable": True,
        "pivotCurrency": "string",
        "pivotIndexName": "string",
        "quotedCurrency": "string",
        "quotedIndexName": "string",
    }

    # when
    testing_obj = FxForwardCurveDefinition(
        cross_currency_definitions=[CrossCurrencyCurveDefinitionPricing()],
        curve_tenors=["string1", "string2"],
        interest_rate_curve_definitions=[ZcCurveDefinition()],
        base_currency="string",
        base_index_name="string",
        is_non_deliverable=True,
        pivot_currency="string",
        pivot_index_name="string",
        quoted_currency="string",
        quoted_index_name="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.cross_currency_definitions == [
        CrossCurrencyCurveDefinitionPricing()
    ]
    assert testing_obj.curve_tenors == ["string1", "string2"]
    assert testing_obj.interest_rate_curve_definitions == [ZcCurveDefinition()]
    assert testing_obj.base_currency == "string"
    assert testing_obj.base_index_name == "string"
    assert testing_obj.is_non_deliverable is True
    assert testing_obj.pivot_currency == "string"
    assert testing_obj.pivot_index_name == "string"
    assert testing_obj.quoted_currency == "string"
    assert testing_obj.quoted_index_name == "string"
