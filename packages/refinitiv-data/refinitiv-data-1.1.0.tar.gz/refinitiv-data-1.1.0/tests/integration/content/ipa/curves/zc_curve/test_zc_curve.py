import json

import allure
import pytest

from refinitiv.data.content.ipa.curves import zc_curves
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.curves.conftest import (
    zc_curves_01,
    zc_curves_02,
    check_curve,
    check_curve_response,
    on_response,
)
from tests.integration.content.ipa.curves.zc_curve.conftest import zc_curves_universe
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - ZcCurve")
@allure.feature("Content object - ZcCurve")
@allure.severity(allure.severity_level.CRITICAL)
class TestZcCurve:
    @allure.title("Create a zc curve definition object with valid params and get data")
    @pytest.mark.caseid("37962810")
    @pytest.mark.smoke
    def test_create_zc_curve_definition_with_valid_params(self, open_session):
        response = zc_curves_01().get_data(
            on_response=lambda response, definition, session: on_response(
                response, definition, open_session
            )
        )

        check_curve_response(response, expected_currency="CHF")
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create a empty zc curve definition object and get data")
    @pytest.mark.caseid("37962856")
    def test_create_empty_zc_curve_definition(self, open_session):
        with pytest.raises(
            RDError,
            match="Error code QPS-Curves.6 | Invalid input: curveDefinition is missing",
        ):
            zc_curves.Definition().get_data()

    @allure.title("Create a zc curve definition object and check curve parameters")
    @pytest.mark.caseid("37962956")
    def test_create_zc_curve_definition_and_check_curve_parameters(self, open_session):
        response = zc_curves_01().get_data()
        curve = response.data.curve
        check_curve(curve)

    @allure.title("Create a zc curve definition object async")
    @pytest.mark.caseid("37963115")
    async def test_create_zc_curve_definition_async(self, open_session_async):
        valid_response, invalid_response = await get_async_response_from_definitions(
            zc_curves_02(), zc_curves.Definition()
        )
        curve = valid_response.data.curve

        check_curve(curve)
        check_curve_response(valid_response, expected_currency="EUR")

        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="QPS-Curves.6",
            expected_error_message="Invalid input: curveDefinition is missing",
        )

    @allure.title("Create a zc_curve with extended parameters")
    @pytest.mark.caseid("C40202633")
    def test_get_zc_curves_with_extended_params(self, open_session):
        response = zc_curves.Definition(
            curve_definition=zc_curves.ZcCurveDefinitions(
                discounting_tenor="OIS",
            ),
            extended_params={
                "curveDefinition": {
                    "currency": "CHF",
                    "discountingTenor": "OIS",
                    "name": "CHF LIBOR Swap ZC Curve",
                },
                "curveParameters": {"useSteps": True, "valuationDate": "2019-08-21"},
            },
        ).get_data()

        check_curve_response(response, expected_currency="CHF")

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == zc_curves_universe
        ), f"Extended params are applied incorrectly"
