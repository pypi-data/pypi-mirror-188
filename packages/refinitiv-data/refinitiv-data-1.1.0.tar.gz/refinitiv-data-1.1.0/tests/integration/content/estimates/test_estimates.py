import allure
import pytest

from refinitiv.data.content import estimates
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.estimates.conftest import (
    invalid_view_actuals_interim_estimates,
    view_actuals_annual_estimates,
    view_actuals_kpi_annual_estimates,
    view_summary_annual_estimates,
    view_summary_historical_non_periodic_estimates,
    view_summary_historical_annual_estimates,
    view_summary_recommendations_estimates,
    view_summary_kpi_annual_estimates,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
    check_extended_params_were_sent_in_request,
    check_response_dataframe_contains_columns_names,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - Estimates")
@allure.feature("Content object - Estimates")
@allure.severity(allure.severity_level.CRITICAL)
class TestEstimates:
    @allure.title(
        "Create estimates definition object with valid params - synchronously"
    )
    @pytest.mark.caseid("C40050717")
    @pytest.mark.parametrize(
        "estimates_definition,universe,package,header",
        [
            (
                view_actuals_annual_estimates,
                "IBM",
                estimates.Package.PROFESSIONAL,
                "name",
            ),
            (
                view_summary_annual_estimates,
                ["IBM.N", "ORCL.N"],
                estimates.Package.BASIC,
                "title",
            ),
        ],
    )
    @pytest.mark.smoke
    def test_estimates_definition_object_with_valid_params_and_get_data(
        self,
        estimates_definition,
        open_platform_session_with_rdp_creds,
        universe,
        package,
        header,
    ):
        response = estimates_definition(universe=universe, package=package)
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create estimates definition object with use_field_names_in_headers True"
    )
    @pytest.mark.caseid("C40050718")
    @pytest.mark.parametrize(
        "universe,expected_column_names",
        [
            (
                ["GOOG.O", "MSFT.O", "FB.O", "AMZN.O", "TWTR.K"],
                [
                    "instrument",
                    "periodenddate",
                    "fperiod",
                    "rfperiod",
                    "TR.AdRevenueActValue",
                ],
            )
        ],
    )
    def test_estimates_definition_object_with_use_field_names_in_headers_true(
        self,
        open_platform_session_with_rdp_creds,
        universe,
        expected_column_names,
    ):
        response = view_actuals_kpi_annual_estimates(
            universe, use_field_names_in_headers=True
        )
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column_names)

    @allure.title(
        "Create estimates definition object with invalid params and get error"
    )
    @pytest.mark.caseid("C40050719")
    @pytest.mark.parametrize(
        "universe,package,expected_error",
        [
            (
                [],
                estimates.Package.PROFESSIONAL,
                "Error code 400 | Validation error: validation failure list:\nuniverse.0 in query should be at least 1 chars long",
            ),
            (
                ["INVALID"],
                estimates.Package.BASIC,
                "Error code 412 | Unable to resolve all requested identifiers. Requested items: ['INVALID']",
            ),
        ],
    )
    def test_estimates_definition_object_with_invalid_params_and_get_error(
        self,
        universe,
        package,
        expected_error,
        open_platform_session_with_rdp_creds,
    ):
        with pytest.raises(RDError) as error:
            view_summary_annual_estimates(universe=universe, package=package)
        assert str(error.value) == expected_error

    @allure.title("Create estimates definition object using closed session")
    @pytest.mark.caseid("C40050720")
    def test_estimates_definition_object_using_closed_session(
        self, open_platform_session_with_rdp_creds
    ):
        session = open_platform_session_with_rdp_creds
        session.close()
        with pytest.raises(ValueError) as error:
            view_actuals_annual_estimates(
                universe="IBM.N", package=estimates.Package.PROFESSIONAL
            )
        assert str(error.value) == "Session is not opened. Can't send any request"

    @allure.title("Create estimates definition object with wrong package")
    @pytest.mark.caseid("C40050721")
    def test_estimates_definition_object_with_wrong_package(
        self, open_platform_session_with_rdp_creds
    ):
        with pytest.raises(AttributeError) as error:
            view_summary_recommendations_estimates(
                universe="IBM.N", package="WRONG_PACKAGE"
            )
        assert (
            str(error.value)
            == "Value 'WRONG_PACKAGE' must be in ['basic', 'standard', 'professional']"
        )

    @allure.title("Create estimates definition object with extended params")
    @pytest.mark.caseid("C40050723")
    @pytest.mark.parametrize(
        "estimate_definition,universe,package,extended_params",
        [
            (
                view_summary_historical_annual_estimates,
                "IBM.N",
                estimates.Package.PROFESSIONAL,
                {"universe": "ORCL.N"},
            ),
            (
                view_summary_historical_non_periodic_estimates,
                "ORCL.N",
                estimates.Package.PROFESSIONAL,
                {"package": "basic"},
            ),
        ],
    )
    def test_estimates_definition_object_with_extended_params(
        self,
        open_platform_session_with_rdp_creds,
        estimate_definition,
        universe,
        package,
        extended_params,
    ):
        response = estimate_definition(universe, package, extended_params)
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_extended_params_were_sent_in_request(response, extended_params)

    @allure.title(
        "Create estimates definition object with use mix valid and invalid data and get partial result"
    )
    @pytest.mark.caseid("C40050722")
    @pytest.mark.parametrize(
        "universe,invalid_universe", [(["ORCL.N", "INVALID"], "INVALID")]
    )
    async def test_estimates_definition_object_with_use_mix_valid_and_invalid_data(
        self, open_platform_session_with_rdp_creds_async, universe, invalid_universe
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            view_summary_kpi_annual_estimates(universe=universe),
            invalid_view_actuals_interim_estimates(universe=invalid_universe),
        )
        check_response_status(
            response=valid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code=None,
            expected_error_message="Failed to resolve identifiers ['INVALID']",
        )
        check_non_empty_response_data(valid_response)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code=HttpStatusCode.FOUR_HUNDRED_TWELVE,
            expected_error_message="Unable to resolve all requested identifiers. Requested items: ['INVALID']",
        )
