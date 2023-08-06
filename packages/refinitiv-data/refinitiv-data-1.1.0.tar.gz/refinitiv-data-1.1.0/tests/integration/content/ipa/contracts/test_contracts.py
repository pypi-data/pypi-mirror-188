import allure
import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.contracts.conftest import (
    financial_contracts_definition_without_fields,
    financial_contracts_definition_with_fields,
    check_http_status_is_success_and_df_value_not_empty,
    check_request_message_contains_expected_fields,
    get_valid_and_invalid_financial_contracts_definition,
)
from tests.integration.helpers import (
    get_async_response_from_definition,
    check_response_dataframe_contains_columns_names,
    check_response_status,
    check_dataframe_column_date_for_datetime_type,
)

COLUMN_NAMES = {
    "argnames": "expected_column_names",
    "argvalues": [
        (
            [
                "InstrumentCode",
                "MarketDataDate",
                "YieldPercent",
                "GovernmentSpreadBp",
                "GovCountrySpreadBp",
                "RatingSpreadBp",
                "SectorRatingSpreadBp",
                "EdsfSpreadBp",
                "IssuerSpreadBp",
                "ErrorMessage",
            ]
        )
    ],
}


@allure.suite("IPA FinancialContracts")
@allure.feature("IPA FinancialContracts")
@allure.severity(allure.severity_level.CRITICAL)
class TestFinancialContracts:
    @allure.title("Create a list of definitions with params and get data")
    @pytest.mark.parametrize(**COLUMN_NAMES)
    @pytest.mark.caseid("38447246")
    def test_user_created_definitions_list(self, open_session, expected_column_names):
        response = financial_contracts_definition_without_fields().get_data()
        check_http_status_is_success_and_df_value_not_empty(response)
        check_response_dataframe_contains_columns_names(response, expected_column_names)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create a list of definitions with expected fields in dataframe columns"
    )
    @pytest.mark.caseid("38447487")
    @pytest.mark.parametrize(**COLUMN_NAMES)
    def test_user_created_definitions_list_with_custom_fields_1(
        self, open_session, expected_column_names
    ):
        response = financial_contracts_definition_with_fields().get_data()
        check_request_message_contains_expected_fields(response, expected_column_names)
        check_response_dataframe_contains_columns_names(response, expected_column_names)

    @allure.title("Create a list of definitions request asynchronously")
    @pytest.mark.caseid("38447267")
    async def test_user_created_definitions_list_asynchronously(self, open_session_async):
        response = await get_async_response_from_definition(
            financial_contracts_definition_without_fields()
        )
        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title(
        "Create a list of definitions request asynchronously with mix of valid and invalid parameters"
    )
    @pytest.mark.parametrize(
        "error_message",
        [
            "Analysis error : an error occurred. An unexpected error occurs during analysis step"
        ],
    )
    @pytest.mark.caseid("38447267")
    async def test_user_get_data_async_with_mix_of_valid_and_invalid_params(
        self, error_message, open_session_async
    ):
        definition = get_valid_and_invalid_financial_contracts_definition()
        response = await get_async_response_from_definition(definition)
        check_http_status_is_success_and_df_value_not_empty(response)

        check_response_status(
            response=response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_message=error_message,
        )

    @allure.title(
        "Create a definition list object without required parameter"
    )
    @pytest.mark.caseid("38447268")
    def test_definition_with_invalid_value_type(self, open_session):
        with pytest.raises(TypeError) as error:
            rdf.Definitions().get_data()
        assert str(error.value) == "__init__() missing 1 required positional argument: 'universe'"
