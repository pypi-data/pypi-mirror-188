import allure
import pytest

from refinitiv.data.content.ipa.curves import zc_curves
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.curves.conftest import (
    on_response,
    check_curve_response,
    check_curves,
    zc_curves_01,
    zc_curves_02,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - ZcCurves")
@allure.feature("Content object - ZcCurves")
@allure.severity(allure.severity_level.CRITICAL)
class TestZcCurves:
    @allure.title("Create a zc_curves object with valid definitions and get data")
    @pytest.mark.caseid("39788765")
    @pytest.mark.smoke
    def test_create_zc_curves_definition_with_valid_definitions(self, open_session):
        response = zc_curves.Definitions([zc_curves_01(), zc_curves_02()]).get_data(
            on_response=lambda response, definition, session: on_response(
                response, definition, open_session
            )
        )

        check_curves(response)
        check_curve_response(response, expected_currency="CHF")
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create zc curves object with invalid definition and get data")
    @pytest.mark.caseid("39788766")
    def test_create_invalid_zc_curves(self, open_session):
        with pytest.raises(
            RDError,
            match="Error code QPS-Curves.6 | Invalid input: curveDefinition is missing",
        ):
            zc_curves.Definitions(zc_curves.Definition()).get_data()

    @allure.title("Create a zc curves definition object async")
    @pytest.mark.caseid("39788767")
    async def test_create_zc_curves_definition_async(self, open_session_async):
        valid_response, invalid_response = await get_async_response_from_definitions(
            zc_curves.Definitions([zc_curves_01(), zc_curves_02()]),
            zc_curves.Definitions(zc_curves.Definition()),
        )

        check_curves(valid_response)
        check_curve_response(valid_response, expected_currency="CHF")

        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="QPS-Curves.6",
            expected_error_message="Invalid input: curveDefinition is missing",
        )

    @allure.title(
        "Create a zc curves definition object with valid and invalid zc_crve definition and get data"
    )
    @pytest.mark.caseid("39788768")
    @pytest.mark.smoke
    def test_create_zc_curves_definition_with_valid_and_invalid_forward_curve(
        self, open_session
    ):
        response = zc_curves.Definitions(
            [zc_curves_01(), zc_curves.Definition()]
        ).get_data()

        check_curve_response(response, expected_currency="CHF")
        check_response_status(
            response=response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="QPS-Curves.6",
            expected_error_message="Invalid input: curveDefinition is missing",
        )
        check_curves(response)
