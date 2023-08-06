import allure
import pytest

from refinitiv.data.content.esg import basic_overview
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ownership.helpers import (
    check_response_dataframe_instrument_contains_expected_universes,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_dataframe_column_date_for_datetime_type,
)

EXPECTED_TITLES = [
    "Instrument",
    "Period End Date",
    "ESG Reporting Scope",
    "ESG Period Last Update Date",
    "CO2 Equivalents Emission Total",
    "Women Managers",
    "Average Training Hours",
]


@allure.suite("Content object - ESG Basic Overview")
@allure.feature("Content object - ESG Basic Overview")
@allure.severity(allure.severity_level.CRITICAL)
class TestESGBasicOverview:
    @allure.title(
        "Create ESG Basic Overview definition object with valid params - synchronously"
    )
    @pytest.mark.parametrize(
        "universe",
        ["IBM.N", ["IBM.N", "VOD.L"]],
    )
    @pytest.mark.caseid("C40203262")
    @pytest.mark.smoke
    def test_esg_basic_overview_definition_object_with_valid_params_and_get_data(
        self, universe, open_platform_session
    ):
        response = basic_overview.Definition(universe=universe).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_dataframe_contains_columns_names(response, EXPECTED_TITLES)
        check_response_dataframe_instrument_contains_expected_universes(
            response, universe
        )
        check_non_empty_response_data(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create ESG Basic Overview definition object with invalid params and get error"
    )
    @pytest.mark.caseid("C40203263")
    @pytest.mark.parametrize(
        "universe,expected_error",
        [
            (
                [],
                "Error code 400 | Validation error: Missing required parameter 'universe'",
            ),
            (
                ["INVALID"],
                "Error code 412 | Unable to resolve all requested identifiers. Requested items: ['INVALID']",
            ),
        ],
    )
    def test_esg_basic_overview_definition_object_with_invalid_params_and_get_error(
        self,
        universe,
        expected_error,
        open_platform_session,
    ):
        with pytest.raises(RDError) as error:
            basic_overview.Definition(universe=universe).get_data()
        assert str(error.value) == expected_error

    @allure.title("Create ESG Basic Overview definition object using closed session")
    @pytest.mark.caseid("C40203264")
    def test_esg_basic_overview_definition_object_using_closed_session(
        self, open_platform_session
    ):
        session = open_platform_session
        session.close()
        with pytest.raises(ValueError) as error:
            basic_overview.Definition(universe="IBM.N").get_data()
        assert str(error.value) == "Session is not opened. Can't send any request"

    @allure.title(
        "Create ESG Basic Overview definition object with use mix valid and invalid data - asynchronously"
    )
    @pytest.mark.caseid("C40203265")
    @pytest.mark.parametrize(
        "universe,invalid_universe", [(["IBM.N", "INVALID"], "INVALID")]
    )
    async def test_esg_basic_overview_definition_object_with_use_mix_valid_and_invalid_data(
        self, open_platform_session_async, universe, invalid_universe
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            basic_overview.Definition(universe=universe),
            basic_overview.Definition(universe=invalid_universe),
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
