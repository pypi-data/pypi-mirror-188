import json

import allure
import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.contracts.conftest import (
    add_call_backs,
)
from tests.integration.content.ipa.contracts.swap.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
    check_stream_state_and_df_from_stream,
)
from tests.integration.content.ipa.contracts.term_deposit.conftest import (
    term_deposit_definition,
    term_deposit_universe,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
)


@allure.suite("Content object - Term Deposit")
@allure.feature("Content object - Term Deposit")
@allure.severity(allure.severity_level.CRITICAL)
class TestTermDeposit:
    @allure.title(
        "Create term deposit definition object with valid params and get data"
    )
    @pytest.mark.caseid("36801954")
    def test_get_term_deposit_analytics_with_valid_params(self, open_session):
        response = term_deposit_definition().get_data()
        check_http_status_is_success_and_df_value_not_empty(response=response)

    @allure.title("Create term deposit definition object without any parameters")
    @pytest.mark.caseid("36801991")
    def test_get_term_deposit_analytics_without_any_params(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.term_deposit.Definition().get_data()
        assert (
            str(error.value)
            == "Error code QPS-DPS.1011 | Invalid input: instrument definition is invalid. Field 'FixedRatePercent' cannot be empty."
        )

    @allure.title("Create term deposit definition object asynchronously")
    @pytest.mark.caseid("36801992")
    async def test_get_term_deposit_analytics_asynchronously(self, open_session_async):
        response_01, response_02 = await get_async_response_from_definitions(
            rdf.term_deposit.Definition(),
            term_deposit_definition(),
        )

        check_response_status(
            response=response_01,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="QPS-DPS.1011",
            expected_error_message="Invalid input: instrument definition is invalid. Field 'FixedRatePercent' cannot be empty.",
        )
        check_http_status_is_success_and_df_value_not_empty(response_02)

    @allure.title("Create term deposit stream with all callbacks")
    @pytest.mark.caseid("36801994")
    @pytest.mark.smoke
    def test_get_term_deposit_analytics(self, open_session):
        events_list = []
        stream = term_deposit_definition().get_stream()
        add_call_backs(stream, events_list)

        stream.open()
        check_stream_state_and_df_from_stream(stream)
        assert "Response received for" in events_list, f"Events list is {events_list}"

    @allure.title("Create a term deposit definition with extended parameters")
    @pytest.mark.caseid("C39506224")
    def test_get_term_deposit_with_extended_params(self, open_session):
        response = rdf.term_deposit.Definition(
            tenor="2Y",
            notional_ccy="USD",
            extended_params={
                "instrumentType": "TermDeposit",
                "instrumentDefinition": {
                    "instrumentTag": "my tag AED_AM1A",
                    "tenor": "5Y",
                    "notionalCcy": "GBP",
                    "fixedRatePercent": 1,
                },
                "pricingParameters": {"valuationDate": "2018-01-10T00:00:00Z"},
            },
            fields=[
                "InstrumentTag",
                "InstrumentDescription",
                "InterestAmountInDealCcy",
                "FixedRate",
                "MarketValueInDealCcy",
                "MarketValueInReportCcy",
                "ErrorMessage",
            ],
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == term_deposit_universe
        ), f"Extended params are applied incorrectly"
        assert response.data.df.InstrumentTag[0] == "my tag AED_AM1A"
