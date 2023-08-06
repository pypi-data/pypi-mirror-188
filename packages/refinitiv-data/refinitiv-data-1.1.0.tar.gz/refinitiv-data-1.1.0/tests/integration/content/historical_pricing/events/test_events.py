from datetime import timedelta, datetime

import allure
import pytest

from refinitiv.data.content.historical_pricing import events, Adjustments, EventTypes
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.historical_pricing.events.conftest import (
    check_response_data_fields,
    check_response_data_event_type,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_non_empty_response_data,
    check_response_status,
    assert_error,
    check_response_data_start_end_date,
    is_universe_empty,
    check_response_is_success,
    check_response_data_universe,
    is_expected_param_in_request_url,
    check_extended_params_were_sent_in_request,
)


@allure.suite("Historical Pricing Events")
@allure.feature("Historical Pricing Events")
@allure.severity(allure.severity_level.CRITICAL)
class TestHistoricalPricingEvents:
    @allure.title("Pricing event definition - get data")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "universe, fields, count",
        [[["VOD.L", "GOOG.O"], ["BID", "BIDSIZE", "ASK"], 42]],
    )
    @pytest.mark.caseid("С37902412")
    def test_get_data(self, open_desktop_session, universe, fields, count):
        response = events.Definition(universe, fields=fields, count=count).get_data()
        check_response_is_success(response)
        check_response_data_universe(response, universe)
        check_response_data_fields(response, fields)
        assert len(response.data.raw[0]["data"]) == count, (
            f"Pricing dataframe size is not as expected: "
            f"{response.data.raw[0]['data']} != {count}"
        )

    @allure.title("Pricing event definition - get data with interval")
    @pytest.mark.parametrize(
        "universe, fields, start_date, end_date, event_type",
        [
            (
                "LSEG.L",
                ["EVENT_TYPE", "BID", "ASK"],
                timedelta(-1),
                timedelta(0),
                "trade",
            ),
            ("VOD.L", None, timedelta(hours=-24), datetime.now(), EventTypes.QUOTE),
            ("EUR=", None, "2022-12-18T10:00:00", "2022-12-19T16:00:00", "quote"),
        ],
        ids=["timedelta", "datetime", "string"],
    )
    @pytest.mark.caseid("C37902415")
    def test_get_data_with_interval(
        self,
        open_desktop_session,
        universe,
        fields,
        start_date,
        end_date,
        event_type,
        request,
    ):
        response = events.Definition(
            universe,
            fields=fields,
            start=start_date,
            end=end_date,
            eventTypes=event_type,
            count=13000,
        ).get_data()
        is_expected_param_in_request_url(response, ["start", "end"])
        check_response_is_success(response)
        check_response_data_start_end_date(response, start_date, end_date, request)
        check_response_data_event_type(response, event_type)

    @allure.title(
        "Pricing event definition - get data with mix of valid and invalid universe"
    )
    @pytest.mark.parametrize(
        "universe",
        [["IBM", "WRONG_UNIVERSE"]],
    )
    @pytest.mark.caseid("C38941492")
    def test_get_data_with_mix_of_valid_and_invalid_universe(
        self,
        open_desktop_session,
        universe,
    ):
        response = events.Definition(universe).get_data()
        check_response_is_success(response)
        assert not is_universe_empty(response.data.df, universe[0])
        assert is_universe_empty(response.data.df, universe[1])

    @allure.title("Pricing event definition - get data without universe")
    @pytest.mark.caseid("C37913678")
    def test_get_data_without_universe(self):
        with pytest.raises(
            TypeError,
        ) as error:
            events.Definition()

        assert_error(error, "universe")

    @allure.title("Pricing event definition - get data with incorrect parameters")
    @pytest.mark.parametrize(
        "universe, fields, start, end, event_type",
        [["123", ["QWE"], "2021-12-01T00:00:00", "2020-12-07T00:10:00", "asd"]],
    )
    @pytest.mark.caseid("C37902416")
    def test_get_data_with_incorrect_parameters(
        self, open_desktop_session, universe, fields, start, end, event_type
    ):
        with pytest.raises(RDError) as error:
            events.Definition("IBM", fields=fields).get_data()
        assert "The universe does not support the following fields" in str(error.value)

        with pytest.raises(RDError) as error:
            events.Definition("IBM", start=start, end=end).get_data()
        assert "Request Validation Error" in str(error.value)

    @allure.title(
        "Create Historical Pricing Events get data async with valid and invalid universe"
    )
    @pytest.mark.parametrize("universe,invalid_universe", [("VOD.L", "INVALID")])
    @pytest.mark.caseid("C38941498")
    async def test_get_data_async(
        self, open_desktop_session_async, universe, invalid_universe
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            events.Definition(universe), events.Definition(invalid_universe)
        )
        check_response_is_success(valid_response)
        check_non_empty_response_data(valid_response)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="TS.Intraday.UserRequestError.90001",
            expected_error_message="INVALID - The universe is not found",
        )

    @allure.title("Pricing event definition - get partial data with extended params")
    @pytest.mark.parametrize(
        "universe,fields,adjustments,extended_params",
        [
            (
                "GBP=",
                ["BID", "ASK"],
                None,
                {"count": "50", "adjustments": "exchangeCorrection,manualCorrection"},
            ),
            (
                "GBP=",
                "ASK",
                [
                    Adjustments.EXCHANGE_CORRECTION,
                    Adjustments.MANUAL_CORRECTION,
                    Adjustments.QUALIFIERS,
                ],
                None,
            ),
        ],
    )
    @pytest.mark.caseid("C37902415")
    def test_get_data_with_extended_params_and_partial_data(
        self, open_desktop_session, universe, fields, adjustments, extended_params
    ):
        response = events.Definition(
            universe=universe,
            fields=fields,
            adjustments=adjustments,
            start=timedelta(hours=-1),
            end=timedelta(0),
            extended_params=extended_params,
        ).get_data()
        check_response_is_success(response)
        check_non_empty_response_data(response)
        check_response_status(
            response=response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="TS.Intraday.Warning.95004",
            expected_error_message=f"{universe} - Trades interleaving with corrections is currently not supported. Corrections will not be returned.",
        )
        check_extended_params_were_sent_in_request(response, extended_params)
