from refinitiv.data.content.ipa._curves._bond_curves._curves import (
    CreditCurveParameters,
)
from refinitiv.data.content.ipa._curves._bond_curves._enums import (
    InterestCalculationMethod,
    BasisSplineSmoothModel,
    CalendarAdjustment,
    CalibrationModel,
)
from refinitiv.data.content.ipa._curves._enums import CompoundingType
from refinitiv.data.content.ipa._enums._extrapolation_mode import ExtrapolationMode
from refinitiv.data.content.ipa._curves._bond_curves._enums import (
    InterpolationMode,
    PriceSide,
)


def test_credit_curve_parameters():
    # given
    expected_dict = {
        "interestCalculationMethod": "Dcb_30E_360_ISMA",
        "basisSplineSmoothModel": "AndersonSmoothingSplineModel",
        "calendarAdjustment": "Calendar",
        "calendars": ["string1", "string2"],
        "calibrationModel": "BasisSpline",
        "compoundingType": "Compounded",
        "extrapolationMode": "Constant",
        "interpolationMode": "AkimaMethod",
        "priceSide": "Ask",
        "basisSplineKnots": 10,
        "returnCalibratedParameters": True,
        "useDelayedDataIfDenied": True,
        "useDurationWeightedMinimization": True,
        "useMultiDimensionalSolver": True,
        "valuationDate": "string",
    }

    # when
    testing_obj = CreditCurveParameters(
        interest_calculation_method=InterestCalculationMethod.DCB_30_E_360_ISMA,
        basis_spline_smooth_model=BasisSplineSmoothModel.ANDERSON_SMOOTHING_SPLINE_MODEL,
        calendar_adjustment=CalendarAdjustment.CALENDAR,
        calendars=["string1", "string2"],
        calibration_model=CalibrationModel.BASIS_SPLINE,
        compounding_type=CompoundingType.COMPOUNDED,
        extrapolation_mode=ExtrapolationMode.CONSTANT,
        interpolation_mode=InterpolationMode.AKIMA_METHOD,
        price_side=PriceSide.ASK,
        basis_spline_knots=10,
        return_calibrated_parameters=True,
        use_delayed_data_if_denied=True,
        use_duration_weighted_minimization=True,
        use_multi_dimensional_solver=True,
        valuation_date="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert (
        testing_obj.interest_calculation_method
        == InterestCalculationMethod.DCB_30_E_360_ISMA
    )
    assert (
        testing_obj.basis_spline_smooth_model
        == BasisSplineSmoothModel.ANDERSON_SMOOTHING_SPLINE_MODEL
    )
    assert testing_obj.calendar_adjustment == CalendarAdjustment.CALENDAR
    assert testing_obj.calendars == ["string1", "string2"]
    assert testing_obj.calibration_model == CalibrationModel.BASIS_SPLINE
    assert testing_obj.compounding_type == CompoundingType.COMPOUNDED
    assert testing_obj.extrapolation_mode == ExtrapolationMode.CONSTANT
    assert testing_obj.interpolation_mode == InterpolationMode.AKIMA_METHOD
    assert testing_obj.price_side == PriceSide.ASK
    assert testing_obj.basis_spline_knots == 10
    assert testing_obj.return_calibrated_parameters == True
    assert testing_obj.use_delayed_data_if_denied == True
    assert testing_obj.use_duration_weighted_minimization == True
    assert testing_obj.use_multi_dimensional_solver == True
    assert testing_obj.valuation_date == "string"
