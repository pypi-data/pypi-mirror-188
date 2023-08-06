from refinitiv.data.content.ipa._curves._cross_currency_curves import (
    MainConstituentAssetClass,
    RiskType,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions._update import (
    CrossCurrencyCurveUpdateDefinition,
)


def test_cross_currency_curve_update_definition():
    # given
    expected_dict = {
        "id": "string",
        "mainConstituentAssetClass": "FxForward",
        "riskType": "CrossCurrency",
        "baseCurrency": "string",
        "baseIndexName": "string",
        "definitionExpiryDate": "string",
        "isFallbackForFxCurveDefinition": True,
        "isNonDeliverable": True,
        "name": "string",
        "quotedCurrency": "string",
        "quotedIndexName": "string",
        "source": "string",
    }

    # when
    testing_obj = CrossCurrencyCurveUpdateDefinition(
        id="string",
        main_constituent_asset_class=MainConstituentAssetClass.FX_FORWARD,
        risk_type=RiskType.CROSS_CURRENCY,
        base_currency="string",
        base_index_name="string",
        definition_expiry_date="string",
        is_fallback_for_fx_curve_definition=True,
        is_non_deliverable=True,
        name="string",
        quoted_currency="string",
        quoted_index_name="string",
        source="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.id == "string"
    assert (
        testing_obj.main_constituent_asset_class == MainConstituentAssetClass.FX_FORWARD
    )
    assert testing_obj.risk_type == RiskType.CROSS_CURRENCY
    assert testing_obj.base_currency == "string"
    assert testing_obj.base_index_name == "string"
    assert testing_obj.definition_expiry_date == "string"
    assert testing_obj.is_fallback_for_fx_curve_definition == True
    assert testing_obj.is_non_deliverable == True
    assert testing_obj.name == "string"
    assert testing_obj.quoted_currency == "string"
    assert testing_obj.quoted_index_name == "string"
    assert testing_obj.source == "string"
