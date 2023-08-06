import allure
import pytest

from refinitiv.data.content.ipa.surfaces import cap
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.conftest import (
    check_surface,
    check_surface_curve,
    check_surface_point,
)
from tests.integration.content.ipa.contracts.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
)
from tests.integration.content.ipa.surfaces.cap.conftest import (
    surface_cap_definition,
    invalid_surface_cap_definition,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
)


@allure.suite("Content object - Surface Cap")
@allure.feature("Content object - Surface Cap")
@allure.severity(allure.severity_level.CRITICAL)
class TestSurfaceCap:
    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-4119")
    @allure.title(
        "Create a surface cap definition object with valid params and get data"
    )
    @pytest.mark.caseid("37821484")
    def test_surface_cap_with_valid_params_and_get_data(self, open_session):
        response = surface_cap_definition().get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        surface = response.data.surface
        check_surface(surface)
        curve = surface.get_curve("0.5", cap.Axis.X)
        check_surface_curve(curve)
        point = surface.get_point("0.5", "2Y")
        check_surface_point(point)

    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-3135")
    @allure.title(
        "Create a surface cap definition object with valid and invalid params and get data asynchronously"
    )
    @pytest.mark.caseid("37821485")
    @pytest.mark.smoke
    async def test_surface_cap_with_valid_and_invalid_params_and_get_data_async(
        self, open_session_async
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            surface_cap_definition(), invalid_surface_cap_definition()
        )

        check_response_status(valid_response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="VolSurf.10200",
            expected_error_message="Market data: The service failed to retrieve the necessary data to build the volatility surface",
        )

        surface = valid_response.data.surface
        check_surface(surface)

    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-4119")
    @allure.title("Create a surface cap - short definition")
    @pytest.mark.caseid("37821486")
    def test_surface_cap_with_simple_definition(self, open_session):
        response = cap.Definition("USD").get_data()
        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create an invalid surface cap definition and get RDError")
    @pytest.mark.caseid("39606897")
    def test_invalid_surface_cap_definition(self, open_session):
        with pytest.raises(
            RDError,
            match="Error code VolSurf.10200 | Market data: The service failed to retrieve the necessary data to build the volatility surface",
        ):
            invalid_surface_cap_definition().get_data()
