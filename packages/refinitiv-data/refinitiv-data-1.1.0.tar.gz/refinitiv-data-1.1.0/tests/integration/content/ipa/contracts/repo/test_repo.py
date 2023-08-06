import json

import allure
import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.errors import RDError
from tests.integration.content.ipa.contracts.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
    check_stream_state_and_df_from_stream,
    add_call_backs,
)
from tests.integration.content.ipa.contracts.repo.conftest import (
    repo_definition_01,
    repo_definition_02,
    on_response,
    repo_universe,
)
from tests.integration.helpers import get_async_response_from_definition


@allure.suite("Content object - Repo")
@allure.feature("Content object - Repo")
@allure.severity(allure.severity_level.CRITICAL)
class TestRepo:
    @allure.title(
        "Create two repo definition object with params in one session and get data"
    )
    @pytest.mark.caseid("36746892")
    def test_repo_get_data(self, open_session):
        events_list = []
        response_01 = repo_definition_01().get_data(
            on_response=lambda response, content_provider, session: on_response(
                response, session, events_list
            )
        )
        response_02 = repo_definition_02().get_data()

        assert "Response received for" in events_list, f"Events list is {events_list}"
        check_http_status_is_success_and_df_value_not_empty(response_01)
        check_http_status_is_success_and_df_value_not_empty(response_02)

    @allure.title("Create repo definition object without any parameters")
    @pytest.mark.caseid("36746910")
    def test_create_repo_without_any_parameters(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.repo.Definition().get_data()
        assert (
            str(error.value)
            == "Error code QPS-DPS.1024 | Invalid date. Provide either fields 'EndDate' or 'Tenor', not both or none."
        )

    @allure.title("Create repo definition asynchronously")
    @pytest.mark.caseid("36746933")
    async def test_repo_get_data_async(self, open_session_async):
        response = await get_async_response_from_definition(repo_definition_01())

        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create a repo stream with callbacks")
    @pytest.mark.caseid("36746936")
    def test_repo_get_stream(self, open_session):
        events_list = []
        stream = repo_definition_01().get_stream()

        add_call_backs(stream, events_list)

        stream.open()
        check_stream_state_and_df_from_stream(stream)
        assert "Response received for" in events_list, f"Events list is {events_list}"

    @allure.title("Create a repo definition with extended parameters")
    @pytest.mark.caseid("C39383379")
    def test_get_repo_with_extended_params(self, open_session):
        response = rdf.repo.Definition(
            underlying_instruments=[
                rdf.repo.UnderlyingContract(
                    instrument_type="Bond",
                    instrument_definition=rdf.bond.Definition(
                        instrument_code="US12345="
                    ),
                    pricing_parameters=rdf.repo.UnderlyingPricingParameters(
                        repo_parameters=rdf.repo.RepoParameters(
                            initial_margin_percent=20
                        )
                    ),
                )
            ],
            extended_params={
                "instrumentDefinition": {
                    "InstrumentTag": "my tag",
                    "startDate": "2020-08-17T00:00:00Z",
                    "endDate": "2020-08-22T00:00:00Z",
                    "underlyingInstruments": [
                        {
                            "instrumentType": "Bond",
                            "instrumentDefinition": {"instrumentCode": "US191450264="},
                            "pricingParameters": {
                                "repoParameters": {"initialMarginPercent": 50}
                            },
                        }
                    ],
                },
                "pricingParameters": {"marketDataDate": "2020-08-19T00:00:00Z"},
            },
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == repo_universe
        ), f"Extended params are applied incorrectly"
        assert response.data.df.InstrumentTag[0] == "my tag"
