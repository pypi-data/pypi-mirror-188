from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    CrossCurrencyCurveParameters,
)
from refinitiv.data.content.ipa._enums._extrapolation_mode import ExtrapolationMode
from refinitiv.data.content.ipa._curves._cross_currency_curves._enums import (
    InterpolationMode,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    TurnAdjustment,
)


def test_cross_currency_curve_parameters():
    # given
    expected_dict = {
        "extrapolationMode": "Constant",
        "interpolationMode": "CubicSpline",
        "turnAdjustment": {},
    }

    # when
    testing_obj = CrossCurrencyCurveParameters(
        extrapolation_mode=ExtrapolationMode.CONSTANT,
        interpolation_mode=InterpolationMode.CUBIC_SPLINE,
        turn_adjustment=TurnAdjustment(),
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.extrapolation_mode == ExtrapolationMode.CONSTANT
    assert testing_obj.interpolation_mode == InterpolationMode.CUBIC_SPLINE
    assert testing_obj.turn_adjustment == TurnAdjustment()
