import allure
import pytest

from refinitiv.data.content.ipa.surfaces import fx
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
from tests.integration.content.ipa.surfaces.fx.conftest import (
    surface_fx_definition,
    invalid_surface_fx_definition,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
)


@allure.suite("Content object - Surface Fx")
@allure.feature("Content object - Surface Fx")
@allure.severity(allure.severity_level.CRITICAL)
class TestSurfaceFx:
    @allure.title(
        "Create a surface fx definition object with valid params and get data"
    )
    @pytest.mark.caseid("37821399")
    def test_surface_fx_with_valid_params_and_get_data(self, open_session):
        response = surface_fx_definition().get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        surface = response.data.surface
        check_surface(surface)
        curve = surface.get_curve("2021-08-19", fx.Axis.X)
        print(curve)
        check_surface_curve(curve)
        point = surface.get_point("2021-08-19", 1.109)
        check_surface_point(point)

    @allure.title(
        "Create a surface fx definition object with valid params and get data asynchronously"
    )
    @pytest.mark.caseid("37821400")
    @pytest.mark.smoke
    async def test_surface_fx_with_valid_params_and_get_data_async(self, open_session_async):
        valid_response, invalid_response = await get_async_response_from_definitions(
            surface_fx_definition(), invalid_surface_fx_definition()
        )
        check_response_status(valid_response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(valid_response)
        surface = valid_response.data.surface
        check_surface(surface)
        curve = surface.get_curve("2020-08-20", fx.Axis.X)
        check_surface_curve(curve)
        point = surface.get_point("2021-11-19", 1.12)
        check_surface_point(point)

        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="VolSurf.10300",
            expected_error_message="The service failed to build the volatility surface. (Additional technical information: Invalid input: CrossCurrency value is unknown. \'INVAL\' is not a valid FxCrossCode.)",
        )

    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-4119")
    @allure.title("Create a surface fx - short definition")
    @pytest.mark.caseid("37821401")
    def test_surface_fx_with_simple_definition(self, open_session):
        response = fx.Definition(underlying_definition="EURUSD").get_data()
        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create a invalid surface fx definition and get RDError")
    @pytest.mark.caseid("39606894")
    def test_invalid_surface_fx_definition(self, open_session):
        with pytest.raises(
            RDError,
            match="Error code VolSurf.10300 | The service failed to build the volatility surface",
        ):
            invalid_surface_fx_definition().get_data()
