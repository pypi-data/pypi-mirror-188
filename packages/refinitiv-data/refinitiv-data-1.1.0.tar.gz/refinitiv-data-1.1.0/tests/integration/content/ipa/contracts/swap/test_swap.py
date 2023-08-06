import json

import allure
import pytest

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.errors import RDError
from tests.integration.content.ipa.contracts.swap.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
    check_stream_state_and_df_from_stream,
    swap_definition_01,
    swap_definition_02,
    swap_universe,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - SWAP")
@allure.feature("Content object - SWAP")
@allure.severity(allure.severity_level.CRITICAL)
class TestSwap:
    @allure.title("Create swap definition object with valid params and get data")
    @pytest.mark.caseid("36762994")
    def test_get_swap_analytics_without_fields(self, open_session):
        response = swap_definition_02().get_data()
        check_http_status_is_success_and_df_value_not_empty(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create swap definition object with legs and get data")
    @pytest.mark.caseid("36763041")
    def test_get_swap_analytics_with_legs(self, open_session):
        response = swap_definition_01().get_data()
        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create swap definition object without any params and get data")
    @pytest.mark.caseid("36763075")
    def test_get_swap_analytics_with_empty_definition(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.swap.Definition().get_data()
        assert (
            str(error.value)
            == "Error code QPS-DPS.5004 | Invalid input: 'tenor' not specified or incorrect. Cannot extract Tenor value from instrumentCode."
        )

    @allure.title("Create swap definition object asynchronously")
    @pytest.mark.caseid("36763077")
    async def test_get_swap_analytics_asynchronously(self, open_session_async):
        response_01, response_02 = await get_async_response_from_definitions(
            swap_definition_01(), swap_definition_02()
        )
        check_http_status_is_success_and_df_value_not_empty(response_02)

    @allure.title("Create swap stream")
    @pytest.mark.caseid("36763080")
    def test_create_swap_stream(self, open_session):
        stream = swap_definition_01().get_stream()
        stream.open()

        check_stream_state_and_df_from_stream(stream)

    @allure.title("Create a swap definition with extended parameters")
    @pytest.mark.caseid("C37561644")
    def test_get_swap_with_extended_params(self, open_session):
        response = rdf.swap.Definition(
            tenor="5Y",
            legs=[
                rdf.swap.LegDefinition(
                    index_tenor="1Y",
                    interest_type=rdf.swap.InterestType.FLOAT,
                    interest_payment_frequency=rdf.swap.Frequency.QUARTERLY,
                    direction=rdf.swap.Direction.RECEIVED,
                    notional_ccy="GBP",
                ),
            ],
            extended_params={
                "instrumentDefinition": {
                    "InstrumentTag": "my tag",
                    "tenor": "2Y",
                    "legs": [
                        {
                            "direction": "Paid",
                            "interestType": "Float",
                            "notionalCcy": "EUR",
                            "notionalAmount": 1,
                            "interestPaymentFrequency": "Quarterly",
                        },
                        {
                            "direction": "Received",
                            "interestType": "Float",
                            "notionalCcy": "EUR",
                            "indexTenor": "5Y",
                            "interestPaymentFrequency": "Quarterly",
                        },
                    ],
                },
                "pricingParameters": {
                    "indexConvexityAdjustmentIntegrationMethod": "RiemannSum",
                    "indexConvexityAdjustmentMethod": "BlackScholes",
                    "valuationDate": "2020-06-01",
                },
            },
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == swap_universe
        ), f"Extended params are applied incorrectly"
        assert response.data.df.InstrumentTag[0] == "my tag"
