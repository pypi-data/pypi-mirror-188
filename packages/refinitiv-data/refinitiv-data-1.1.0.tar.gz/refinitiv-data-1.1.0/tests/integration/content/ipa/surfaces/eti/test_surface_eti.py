import allure
import pytest

from refinitiv.data.content.ipa.surfaces import eti
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.conftest import (
    check_surface,
    check_surface_curve,
    check_surface_point,
)
from tests.integration.content.ipa.surfaces.eti.conftest import (
    surface_eti_definition,
    invalid_surface_eti_definition,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
)


@allure.suite("Content object - Surface Eti")
@allure.feature("Content object - Surface Eti")
@allure.severity(allure.severity_level.CRITICAL)
class TestSurfaceEti:
    @allure.title(
        "Create a surface eti definition object with valid params and get data"
    )
    @pytest.mark.caseid("37821477")
    @pytest.mark.smoke
    def test_surface_eti_with_valid_params_and_get_data(self, open_session):
        response = surface_eti_definition().get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        surface = response.data.surface
        check_surface(surface)
        curve = surface.get_curve("2022-03-18", eti.Axis.X)
        check_surface_curve(curve)
        point = surface.get_point("2022-03-18", 49.75)
        check_surface_point(point)

    @allure.title(
        "Create a surface eti definition object with valid params and get data asynchronously"
    )
    @pytest.mark.caseid("37821478")
    async def test_surface_eti_with_valid_params_and_get_data_async(self, open_session_async):
        valid_response, invalid_response = await get_async_response_from_definitions(
            surface_eti_definition(), invalid_surface_eti_definition()
        )
        surface = valid_response.data.surface
        check_surface(surface)
        curve = surface.get_curve("2021-12-17", eti.Axis.X)
        check_surface_curve(curve)
        point = surface.get_point("2021-12-17", 59.62)
        check_surface_point(point)

        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="VolSurf.10006",
            expected_error_message="Invalid input: Instrument code must end with @RIC, @RICROOT",
        )

    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-4119")
    @allure.title("Create a surface eti - short definition")
    @pytest.mark.caseid("37821479")
    def test_surface_eti_with_simple_definition(self, open_session):
        response = eti.Definition(underlying_definition={"instrumentCode": "USD"}).get_data()
        surface = response.data.surface
        check_surface(surface)
        curve = surface.get_curve("2021-11-19", "X")
        check_surface_curve(curve)
        point = surface.get_point("2021-11-19", 50.89)
        check_surface_point(point)

    @allure.title("Create a invalid surface eti definition and get RDError")
    @pytest.mark.caseid("39606896")
    def test_invalid_surface_eti_definition(self, open_session):
        with pytest.raises(
            RDError,
            match="Error code VolSurf.10006 | Invalid input: Instrument code must end with @RIC, @RICROOT",
        ):
            invalid_surface_eti_definition().get_data()
