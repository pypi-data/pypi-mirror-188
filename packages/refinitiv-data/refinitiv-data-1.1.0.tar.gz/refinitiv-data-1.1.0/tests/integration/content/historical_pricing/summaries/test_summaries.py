from datetime import timedelta, datetime

import allure
import pytest

from refinitiv.data.content import historical_pricing
from refinitiv.data.content.historical_pricing import MarketSession
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason, Intervals
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_non_empty_response_data,
    check_response_status,
    check_response_is_success,
    check_response_values,
    check_universe_in_response,
    is_expected_param_in_request_url,
    check_index_column_contains_dates,
    check_universe_order_in_df,
    check_extended_params_were_sent_in_request,
)


@allure.suite("Historical Pricing Summaries")
@allure.feature("Historical Pricing Summaries")
@allure.severity(allure.severity_level.CRITICAL)
class TestHistoricalPricingSummaries:
    @allure.title(
        "Create HistoricalPricing Summaries Definition object using IntradayInterval and extended params"
    )
    @pytest.mark.parametrize(
        "universe,intervals,sessions,extended_params",
        [
            (
                "GBP=",
                historical_pricing.Intervals.ONE_MINUTE,
                [MarketSession.PRE, MarketSession.NORMAL, MarketSession.POST],
                None,
            ),
            (
                ["VOD.L", "GOOG.O", "LSEG.L"],
                "P1M",
                None,
                {"sessions": "pre,normal,post"},
            ),
        ],
    )
    @pytest.mark.caseid("33303593")
    def test_create_historical_pricing_summaries_object_with_universe_intraday_interval_and_extended_params(
        self,
        open_desktop_session,
        universe,
        intervals,
        sessions,
        extended_params,
    ):
        response = historical_pricing.summaries.Definition(
            universe,
            interval=intervals,
            count=200,
            sessions=sessions,
            extended_params=extended_params,
        ).get_data()
        check_universe_in_response(response, universe)
        check_index_column_contains_dates(response)
        check_universe_order_in_df(response, universe)
        check_extended_params_were_sent_in_request(response, extended_params)

    @allure.title(
        "Create HistoricalPricing Summaries Definition object using a string/list of strings to define universe and InterdayInterval"
    )
    @pytest.mark.caseid("33303593")
    @pytest.mark.parametrize(
        "universe,intervals",
        [("VOD.L", historical_pricing.Intervals.DAILY), (["VOD.L", "GOOG.O"], None)],
    )
    def test_create_historical_pricing_summaries_object_with_universe_interday_interval(
        self, open_desktop_session, universe, intervals
    ):
        response = historical_pricing.summaries.Definition(
            universe, interval=intervals
        ).get_data()

        check_universe_in_response(response, universe)
        check_index_column_contains_dates(response)

    @allure.title(
        "Create HistoricalPricing Summaries Definition object using some valid optional parameters"
    )
    @pytest.mark.caseid("33303594")
    @pytest.mark.parametrize(
        "universe, fields, start_date, end_date",
        [
            ("EUR=", ["DATE", "MKT_OPEN", "BID", "ASK"], timedelta(-3), timedelta(0)),
            ("EUR=", "BID", timedelta(hours=-100), datetime.now()),
            ("IBM", None, "2021-12-30T00:10:00", "2022-01-05T05:10:00"),
        ],
        ids=["timedelta", "datetime", "string"],
    )
    def test_create_historical_pricing_summaries_object_with_valid_optional_parameters(
        self, open_desktop_session, universe, fields, start_date, end_date
    ):
        response = historical_pricing.summaries.Definition(
            universe,
            interval=historical_pricing.Intervals.DAILY,
            adjustments=historical_pricing.Adjustments.CCH,
            count=5,
            fields=fields,
            start=start_date,
            end=end_date,
        ).get_data()
        is_expected_param_in_request_url(response, ["start", "end"])
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_values(
            response,
            expected_universe_ric=universe,
            expected_interval=Intervals.DAILY,
            expected_summary_timestamp_label="endPeriod",
        )

    @allure.title(
        "Create HistoricalPricing Summaries Definition object using invalid universe"
    )
    @pytest.mark.caseid("33303595")
    @pytest.mark.parametrize("universe", ["VOD.invalid"])
    def test_create_historical_pricing_summaries_object_with_invalid_universe(
        self, open_desktop_session, universe
    ):
        with pytest.raises(RDError) as error:
            historical_pricing.summaries.Definition(universe).get_data()
        assert (
            str(error.value)
            == "Error code 1 | No data to return, please check errors: ERROR: No successful "
            "response.\n"
            "(TS.Interday.UserRequestError.70005, The universe is not found)"
        )

    @allure.title(
        "Create HistoricalPricing Summaries Definition object using invalid Interval"
    )
    @pytest.mark.caseid("33303596")
    @pytest.mark.parametrize("universe", ["VOD.L"])
    def test_create_historical_pricing_summaries_object_using_invalid_interval(
        self, open_desktop_session, universe
    ):
        """
        we have different with TS lib, when creating a request using invalid Interval in TS lib expected status code 400
        in python lib we receive AttributeError "interval must be in ['PT1M', 'PT5M', 'PT10M', 'PT30M', 'PT60M', 'PT1H',
        'P1D', 'P7D', 'P1W', 'P1M', 'P3M', 'P12M', 'P1Y']"
        this test case only catch AttributeError, if AttributeError not rise we assert on http status code
        """
        with pytest.raises(AttributeError) as error:
            historical_pricing.summaries.Definition(
                universe, interval="INVALID"
            ).get_data()
        assert (
            str(error.value)
            == "Value 'INVALID' must be in ['PT1M', 'PT5M', 'PT10M', 'PT30M', 'PT60M', 'PT1H', "
            "'P1D', 'P7D', 'P1W', 'P1M', 'P3M', 'P12M', 'P1Y']"
        )

    @allure.title(
        "Create HistoricalPricing Summaries Definition object when session is not open"
    )
    @pytest.mark.parametrize("universe", ["VOD.L"])
    def test_create_historical_pricing_summaries_object_with_session_not_opened(
        self, universe, open_desktop_session
    ):
        session = open_desktop_session
        session.close()
        historical_pricing_definition = historical_pricing.summaries.Definition(
            universe
        )
        with pytest.raises(ValueError) as error:
            historical_pricing_definition.get_data()
        assert str(error.value) == "Session is not opened. Can't send any request"

    @allure.title(
        "Create Historical Pricing Summaries get data async with valid and invalid universe"
    )
    @pytest.mark.parametrize(
        "universe,invalid_universe", [(["VOD.L", "INVALID"], "INVALID")]
    )
    @pytest.mark.caseid("39746370")
    async def test_get_data_async(
        self, open_desktop_session_async, universe, invalid_universe
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            historical_pricing.summaries.Definition(universe),
            historical_pricing.summaries.Definition(invalid_universe),
        )
        check_response_is_success(valid_response)
        check_non_empty_response_data(valid_response)
        check_response_status(
            response=valid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="TS.Interday.UserRequestError.70005",
            expected_error_message="The universe is not found.. Requested ric: INVALID. Requested fields: None",
        )
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="TS.Interday.UserRequestError.70005",
            expected_error_message="The universe is not found.. Requested ric: INVALID. Requested fields: None",
        )
