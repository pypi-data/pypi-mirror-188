from datetime import timedelta, datetime

import allure
import pytest

from refinitiv.data.content import custom_instruments as ci
from refinitiv.data.content.custom_instruments._custom_instruments_data_provider import (
    get_user_id,
)
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.helpers import (
    get_async_response_from_definitions,
    assert_error,
    check_response_status,
    check_non_empty_response_data,
    check_response_data_start_end_date,
    is_universe_empty,
    check_response_is_success,
    check_response_data_universe,
    is_expected_param_in_request_url,
    check_index_column_contains_dates,
)


@allure.suite("Content object - Custom Instrument")
@allure.feature("Custom Instrument Events")
@allure.severity(allure.severity_level.CRITICAL)
class TestCustomInstrumentEvents:
    @allure.title("Create Custom Instrument events definition and get data")
    @pytest.mark.caseid(["C42988157", "C42988703"])
    @pytest.mark.smoke
    def test_custom_instrument_events_and_get_data(
        self, open_session_with_rdp_creds_for_ci, create_instrument
    ):
        instrument = create_instrument()
        response = ci.events.Definition(universe=instrument, count=15).get_data()
        check_response_is_success(response)
        check_non_empty_response_data(response)
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        assert len(response.data.raw["data"]) == 15, (
            f"Custom Instrument event dataframe size is not as expected: "
            f"{response.data.raw['data']} != {15}"
        )
        check_index_column_contains_dates(response)

    @allure.title(
        "Create Custom Instrument multi-request events definition and get data with interval"
    )
    @pytest.mark.caseid("C42991351")
    @pytest.mark.parametrize(
        "start_date, end_date",
        [
            (timedelta(hours=-10), timedelta(0)),
            (timedelta(hours=3), datetime.now()),
            ("2022-12-08T05:00:00", "2022-12-09T07:10:00"),
        ],
        ids=["timedelta", "datetime", "string"],
    )
    def test_custom_instrument_events_get_data_with_interval(
        self, open_desktop_session, create_instrument, start_date, end_date, request
    ):
        if "datetime" in request.node.callspec.id:
            start_date = end_date - start_date

        instrument_01 = create_instrument()
        instrument_02 = create_instrument()
        response = ci.events.Definition(
            universe=[instrument_01, instrument_02],
            start=start_date,
            end=end_date,
            count=13000,
        ).get_data()
        is_expected_param_in_request_url(response, ["start", "end"])
        check_response_is_success(response)
        check_non_empty_response_data(response)
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_data_universe(response, [instrument_01, instrument_02])
        check_response_data_start_end_date(response, start_date, end_date, request)
        check_index_column_contains_dates(response)

    @allure.title(
        "Create Custom Instrument events definition get data with mix of valid and invalid universe"
    )
    @pytest.mark.caseid("C42991486")
    def test_custom_instrument_events_get_data_with_mix_of_valid_and_invalid_universe(
        self, open_desktop_session, create_instrument
    ):
        instrument = create_instrument()
        response = ci.events.Definition([instrument, "invalid_universe"]).get_data()
        check_response_is_success(response)
        assert not is_universe_empty(response.data.df, instrument)
        assert is_universe_empty(response.data.df, "invalid_universe")

    @allure.title("Custom Instrument events definition - get data without universe")
    @pytest.mark.caseid("C42991497")
    def test_custom_instrument_events_get_data_without_universe(self):
        with pytest.raises(TypeError) as error:
            ci.events.Definition()
        assert_error(error, "universe")

    @allure.title(
        "Create Custom Instrument events get data async with valid and invalid universe"
    )
    @pytest.mark.caseid("C42991499")
    async def test_custom_instrument_events_get_data_async(
        self, open_desktop_session_async, create_instrument
    ):
        instrument = create_instrument()
        uuid = get_user_id()
        valid_response, invalid_response = await get_async_response_from_definitions(
            ci.events.Definition(instrument),
            ci.events.Definition("invalid_universe"),
        )
        check_response_is_success(valid_response)
        check_non_empty_response_data(valid_response)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.FOUR_HUNDRED_FOUR,
            expected_http_reason=HttpReason.NOT_FOUND,
            expected_error_code="404",
            expected_error_message=f"CustomInstrument with symbol: S)invalid_universe.{uuid} for user: {uuid} "
            f"not found!. Requested ric: invalid_universe. Requested fields: None",
        )
