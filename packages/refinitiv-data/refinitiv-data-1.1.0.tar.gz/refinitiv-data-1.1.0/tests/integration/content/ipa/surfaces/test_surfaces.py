import allure
import pytest

from refinitiv.data.content.ipa import surfaces
from refinitiv.data.content.ipa.surfaces import cap
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.conftest import (
    check_surface,
    check_surface_curve,
    check_surface_point,
)
from tests.integration.content.ipa.surfaces.cap.conftest import (
    surface_cap_definition,
    invalid_surface_cap_definition,
)
from tests.integration.content.ipa.surfaces.eti.conftest import (
    surface_eti_definition,
)
from tests.integration.content.ipa.surfaces.fx.conftest import (
    surface_fx_definition,
    invalid_surface_fx_definition,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
)


@allure.suite("Content object - Surfaces")
@allure.feature("Content object - Surfaces")
@allure.severity(allure.severity_level.CRITICAL)
class TestSurfaces:
    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-3135")
    @allure.title(
        "Create a surfaces definition object with valid definitions and get data"
    )
    @pytest.mark.caseid("39606902")
    @pytest.mark.smoke
    def test_surfaces_valid_params_and_get_data(self, open_session):
        response = surfaces.Definitions(
            [
                surface_cap_definition(),
                surface_fx_definition(),
                surface_eti_definition(),
            ]
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        surface = response.data.surfaces
        check_surface(surface)
        curve = surface.get_curve("0.5", cap.Axis.X)
        check_surface_curve(curve)
        point = surface.get_point("0.5", "2Y")
        check_surface_point(point)

    @allure.title(
        "Create a surfaces definition object with valid and invalid definitions and get data"
    )
    @pytest.mark.caseid("39606903")
    @pytest.mark.smoke
    def test_surfaces_valid_and_invalid_params_and_get_data(self, open_session):
        response = surfaces.Definitions(
            [
                surface_cap_definition(),
                surface_fx_definition(),
                invalid_surface_fx_definition(),
            ]
        ).get_data()

        check_response_status(
            response=response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="VolSurf.10300",
            expected_error_message="The service failed to build the volatility surface. (Additional technical information: Invalid input: CrossCurrency value is unknown. 'INVAL' is not a valid FxCrossCode.)",
        )

    @allure.title(
        "Create a surfaces definition object with valid and invalid definitions and get data asynchronously"
    )
    @pytest.mark.caseid("39606904")
    @pytest.mark.smoke
    async def test_surfaces_with_valid_and_invalid_params_and_get_data_async(
        self, open_session_async
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            surfaces.Definitions([surface_eti_definition(), surface_fx_definition()]),
            surfaces.Definitions([invalid_surface_cap_definition()]),
        )

        check_response_status(valid_response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="VolSurf.10200",
            expected_error_message="Market data: The service failed to retrieve the necessary data to build the volatility surface",
        )

    @allure.title("Create a invalid surfaces definition and get RDError")
    @pytest.mark.caseid("39606905")
    def test_invalid_surface_cap_definition(self, open_session):
        with pytest.raises(
            RDError,
            match="Error code VolSurf.10200 | Market data: The service failed to retrieve the necessary data to build the volatility surface",
        ):
            surfaces.Definitions([invalid_surface_cap_definition()]).get_data()
