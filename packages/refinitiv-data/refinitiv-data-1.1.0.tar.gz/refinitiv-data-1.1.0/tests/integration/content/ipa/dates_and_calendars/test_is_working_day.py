from datetime import datetime, timedelta

import allure
import pytest

from refinitiv.data.content.ipa.dates_and_calendars import is_working_day
from refinitiv.data.content.ipa.dates_and_calendars.is_working_day import HolidayOutputs
from refinitiv.data.content.ipa.dates_and_calendars.is_working_day._is_working_day_data_provider import (
    WorkingDay,
)
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.helpers import (
    check_response_status,
    get_async_response_from_definitions,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_extended_params_were_sent_in_request,
)

first_definition = is_working_day.Definition(
    tag="my request",
    date="2022-01-01",
    calendars=["BAR", "KOR", "JAP"],
    currencies=["USD"],
    holiday_outputs=[HolidayOutputs.DATE, HolidayOutputs.NAMES],
)

second_definition = is_working_day.Definition(
    tag="my request",
    date="2021-12-25",
    calendars=["BAR"],
    currencies=["EUR"],
    holiday_outputs=[HolidayOutputs.DATE, HolidayOutputs.NAMES],
)

invalid_definition = is_working_day.Definition(
    date="2021.04.24",
    calendars=["JAP11"],
    holiday_outputs=[HolidayOutputs.DATE, HolidayOutputs.NAMES],
)


@allure.suite("Dates And Calendars")
@allure.feature("Content object - Is Working Day")
@allure.severity(allure.severity_level.CRITICAL)
class TestIsWorkingDay:
    @allure.title("Create a is_working_day definition with valid params")
    @pytest.mark.caseid("C46247467")
    @pytest.mark.parametrize(
        "date, calendars, currencies, holiday_outputs",
        [
            (
                "2018-12-31",
                ["UKR", "FRA"],
                ["EUR"],
                [HolidayOutputs.DATE, HolidayOutputs.NAMES, HolidayOutputs.COUNTRIES],
            ),
            (
                timedelta(-60),
                None,
                ["EUR"],
                ["Date", HolidayOutputs.NAMES, HolidayOutputs.COUNTRIES],
            ),
            (datetime(2022, 4, 13), ["UKR", "FRA"], None, ["Date", "Names"]),
        ],
    )
    def test_is_working_day_definition_with_valid_params(
        self,
        open_session,
        date,
        calendars,
        currencies,
        holiday_outputs,
    ):
        response = is_working_day.Definition(
            date=date,
            calendars=calendars,
            currencies=currencies,
            holiday_outputs=holiday_outputs,
        ).get_data()

        assert isinstance(response.data.day, WorkingDay)
        assert isinstance(response.data.day.holidays, list)
        assert isinstance(response.data.day.is_working_day, bool)

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(
            response, ["isWorkingDay", "isWeekEnd"]
        )

    @allure.title(
        "Create a is_working_day definition with valid and invalid definition asynchronously"
    )
    @pytest.mark.caseid("C46670891")
    async def test_is_working_day_definition_with_valid_and_invalid_def_async(
        self, open_session_async
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            first_definition, invalid_definition
        )

        check_non_empty_response_data(valid_response)
        check_response_status(
            response=valid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
        )

        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="IPA_library.ErrorBusinessCalendar_CalendarNotFound",
            expected_error_message="Business Calendar: calendar not found.",
        )

    @allure.title(
        "Create a is_working_day definition with invalid calendar and getting RDError"
    )
    @pytest.mark.parametrize(
        "expected_error",
        [
            (
                "Error code IPA_library.ErrorBusinessCalendar_CalendarNotFound | Business Calendar: calendar not found."
            )
        ],
    )
    @pytest.mark.caseid("C46247474")
    def test_is_working_day_definition_with_invalid_param(
        self, open_session, expected_error
    ):
        with pytest.raises(RDError) as error:
            is_working_day.Definition(
                date=datetime.now(),
                currencies=["UKR"],
            ).get_data()
        assert str(error.value) == expected_error

    @allure.title("Create is_working_day definition with extended params and get data")
    @pytest.mark.parametrize(
        "extended_param",
        [
            {
                "date": "2022-09-22",
                "calendars": ["USA"],
            }
        ],
    )
    @pytest.mark.caseid("C46247470")
    def test_is_working_day_definition_with_extended_params(
        self, open_session, extended_param
    ):
        response = is_working_day.Definition(
            tag="my request",
            date=timedelta(-360),
            calendars=["UKR", "FRA"],
            currencies=["EUR"],
            extended_params=extended_param,
        ).get_data()

        check_extended_params_were_sent_in_request(response, extended_param)
        check_non_empty_response_data(response)
        check_response_status(
            response=response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
        )

        assert response.data.day.is_working_day is True
        assert response.data.day.is_weekend is False

    @allure.title(
        "Create multi is_working_day definitions for working days and holidays and get data"
    )
    @pytest.mark.caseid("C46247473")
    def test_is_working_day_definitions_with_valid_def(self, open_session):
        response = is_working_day.Definitions(
            [first_definition, second_definition]
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(
            response, ["isWorkingDay", "isWeekEnd"]
        )

        assert isinstance(response.data.days, list)
        assert isinstance(response.data.days[0].holidays, list)
        assert response.data.days[0].is_working_day is False
