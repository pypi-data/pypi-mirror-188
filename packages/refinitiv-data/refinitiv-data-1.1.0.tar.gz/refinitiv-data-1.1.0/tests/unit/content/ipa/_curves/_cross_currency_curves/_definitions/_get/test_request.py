from refinitiv.data.content.ipa._curves._cross_currency_curves import (
    RiskType,
    MainConstituentAssetClass,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions._get import (
    CrossCurrencyCurveDefinitionKeys,
    GetRequest,
)


def test_cross_currency_curve_definition_keys():
    # given
    curve_definition = CrossCurrencyCurveDefinitionKeys(
        main_constituent_asset_class=MainConstituentAssetClass.FX_FORWARD,
        risk_type=RiskType.CROSS_CURRENCY,
        base_currency="string",
        base_index_name="string",
        id="string",
        is_non_deliverable=True,
        name="string",
        quoted_currency="string",
        quoted_index_name="string",
        source="string",
    )

    # when
    testing_obj = GetRequest(curve_definition=curve_definition)

    # then
    assert testing_obj.get_dict() == {"curveDefinition": curve_definition}

    assert testing_obj.curve_definition == curve_definition
