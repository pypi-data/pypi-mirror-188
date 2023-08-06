import json

import allure
import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.errors import RDError
from tests.integration.content.ipa.contracts.conftest import option_definition_01
from tests.integration.content.ipa.contracts.option.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
    check_stream_state_and_df_from_stream,
    option_definition_02,
    option_universe,
)
from tests.integration.helpers import (
    get_async_response_from_definition,
    get_async_response_from_definitions,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - Option")
@allure.feature("Content object - Option")
@allure.severity(allure.severity_level.CRITICAL)
class TestOption:
    @allure.title("Create an option definition object with params and get data")
    @pytest.mark.caseid("36647914")
    def test_create_option_with_valid_params(self, open_session):
        response = option_definition_01().get_data()
        check_http_status_is_success_and_df_value_not_empty(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create an Option definition without any parameters")
    @pytest.mark.caseid("C36647917")
    def test_create_option_without_any_params(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.option.Definition().get_data(session=open_session)
        assert (
            str(error.value)
            == "Error code 400 | The underlyingType cannot be found, in the request, from the expected path instrumentDefinition.underlyingType for 'instrumentType' Option"
        )

    @allure.title("Create an Option definition with empty pricing parameters")
    @pytest.mark.caseid("36647981")
    def test_create_option_with_empty_pricing_parameters(self, open_session):
        response = rdf.option.Definition(
            underlying_type=rdf.option.UnderlyingType.FX,
            strike=265,
            underlying_definition=rdf.option.FxUnderlyingDefinition("AUDUSD"),
            notional_ccy="AUD",
            tenor="5M",
            pricing_parameters=rdf.option.PricingParameters(),
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create a Option definition request asynchronously")
    @pytest.mark.caseid("36678381")
    async def test_create_async_option_definition(self, open_session_async):
        response = await get_async_response_from_definition(option_definition_01())

        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create multiple async Option definitions")
    @pytest.mark.caseid("36678382")
    async def test_create_multiple_async_option_definitions(self, open_session_async):
        response_01, response_02 = await get_async_response_from_definitions(
            option_definition_01(), option_definition_02()
        )

        check_http_status_is_success_and_df_value_not_empty(response_01)

    @allure.title("Create an Option stream")
    @pytest.mark.caseid("36678383")
    def test_create_option_stream(self, open_session):
        stream = option_definition_01().get_stream()
        stream.open()

        check_stream_state_and_df_from_stream(stream)

    @allure.title("Create an option definition with extended parameters")
    @pytest.mark.caseid("C37435263")
    def test_get_option_with_extended_params(self, open_session):
        response = rdf.option.Definition(
            underlying_type=rdf.option.UnderlyingType.FX,
            strike=290,
            underlying_definition=rdf.option.FxUnderlyingDefinition("EUR"),
            tenor="7M",
            pricing_parameters=rdf.option.PricingParameters(
                pricing_model_type=rdf.option.PricingModelType.BLACK_SCHOLES,
                fx_spot_object=rdf.option.BidAskMid(
                    bid=0.7387,
                    ask=0.7387,
                    mid=0.7387,
                ),
            ),
            extended_params={
                "instrumentDefinition": {
                    "InstrumentTag": "my tag",
                    "tenor": "5M",
                    "notionalCcy": "AUD",
                    "underlyingDefinition": {"fxCrossCode": "AUDUSD"},
                    "underlyingType": "Fx",
                    "strike": 265,
                },
                "pricingParameters": {
                    "fxSpotObject": {"bid": 0.7387, "ask": 0.7387, "mid": 0.7387},
                    "priceSide": "Mid",
                    "pricingModelType": "BlackScholes",
                    "valuationDate": "2018-08-06",
                },
            },
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == option_universe
        ), f"Extended params are applied incorrectly"
        assert response.data.df.InstrumentTag[0] == "my tag"
