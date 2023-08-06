from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    CrossCurrencyCurveDefinitionPricing,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves._enums import (
    ConstituentOverrideMode,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._enums import (
    MainConstituentAssetClass,
    RiskType,
)


def test_cross_currency_curve_definition_pricing():
    # given
    expected_dict = {
        "constituentOverrideMode": "MergeWithDefinition",
        "mainConstituentAssetClass": "FxForward",
        "riskType": "CrossCurrency",
        "baseCurrency": "string",
        "baseIndexName": "string",
        "id": "string",
        "ignoreExistingDefinition": True,
        "isNonDeliverable": True,
        "name": "string",
        "quotedCurrency": "string",
        "quotedIndexName": "string",
        "source": "string",
    }

    # when
    testing_obj = CrossCurrencyCurveDefinitionPricing(
        constituent_override_mode=ConstituentOverrideMode.MERGE_WITH_DEFINITION,
        main_constituent_asset_class=MainConstituentAssetClass.FX_FORWARD,
        risk_type=RiskType.CROSS_CURRENCY,
        base_currency="string",
        base_index_name="string",
        id="string",
        ignore_existing_definition=True,
        is_non_deliverable=True,
        name="string",
        quoted_currency="string",
        quoted_index_name="string",
        source="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert (
        testing_obj.constituent_override_mode
        == ConstituentOverrideMode.MERGE_WITH_DEFINITION
    )
    assert (
        testing_obj.main_constituent_asset_class == MainConstituentAssetClass.FX_FORWARD
    )
    assert testing_obj.risk_type == RiskType.CROSS_CURRENCY
    assert testing_obj.base_currency == "string"
    assert testing_obj.base_index_name == "string"
    assert testing_obj.id == "string"
    assert testing_obj.ignore_existing_definition == True
    assert testing_obj.is_non_deliverable == True
    assert testing_obj.name == "string"
    assert testing_obj.quoted_currency == "string"
    assert testing_obj.quoted_index_name == "string"
    assert testing_obj.source == "string"
