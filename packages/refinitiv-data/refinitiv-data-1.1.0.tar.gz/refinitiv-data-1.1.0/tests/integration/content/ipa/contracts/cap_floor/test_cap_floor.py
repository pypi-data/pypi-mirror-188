import allure
import pytest
import json

import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery._stream import stream_cxn_cache
from refinitiv.data.errors import RDError
from tests.integration.conftest import is_open
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.ipa.contracts.cap_floor.conftest import (
    cap_floor_on_cms_definition,
    cap_floor_coller_pos_definition,
    cap_floor_amortized_definition,
    invalid_cap_floor_definition,
    cap_floor_universe,
)
from tests.integration.content.ipa.contracts.conftest import (
    check_http_status_is_success_and_df_value_not_empty,
    check_stream_state_and_df_from_stream,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_response_status,
    check_dataframe_column_date_for_datetime_type,
)


@allure.suite("Content object - CapFloor")
@allure.feature("Content object - CapFloor")
@allure.severity(allure.severity_level.CRITICAL)
class TestCapFloor:
    @allure.title("Create a cap_floor definition object with params and get data")
    @pytest.mark.caseid("36325567")
    @pytest.mark.parametrize(
        "cap_floor_definition",
        [
            cap_floor_on_cms_definition,
            cap_floor_coller_pos_definition,
            cap_floor_amortized_definition,
        ],
    )
    def test_get_cap_floor_analytics(self, open_session, cap_floor_definition):
        response = cap_floor_definition().get_data()
        check_http_status_is_success_and_df_value_not_empty(response)

    @allure.title("Create a cap_floor definition without any parameters")
    @pytest.mark.caseid("36325572")
    def test_get_cap_floor_analytics_without_any_parameters(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.cap_floor.Definition().get_data()
        assert (
            str(error.value)
            == "Error code QPS-DPS.1005 | Mandatory input missing: Notional currency is mandatory."
        )

    @allure.title("Create a cap_floor definition with empty pricing parameters")
    @pytest.mark.caseid("36325576")
    def test_get_cap_floor_with_empty_pricing_params(self, open_session):
        response = rdf.cap_floor.Definition(
            notional_ccy="EUR",
            start_date="2019-02-11",
            tenor="5Y",
            index_tenor="1M",
            buy_sell="Sell",
            floor_strike_percent=1,
            pricing_parameters=rdf.cap_floor.PricingParameters(),
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create a cap_floor definition with extended parameters")
    @pytest.mark.caseid("36325578")
    def test_get_cap_floor_with_extended_params(self, open_session):
        response = rdf.cap_floor.Definition(
            instrument_tag="CapGBP",
            amortization_schedule=[
                rdf.cap_floor.AmortizationItem(
                    start_date="2023-06-12",
                    end_date="2024-06-12",
                    amount=100000,
                    amortization_type="Schedule",
                    amortization_frequency=rdf.cap_floor.AmortizationFrequency.EVERY_COUPON,
                ),
                rdf.cap_floor.AmortizationItem(
                    start_date="2024-06-11",
                    end_date="2025-06-11",
                    amount=-100000,
                    amortization_type="Schedule",
                    amortization_frequency=rdf.cap_floor.AmortizationFrequency.EVERY_COUPON,
                ),
            ],
            fields=[
                "InstrumentTag",
                "InstrumentDescription",
                "FixedRate",
                "MarketDataDate",
                "MarketValueInDealCcy",
                "MarketValueInReportCcy",
                "ErrorMessage",
                "MarketDataDate",
            ],
            extended_params={
                "instrumentDefinition": {
                    "startDate": "2021-06-11",
                    "tenor": "10Y",
                    "notionalCcy": "GBP",
                    "notionalAmount": 10000000,
                    "interestPaymentFrequency": "Quarterly",
                    "buySell": "Buy",
                    "capStrikePercent": 0.25,
                },
                "pricingParameters": {
                    "marketDataDate": "2020-10-07",
                    "skipFirstCapFloorlet": False,
                    "valuationDate": "2021-10-07",
                },
            },
        ).get_data()

        check_http_status_is_success_and_df_value_not_empty(response)

        request = json.loads(response.request_message.content.decode("utf-8"))
        request_universe = request.get("universe")[0]
        assert (
            request_universe == cap_floor_universe
        ), f"Extended params are applied incorrectly"

    @allure.title("Create a cap_floor definition with invalid extended parameters")
    @pytest.mark.caseid("36325581")
    def test_get_cap_floor_with_invalid_extended_params(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.cap_floor.Definition(
                notional_ccy="EUR",
                cap_strike_percent=1,
                fields=["InstrumentTag"],
                extended_params={"fields": "INVALID"},
            ).get_data()
        assert str(error.value)

    @allure.title("Create a cap_floor definition request asynchronously")
    @pytest.mark.caseid("36325638")
    async def test_cap_floor_definition_asynchronously(self, open_session_async):
        valid_response, invalid_response = await get_async_response_from_definitions(
            cap_floor_coller_pos_definition(), invalid_cap_floor_definition()
        )

        check_http_status_is_success_and_df_value_not_empty(valid_response)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_message="Market data error : Invalid fixing source for provided index currency. No matching fixing for INVAL",
        )

    @allure.title("Create a cap_floor stream")
    @pytest.mark.caseid("36325639")
    @pytest.mark.smoke
    def test_cap_floor_stream(self, open_session):
        stream = cap_floor_coller_pos_definition().get_stream()
        stream.open()

        check_stream_state_and_df_from_stream(stream)

    @allure.title(
        "Receiving cap_floor data when the session was interrupted during the process"
    )
    @pytest.mark.caseid("36325652")
    def test_cap_floor_data_when_session_was_interrupted(self, open_session):
        session = open_session
        stream = cap_floor_amortized_definition().get_stream()
        stream.open()
        session.close()

        is_cxn_alive = stream_cxn_cache.is_cxn_alive(
            session, ContentType.STREAMING_CONTRACTS
        )

        assert not is_cxn_alive, f"Connection is alive"
        assert not is_open(stream), f"Stream is open"

    @allure.title("Create cap_floor definition and get data for the invalid params")
    @pytest.mark.caseid("36325581")
    def test_get_cap_floor_with_invalid_params(self, open_session):
        with pytest.raises(RDError) as error:
            rdf.cap_floor.Definition(
                notional_ccy="INVALIDCCY",
                buy_sell=rdf.cap_floor.BuySell.SELL,
                cap_strike_percent=1,
                tenor="5Y",
            ).get_data()
        assert (
            str(error.value)
            == "Error code QPS-DPS.3001 | Market data error : Invalid fixing source for provided index currency. No matching fixing for INVALIDCCY"
        )
