import json

import allure
import pytest

from refinitiv.data.content.ipa.curves import forward_curves
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.curves.conftest import (
    forward_curve_definition_01,
    forward_curve_definition_02,
    check_curve,
    check_curve_response,
)
from tests.integration.content.ipa.curves.forward_curve.conftest import forward_curve_universe
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - ForwardCurve")
@allure.feature("Content object - ForwardCurve")
@allure.severity(allure.severity_level.CRITICAL)
class TestForwardCurve:
    @allure.title(
        "Create a forward curve definition object with valid params and get data"
    )
    @pytest.mark.caseid("37902310")
    @pytest.mark.smoke
    def test_create_forward_curve_definition_with_valid_params(self, open_session):
        response = forward_curve_definition_01().get_data()

        check_curve_response(response, expected_currency="EUR")
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create a empty forward curve definition object and get data")
    @pytest.mark.caseid("37922828")
    def test_create_empty_forward_curve_definition(self, open_session):
        with pytest.raises(
            RDError,
            match="Error code QPS-Curves.6 | Invalid input: curveDefinition is missing",
        ):
            forward_curves.Definition().get_data()

    @allure.title("Create a forward curve definition object and check curve parameters")
    @pytest.mark.caseid("37922829")
    def test_create_forward_curve_definition_and_check_curve_parameters(
        self, open_session
    ):
        response = forward_curve_definition_02().get_data()
        curve = response.data.curve
        check_curve(curve)

    @allure.title("Create a forward curve definition object async")
    @pytest.mark.caseid("37922830")
    async def test_create_forward_curve_definition_async(self, open_session_async):
        invalid_response, valid_response = await get_async_response_from_definitions(
            forward_curves.Definition(), forward_curve_definition_02()
        )

        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="QPS-Curves.6",
            expected_error_message="Invalid input: curveDefinition is missing",
        )

        curve = valid_response.data.curve
        check_curve(curve)
        assert not valid_response.data.df.empty

    @allure.title("Create a forward curve definition with extended parameters")
    @pytest.mark.caseid("C48910806")
    def test_get_forward_curve_with_extended_params(self, open_session):
        response = forward_curves.Definition(
            forward_curve_definitions=[
                forward_curves.ForwardCurveDefinition(
                    index_tenor="1M",
                    forward_curve_tenors=["0D", "1D", "11D"],
                )
            ],
            curve_definition=forward_curves.SwapZcCurveDefinition(
                currency="EUR",
                name="EUR EURIBOR Swap ZC Curve",
            ),
            curve_tag="test_curve",
            extended_params={
                "curveDefinition": {
                    "indexName": "EURIBOR",
                    "currency": "EUR",
                    "discountingTenor": "OIS",
                    "name": "EUR EURIBOR Swap ZC Curve",
                },
                "curveParameters": {"calendarAdjustment": "Calendar"},
                "forwardCurveDefinitions": [
                    {
                        "indexTenor": "3M",
                        "forwardCurveTenors": ["0D", "1D"],
                        "forwardCurveTag": "MyForwardTag",
                        "forwardStartDate": "2021-02-01",
                        "forwardStartTenor": "some_start_tenor",
                    }
                ],
                "curveTag": "my_test_curve",
            },
        ).get_data()

        check_curve_response(response, expected_currency="EUR")

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == forward_curve_universe
        ), f"Extended params are applied incorrectly"
        assert response.data.raw['data'][0]['curveTag'] == "my_test_curve"
        assert response.data.curve.forward_curve_tag == "MyForwardTag"

