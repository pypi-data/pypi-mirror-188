from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    FxForwardCurveParameters,
)
from refinitiv.data.content.ipa._enums._extrapolation_mode import ExtrapolationMode
from refinitiv.data.content.ipa._enums._interpolation_mode import InterpolationMode
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    ValuationTime,
)


def test_fx_forward_curve_parameters():
    # given
    expected_dict = {
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
    testing_obj = FxForwardCurveParameters(
        extrapolation_mode=ExtrapolationMode.CONSTANT,
        interpolation_mode=InterpolationMode.CUBIC_DISCOUNT,
        valuation_time=ValuationTime(),
        ignore_invalid_instrument=True,
        ignore_pivot_currency_holidays=True,
        use_delayed_data_if_denied=True,
        valuation_date="string",
        valuation_date_time="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.extrapolation_mode == ExtrapolationMode.CONSTANT
    assert testing_obj.interpolation_mode == InterpolationMode.CUBIC_DISCOUNT
    assert testing_obj.valuation_time == ValuationTime()
    assert testing_obj.ignore_invalid_instrument == True
    assert testing_obj.ignore_pivot_currency_holidays == True
    assert testing_obj.use_delayed_data_if_denied == True
    assert testing_obj.valuation_date == "string"
    assert testing_obj.valuation_date_time == "string"
