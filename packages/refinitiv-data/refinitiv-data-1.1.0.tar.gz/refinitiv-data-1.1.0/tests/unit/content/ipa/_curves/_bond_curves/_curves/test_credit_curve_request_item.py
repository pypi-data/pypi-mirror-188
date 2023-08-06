from refinitiv.data.content.ipa._curves._bond_curves import RequestItem
from refinitiv.data.content.ipa._curves._bond_curves._curves import (
    CreditCurveParameters,
    CreditCurveDefinition,
)
from refinitiv.data.content.ipa._curves._bond_curves._enums import (
    InterestCalculationMethod,
    BasisSplineSmoothModel,
    CalendarAdjustment,
    CalibrationModel,
    BusinessSector,
    CurveSubType,
    EconomicSector,
    Industry,
    IndustryGroup,
    IssuerType,
    MainConstituentAssetClass,
    Rating,
    RatingScaleSource,
    ReferenceEntityType,
    Seniority,
    InterpolationMode,
    PriceSide,
)
from refinitiv.data.content.ipa._curves._enums import CompoundingType
from refinitiv.data.content.ipa._enums._extrapolation_mode import ExtrapolationMode


def test_credit_curve_request_item():
    # given
    expected_curve_parameters = {
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

    expected_curve_definition = {
        "businessSector": "AcademicAndEducationalServices",
        "creditCurveTypeFallbackLogic": ["string1", "string2"],
        "curveSubType": "BondCarry",
        "curveTenors": ["string1", "string2"],
        "economicSector": "AcademicAndEducationalServices",
        "industry": "AdvancedMedicalEquipmentAndTechnology",
        "industryGroup": "AerospaceAndDefense",
        "issuerType": "Agency",
        "mainConstituentAssetClass": "Bond",
        "rating": "A",
        "ratingScaleSource": "DBRS",
        "referenceEntityType": "BondIsin",
        "seniority": "SeniorNonPreferred",
        "country": "string",
        "currency": "string",
        "id": "string",
        "name": "string",
        "referenceEntity": "string",
        "source": "string",
    }

    # when
    curve_definition = CreditCurveDefinition(
        business_sector=BusinessSector.ACADEMIC_AND_EDUCATIONAL_SERVICES,
        credit_curve_type_fallback_logic=["string1", "string2"],
        curve_sub_type=CurveSubType.BOND_CARRY,
        curve_tenors=["string1", "string2"],
        economic_sector=EconomicSector.ACADEMIC_AND_EDUCATIONAL_SERVICES,
        industry=Industry.ADVANCED_MEDICAL_EQUIPMENT_AND_TECHNOLOGY,
        industry_group=IndustryGroup.AEROSPACE_AND_DEFENSE,
        issuer_type=IssuerType.AGENCY,
        main_constituent_asset_class=MainConstituentAssetClass.BOND,
        rating=Rating.A,
        rating_scale_source=RatingScaleSource.DBRS,
        reference_entity_type=ReferenceEntityType.BOND_ISIN,
        seniority=Seniority.SENIOR_NON_PREFERRED,
        country="string",
        currency="string",
        id="string",
        name="string",
        reference_entity="string",
        source="string",
    )

    curve_parameters = CreditCurveParameters(
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

    # when
    testing_obj = RequestItem(
        curve_definition=curve_definition,
        curve_parameters=curve_parameters,
        curve_tag="curve_tag",
    )

    # then
    assert testing_obj.get_dict() == {
        "curveDefinition": expected_curve_definition,
        "curveParameters": expected_curve_parameters,
        "curveTag": "curve_tag",
    }

    assert testing_obj.curve_definition == curve_definition
    assert testing_obj.curve_parameters == curve_parameters
    assert testing_obj.curve_tag == "curve_tag"
