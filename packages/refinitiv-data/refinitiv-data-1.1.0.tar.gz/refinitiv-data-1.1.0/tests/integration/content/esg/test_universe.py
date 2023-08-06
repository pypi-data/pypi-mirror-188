import allure
import pytest

from refinitiv.data.content.esg import universe
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_dataframe_column_date_for_datetime_type,
)

EXPECTED_TITLES = ["Organization PermID", "Ric Code", "Common name"]
EXPECTED_COLUMN_NAMES = ["TR.OrganizationID", "TR.PrimaryRIC", "TR.CommonName"]


@allure.suite("Content object - ESG Universe")
@allure.feature("Content object - ESG Universe")
@allure.severity(allure.severity_level.CRITICAL)
class TestESGUniverse:
    @allure.title("Create ESG Universe definition object and get data - synchronously")
    @pytest.mark.caseid("C40663512")
    @pytest.mark.smoke
    def test_universe_get_data(self, open_platform_session):
        response = universe.Definition().get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_dataframe_contains_columns_names(response, EXPECTED_TITLES)
        check_non_empty_response_data(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create ESG Universe definition object and get data with different use_field_names_in_headers params - asynchronously"
    )
    @pytest.mark.caseid("C40663507")
    async def test_universe_get_data_async(self, open_platform_session_async):
        first_response, second_response = await get_async_response_from_definitions(
            universe.Definition(use_field_names_in_headers=True),
            universe.Definition(use_field_names_in_headers=False),
        )
        check_response_status(
            response=first_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
        )
        check_non_empty_response_data(first_response)
        check_response_dataframe_contains_columns_names(
            first_response, EXPECTED_COLUMN_NAMES
        )

        check_response_status(
            response=second_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
        )
        check_non_empty_response_data(second_response)
        check_response_dataframe_contains_columns_names(
            second_response, EXPECTED_TITLES
        )

    @allure.title(
        "Create ESG Universe definition object and get data using closed session"
    )
    @pytest.mark.caseid("C40909207")
    def test_universe_get_data_using_closed_session(self, open_platform_session):
        session = open_platform_session
        session.close()
        with pytest.raises(ValueError) as error:
            universe.Definition().get_data()
        assert str(error.value) == "Session is not opened. Can't send any request"

    @allure.title(
        "Create ESG Universe definition object and get data without setting default session"
    )
    @pytest.mark.parametrize(
        "expected_error",
        ["No default session created yet. Please create a session first!"],
    )
    @pytest.mark.caseid("C40909209")
    def test_universe_get_data_without_setting_default_session(self, expected_error):
        with pytest.raises(AttributeError) as error:
            universe.Definition().get_data()
        assert str(error.value) == expected_error

    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-3784")
    @allure.title(
        "Create ESG Universe definition object and get data using invalid closure param"
    )
    @pytest.mark.parametrize(
        "closure, expected_error",
        [(0, "'closure' param must be 'string' object, not 'int'")],
    )
    @pytest.mark.caseid("C40909210")
    def test_universe_get_data_using_invalid_closure_param(
        self, open_platform_session, closure, expected_error
    ):
        with pytest.raises(TypeError) as error:
            universe.Definition(closure=closure).get_data()
        assert str(error.value) == expected_error
