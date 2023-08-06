import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data.content.ipa._curves._curves_data_provider import (
    get_curves_maker,
    CurvesResponseFactory,
    forward_curve_build_df,
)
from refinitiv.data.delivery._data._data_provider import ParsedData
from tests.unit.content.ipa._curves.conftest import (
    zc_curves_json,
    forward_curves_json,
    zc_curve_definitions_json,
)


@pytest.mark.parametrize(
    "input_value", [ContentType.FORWARD_CURVE, ContentType.ZC_CURVES]
)
def test_get_curves_maker(input_value):
    # when
    testing_value = get_curves_maker(input_value)

    # then
    assert testing_value is not None


def test_get_curves_maker_will_raise_exception_if_invalid_value():
    # given
    input_value = None

    # then
    with pytest.raises(ValueError):
        # when
        get_curves_maker(input_value)


def test_create_forward_curves():
    # given
    create_forward_curves = get_curves_maker(ContentType.FORWARD_CURVE)

    # when
    curves = create_forward_curves(forward_curves_json)

    # then
    assert len(curves) > 1


def test_forward_curve_build_df():
    # given
    input_raw = {
        "data": [
            {
                "error": {
                    "id": "b6f9797d-72c8-4baa-84eb-6a079fc40ec5/b6f9797d-72c8-4baa-84eb-6a079fc40ec5",
                    "code": "QPS-Curves.6",
                    "message": "Invalid input: curveDefinition is missing",
                }
            },
            {
                "curveTag": "test_curve",
                "curveParameters": {
                    "interestCalculationMethod": "Dcb_Actual_Actual",
                    "priceSide": "Mid",
                    "calendarAdjustment": "Calendar",
                    "calendars": ["EMU_FI"],
                    "compoundingType": "Compounded",
                    "useConvexityAdjustment": True,
                    "useSteps": False,
                    "valuationDate": "2022-02-09",
                },
                "curveDefinition": {
                    "availableTenors": ["OIS", "1M", "3M", "6M", "1Y"],
                    "availableDiscountingTenors": ["OIS", "1M", "3M", "6M", "1Y"],
                    "currency": "EUR",
                    "mainConstituentAssetClass": "Swap",
                    "riskType": "InterestRate",
                    "indexName": "EURIBOR",
                    "source": "Refinitiv",
                    "name": "EUR EURIBOR Swap ZC Curve",
                    "id": "9d619112-9ab3-45c9-b83c-eb04cbec382e",
                    "discountingTenor": "OIS",
                    "ignoreExistingDefinition": False,
                    "owner": "Refinitiv",
                },
                "forwardCurves": [
                    {
                        "curvePoints": [
                            {
                                "endDate": "2021-02-01",
                                "startDate": "2021-02-01",
                                "discountFactor": 1.0,
                                "ratePercent": 7.040811073443143,
                                "tenor": "0D",
                            },
                            {
                                "endDate": "2021-02-04",
                                "startDate": "2021-02-01",
                                "discountFactor": 0.999442450671571,
                                "ratePercent": 7.040811073443143,
                                "tenor": "1D",
                            },
                        ],
                        "forwardCurveTag": "ForwardTag",
                        "forwardStart": "2021-02-01",
                        "indexTenor": "3M",
                    }
                ],
            },
        ]
    }

    expected_str = (
        "     endDate  startDate  discountFactor  ratePercent tenor\n"
        "0 2021-02-01 2021-02-01             1.0     7.040811    0D\n"
        "1 2021-02-04 2021-02-01        0.999442     7.040811    1D"
    )

    # when
    testing_df = forward_curve_build_df(input_raw)

    # then
    assert testing_df.to_string() == expected_str


def test_create_zc_curves():
    # given
    create_zc_curves = get_curves_maker(ContentType.ZC_CURVES)

    # when
    curves = create_zc_curves(zc_curves_json)

    # then
    assert len(curves) > 1


def test_curves_response_factory_create_response_from_one_curve():
    # given
    response_factory = CurvesResponseFactory()
    data = ParsedData({}, {}, zc_curves_json)
    kwargs = {
        "universe": object(),
        "__content_type__": ContentType.ZC_CURVES,
    }

    # when
    response = response_factory.create_success(data, **kwargs)

    # then
    assert response.data.curve is not None


def test_curves_response_factory_create_response_from_many_curves():
    # given
    response_factory = CurvesResponseFactory()
    data = ParsedData({}, {}, forward_curves_json)
    kwargs = {
        "universe": [object(), object()],
        "__content_type__": ContentType.FORWARD_CURVE,
    }

    # when
    response = response_factory.create_success(data, **kwargs)

    # then
    assert len(response.data.curves) == 2


def test_curves_response_factory_create_response_with_data_with_df():
    # given
    response_factory = CurvesResponseFactory()
    data = ParsedData({}, {}, zc_curves_json)
    kwargs = {
        "universe": object(),
        "__content_type__": ContentType.ZC_CURVES,
    }

    # when
    response = response_factory.create_success(data, **kwargs)

    # then
    assert response.data.df.empty is False


def test_curves_response_factory_create_response_for_zc_curve_definitions_with_data_with_df():
    # given
    response_factory = CurvesResponseFactory()
    data = ParsedData({}, {}, zc_curve_definitions_json)
    kwargs = {
        "universe": object(),
        "__content_type__": ContentType.ZC_CURVE_DEFINITIONS,
    }

    # when
    response = response_factory.create_success(data, **kwargs)

    # then
    assert "currency" in response.data.df


def test_curves_response_factory_create_response_for_zc_curve_definitions_with_data_with_empty_df():
    # given
    response_factory = CurvesResponseFactory()
    data = ParsedData({}, {}, {"data": []})
    kwargs = {
        "universe": object(),
        "__content_type__": ContentType.ZC_CURVE_DEFINITIONS,
    }

    # when
    response = response_factory.create_success(data, **kwargs)

    # then
    assert response.data.df.empty is True
