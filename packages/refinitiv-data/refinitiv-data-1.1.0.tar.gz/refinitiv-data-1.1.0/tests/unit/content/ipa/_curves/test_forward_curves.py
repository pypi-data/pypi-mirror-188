from refinitiv.data.errors import RDError
from refinitiv.data.content.ipa.curves import forward_curves
from tests.unit.conftest import StubSession, StubResponse


def test_forward_curves_two_errors_in_response_will_raise_error():
    # given
    extended_message = (
        "Error code QPS-Curves.6 | Invalid input: curveDefinition is missing"
    )
    response = StubResponse(
        {
            "data": [
                {
                    "error": {
                        "id": "babee8e8-6cd1-48bb-8e19-321c053ab17a/babee8e8-6cd1-48bb-8e19-321c053ab17a",
                        "code": "QPS-Curves.6",
                        "message": "Invalid input: curveDefinition is missing",
                    }
                },
                {
                    "error": {
                        "id": "babee8e8-6cd1-48bb-8e19-321c053ab17a/babee8e8-6cd1-48bb-8e19-321c053ab17a",
                        "code": "QPS-Curves.6",
                        "message": "Invalid input: curveDefinition is missing",
                    }
                },
            ]
        }
    )
    session = StubSession(is_open=True, response=response)
    definition = forward_curves.Definitions(
        [forward_curves.Definition(), forward_curves.Definition()]
    )

    try:
        # when
        definition.get_data(session)
    except RDError as e:
        # then
        assert str(e) == extended_message
    else:
        assert False


def test_forward_curves_one_error_in_response_will_not_raise_error():
    # given
    response = StubResponse(
        {
            "data": [
                {
                    "error": {
                        "id": "81124005-5a32-42fb-b833-5869ab04a1e8/81124005-5a32-42fb-b833-5869ab04a1e8",
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
                        "valuationDate": "2022-02-08",
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
                                    "ratePercent": -0.5576014785508066,
                                    "tenor": "0D",
                                },
                                {
                                    "endDate": "2021-02-04",
                                    "startDate": "2021-02-01",
                                    "discountFactor": 1.000045833991234,
                                    "ratePercent": -0.5576014785508066,
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
    )
    session = StubSession(is_open=True, response=response)
    definition = forward_curves.Definitions(
        [forward_curves.Definition(), forward_curves.Definition()]
    )

    try:
        # when
        response = definition.get_data(session)
    except RDError as e:
        # then
        assert False, str(e)
    else:
        assert len(response.errors) == 1
