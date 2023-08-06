from datetime import timedelta, datetime

import allure
import pytest

from refinitiv.data.content import custom_instruments as ci
from refinitiv.data.content.custom_instruments._custom_instruments_data_provider import (
    get_user_id,
)
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason, Intervals
from tests.integration.content.custom_instruments.summaries.conftest import (
    get_summaries_definition_with_one_universe,
    get_summaries_definition_with_list_universes,
)
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_non_empty_response_data,
    check_response_status,
    check_response_is_success,
    check_response_values,
    check_universe_in_response,
)


@allure.suite("Content object - Custom Instrument")
@allure.feature("Custom Instrument Summaries")
@allure.severity(allure.severity_level.CRITICAL)
class TestCustomInstrumentSummaries:
    @allure.title(
        "Create Custom Instrument Summaries Definition object using a string/list of strings to define universe and "
        "IntradayInterval"
    )
    @pytest.mark.caseid(["C42991501", "C42991503"])
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "summaries_definition",
        [
            get_summaries_definition_with_one_universe,
            get_summaries_definition_with_list_universes,
        ],
    )
    def test_create_custom_instrument_summaries_object_with_universe_intraday_interval(
        self, open_desktop_session, summaries_definition, create_instrument
    ):
        definition, universes = summaries_definition(
            create_instrument, ci.Intervals.ONE_MINUTE
        )
        response = definition.get_data()
        check_universe_in_response(response, universes)

    @allure.title(
        "Create Custom Instrument Summaries Definition object using a string/list of strings to define universe and "
        "InterdayInterval"
    )
    @pytest.mark.caseid(["C42993448"])
    @pytest.mark.parametrize(
        "summaries_definition",
        [
            get_summaries_definition_with_one_universe,
            get_summaries_definition_with_list_universes,
        ],
    )
    def test_create_custom_instrument_summaries_object_with_universe_interday_interval(
        self, open_desktop_session, summaries_definition, create_instrument
    ):
        definition, universes = summaries_definition(
            create_instrument, ci.Intervals.DAILY
        )
        response = definition.get_data()
        check_universe_in_response(response, universes)

    @allure.title(
        "Create Custom Instrument Summaries Definition object using some valid optional parameters"
    )
    @pytest.mark.caseid("C42994114")
    @pytest.mark.parametrize(
        "start_date, end_date",
        [
            (timedelta(days=-90, hours=1), timedelta(0)),
            (timedelta(days=-90, hours=1), datetime.now()),
            ("2022-02-06T00:10:00", "2022-05-06T07:10:00"),
        ],
        ids=["timedelta", "datetime", "string"],
    )
    def test_create_custom_instrument_summaries_object_with_valid_optional_parameters(
        self, open_desktop_session, create_instrument, start_date, end_date
    ):
        instrument = create_instrument()
        response = ci.summaries.Definition(
            universe=[instrument],
            interval=ci.Intervals.WEEKLY,
            count=30,
            start=start_date,
            end=end_date,
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_values(
            response,
            expected_universe_ric=instrument,
            expected_interval=Intervals.WEEKLY,
            expected_summary_timestamp_label="endPeriod",
        )

    @allure.title(
        "Create Custom Instrument Summaries Definition object using invalid universe"
    )
    @pytest.mark.caseid("C42994133")
    @pytest.mark.parametrize("universe", ["invalid_universe"])
    def test_create_custom_instrument_summaries_object_with_invalid_universe(
        self, open_desktop_session, universe
    ):
        with pytest.raises(RDError) as error:
            ci.summaries.Definition(universe).get_data()
        assert (
            "Error code 1 | No data to return, please check errors: ERROR: No successful response.\n(404, CustomInstrument with symbol: S)invalid_universe)"
            == str(error.value)
        )

    @allure.title(
        "Create Custom Instrument Summaries Definition object using invalid Interval"
    )
    @pytest.mark.caseid("C42994652")
    @pytest.mark.parametrize("interval", ["invalid_interval"])
    def test_create_custom_instrument_summaries_object_using_invalid_interval(
        self, open_desktop_session, create_instrument, interval
    ):
        instrument = create_instrument()
        with pytest.raises(AttributeError) as error:
            ci.summaries.Definition(universe=instrument, interval=interval).get_data()

        assert (
            str(error.value)
            == f"Value '{interval}' must be in ['PT1M', 'PT5M', 'PT10M', 'PT30M', 'PT60M', 'PT1H', 'P1D', "
            f"'P7D', 'P1W', 'P1M', 'P3M', 'P12M', 'P1Y']"
        )

    @allure.title(
        "Create Custom Instrument Summaries Definition object when session is not open"
    )
    @pytest.mark.caseid("C42995388")
    def test_create_custom_instrument_summaries_object_with_session_not_opened(
        self, open_desktop_session, create_instrument
    ):
        session = open_desktop_session
        session.close()
        with pytest.raises(ValueError) as error:
            ci.summaries.Definition(universe="S)symbol").get_data()
        assert str(error.value) == "Session is not opened. Can't send any request"

    @allure.title(
        "Create Custom Instrument Summaries get data async with valid and invalid universe"
    )
    @pytest.mark.caseid("C42995791")
    @pytest.mark.parametrize("universe", ["invalid_universe"])
    async def test_custom_instrument_summaries_get_data_async(
        self, open_desktop_session_async, create_instrument, universe
    ):
        symbol = create_instrument()
        uuid = get_user_id()
        valid_response, invalid_response = await get_async_response_from_definitions(
            ci.summaries.Definition(symbol),
            ci.summaries.Definition(universe),
        )
        check_response_is_success(valid_response)
        check_non_empty_response_data(valid_response)
        check_response_status(
            response=valid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
        )
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.FOUR_HUNDRED_FOUR,
            expected_http_reason=HttpReason.NOT_FOUND,
            expected_error_code="404",
            expected_error_message=f"CustomInstrument with symbol: S){universe}.{uuid} for user: {uuid} not found!. "
            f"Requested ric: {universe}. Requested fields: None",
        )
