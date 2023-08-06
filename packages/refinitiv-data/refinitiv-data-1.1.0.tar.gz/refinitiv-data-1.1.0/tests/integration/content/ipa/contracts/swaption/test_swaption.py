import json

import allure
import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.errors import RDError
from tests.integration.content.ipa.contracts.swap.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
    check_stream_state_and_df_from_stream,
)
from tests.integration.content.ipa.contracts.swaption.conftest import (
    swaption_definition_01,
    swaption_definition_02,
    swaption_universe,
)
from tests.integration.helpers import (
    get_async_response_from_definition,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - Swaption")
@allure.feature("Content object - Swaption")
@allure.severity(allure.severity_level.CRITICAL)
class TestSwaption:
    @allure.title("Create swaption definition object with valid params and get data")
    @pytest.mark.caseid("36796304")
    def test_get_swaption_analytics(self, open_session):
        response = swaption_definition_01().get_data()
        check_http_status_is_success_and_df_value_not_empty(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create swaption definition object with specific session")
    @pytest.mark.caseid("36796339")
    def test_get_swaption_analytics_with_specific_session(self, open_session):
        response = swaption_definition_02().get_data(open_session)
        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create swaption definition object without any parameters")
    @pytest.mark.caseid("36796341")
    def test_get_swaption_analytics_without_any_parameters(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.swaption.Definition().get_data()
        assert (
            str(error.value)
            == "Error code QPS-DPS.1046 | Invalid input: missing underlying instrument. InstrumentDefinition is empty. Please provide a valid InstrumentDefinition."
        )

    @allure.title("Create swaption definition object asynchronously")
    @pytest.mark.caseid("36796342")
    async def test_get_swaption_analytics_asynchronously(self, open_session_async):
        response = await get_async_response_from_definition(swaption_definition_01())
        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create swaption stream")
    @pytest.mark.caseid("36796343")
    def test_create_swaption_stream(self, open_session):
        stream = swaption_definition_02().get_stream(open_session)
        stream.open()

        check_stream_state_and_df_from_stream(stream)

    @allure.title("Create swaption stream without session")
    @pytest.mark.caseid("36796344")
    def test_create_swaption_stream_without_session(self):
        with pytest.raises(AttributeError) as error:
            swaption_definition_02().get_stream()
        assert (
            str(error.value)
            == "No default session created yet. Please create a session first!"
        )

    @allure.title("Create swaption definition with extended parameters")
    @pytest.mark.caseid("C37474014")
    def test_get_swaption_with_extended_params(self, open_session):
        response = rdf.swaption.Definition(
            instrument_tag="BermudanEURswaption",
            tenor="2Y",
            bermudan_swaption_definition=rdf.swaption.BermudanSwaptionDefinition(
                exercise_schedule_type=rdf.swaption.ExerciseScheduleType.FLOAT_LEG,
                notification_days=22,
            ),
            underlying_definition=rdf.swap.Definition(tenor="1Y", template="NOK_AB6O"),
            extended_params={
                "instrumentDefinition": {
                    "instrumentTag": "BermudanEURswaption",
                    "tenor": "7Y",
                    "notionalAmount": 1000000,
                    "bermudanSwaptionDefinition": {
                        "exerciseScheduleType": "FloatLeg",
                        "notificationDays": 0,
                    },
                    "buySell": "Buy",
                    "exerciseStyle": "BERM",
                    "settlementType": "Cash",
                    "swaptionType": "Payer",
                    "underlyingDefinition": {"tenor": "3Y", "template": "NOK_AB6O"},
                    "strikePercent": 2.75,
                },
                "pricingParameters": {
                    "nbIterations": 80,
                    "valuationDate": "2020-04-24",
                },
            },
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == swaption_universe
        ), f"Extended params are applied incorrectly"
        assert response.data.df.InstrumentTag[0] == "BermudanEURswaption"
