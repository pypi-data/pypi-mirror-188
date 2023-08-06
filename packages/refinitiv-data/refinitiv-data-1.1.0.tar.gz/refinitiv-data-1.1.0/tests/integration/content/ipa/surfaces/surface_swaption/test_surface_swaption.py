import allure
import pytest

from refinitiv.data.content.ipa.surfaces import swaption
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.conftest import (
    check_surface,
    check_surface_curve,
    check_surface_point,
)
from tests.integration.content.ipa.surfaces.surface_swaption.conftest import (
    surface_swaption_definition,
    invalid_surface_swaption_definition,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
)


@allure.suite("Content object - Surface Swaption")
@allure.feature("Content object - Surface Swaption")
@allure.severity(allure.severity_level.CRITICAL)
class TestSurfaceSwaption:
    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-3135")
    @allure.title(
        "Create a surface swaption definition object with valid params and get data"
    )
    @pytest.mark.caseid("37819904")
    @pytest.mark.smoke
    def test_surface_swaption_with_valid_params_and_get_data(self, open_session):
        response = surface_swaption_definition().get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        surface = response.data.surface
        check_surface(surface)
        curve = surface.get_curve("0.25", swaption.Axis.X)
        check_surface_curve(curve)
        point = surface.get_point("0.25", "1Y")
        check_surface_point(point)

    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-3135")
    @allure.title(
        "Create a surface swaption definition object with valid params and get data asynchronously"
    )
    @pytest.mark.caseid("37819906")
    async def test_surface_swaption_with_valid_params_and_get_data_async(
        self, open_session_async
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            surface_swaption_definition(), invalid_surface_swaption_definition()
        )
        check_response_status(valid_response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(valid_response)
        surface = valid_response.data.surface
        check_surface(surface)
        curve = surface.get_curve("0.5", swaption.Axis.X)
        check_surface_curve(curve)
        point = surface.get_point("0.5", "2Y")
        check_surface_point(point)

        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="QPS-Pricer.1923",
            expected_error_message="Invalid market data input for IR volatility. no swaption vol source for INVAL",
        )

    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-4119")
    @allure.title("Create a surface swaption - short definition")
    @pytest.mark.caseid("37819907")
    def test_surface_swaption_with_simple_definition(self, open_session):
        response = swaption.Definition(
            underlying_definition={"instrumentCode": "EUR"}
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        surface = response.data.surface
        check_surface(surface)
        curve = surface.get_curve("1.5", "X")
        check_surface_curve(curve)
        point = surface.get_point("1.5", "3Y")
        check_surface_point(point)

    @allure.title("Create a invalid surface swaption definition and get RDError")
    @pytest.mark.caseid("39606893")
    def test_invalid_surface_swaption_definition(self, open_session):
        with pytest.raises(RDError) as error:
            invalid_surface_swaption_definition().get_data()
        assert (
            str(error.value)
            == "Error code VolSurf.10300 | The service failed to build the volatility surface. (Additional technical information: Analysis error : pricing item is invalid. SABR volatility cube is not available for 'INVAL', as it has no suitable cap volatility surface provider for caplets vol stripping.)"
        )
