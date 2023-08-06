from refinitiv.data.content.ipa._curves import ZcCurveDefinition
from refinitiv.data.content.ipa._curves._cross_currency_curves import (
    FxForwardCurveDefinition,
    CrossCurrencyCurveDefinitionPricing,
    FxShiftScenario,
    ShiftDefinition,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    FxForwardCurveParameters,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves._request import (
    RequestItem,
)
from refinitiv.data.content.ipa._enums._extrapolation_mode import ExtrapolationMode
from refinitiv.data.content.ipa._enums._interpolation_mode import InterpolationMode
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    ValuationTime,
)


def test_fx_forward_curves_request_item():
    # given
    expected_curve_definition = {
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

    curve_definition = FxForwardCurveDefinition(
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

    expected_curve_parameters = {
        "extrapolationMode": "Constant",
        "ignoreInvalidInstrument": True,
        "ignorePivotCurrencyHolidays": True,
        "interpolationMode": "CubicDiscount",
        "useDelayedDataIfDenied": True,
        "valuationDate": "string",
        "valuationDateTime": "string",
        "valuationTime": {},
    }

    # when
    curve_parameters = FxForwardCurveParameters(
        extrapolation_mode=ExtrapolationMode.CONSTANT,
        interpolation_mode=InterpolationMode.CUBIC_DISCOUNT,
        valuation_time=ValuationTime(),
        ignore_invalid_instrument=True,
        ignore_pivot_currency_holidays=True,
        use_delayed_data_if_denied=True,
        valuation_date="string",
        valuation_date_time="string",
    )

    expected_shift_scenarios = {"fxCurveShift": {}, "shiftTag": "string"}

    # when
    shift_scenarios = FxShiftScenario(
        fx_curve_shift=ShiftDefinition(),
        shift_tag="string",
    )

    # when
    testing_obj = RequestItem(
        curve_definition=curve_definition,
        curve_parameters=curve_parameters,
        shift_scenarios=[shift_scenarios],
        curve_tag="curve_tag",
    )

    # then
    assert testing_obj.get_dict() == {
        "curveDefinition": expected_curve_definition,
        "curveParameters": expected_curve_parameters,
        "shiftScenarios": [expected_shift_scenarios],
        "curveTag": "curve_tag",
    }

    assert testing_obj.curve_tag == "curve_tag"
