from refinitiv.data.content.ipa._curves._cross_currency_curves import (
    MainConstituentAssetClass,
    RiskType,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions._search import (
    CrossCurrencyCurveGetDefinitionItem,
)


def test_cross_currency_curve_get_definition_item():
    # given
    expected_dict = {
        "mainConstituentAssetClass": "FxForward",
        "riskType": "CrossCurrency",
        "baseCurrency": "string",
        "baseIndexName": "string",
        "curveTag": "string",
        "id": "string",
        "isNonDeliverable": True,
        "name": "string",
        "quotedCurrency": "string",
        "quotedIndexName": "string",
        "source": "string",
        "valuationDate": "string",
    }

    # when
    testing_obj = CrossCurrencyCurveGetDefinitionItem(
        main_constituent_asset_class=MainConstituentAssetClass.FX_FORWARD,
        risk_type=RiskType.CROSS_CURRENCY,
        base_currency="string",
        base_index_name="string",
        curve_tag="string",
        id="string",
        is_non_deliverable=True,
        name="string",
        quoted_currency="string",
        quoted_index_name="string",
        source="string",
        valuation_date="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert (
        testing_obj.main_constituent_asset_class == MainConstituentAssetClass.FX_FORWARD
    )
    assert testing_obj.risk_type == RiskType.CROSS_CURRENCY
    assert testing_obj.base_currency == "string"
    assert testing_obj.base_index_name == "string"
    assert testing_obj.curve_tag == "string"
    assert testing_obj.id == "string"
    assert testing_obj.is_non_deliverable == True
    assert testing_obj.name == "string"
    assert testing_obj.quoted_currency == "string"
    assert testing_obj.quoted_index_name == "string"
    assert testing_obj.source == "string"
    assert testing_obj.valuation_date == "string"
