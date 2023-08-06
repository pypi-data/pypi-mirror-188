from datetime import datetime, timedelta

import allure
import numpy
import pytest

from refinitiv.data.content.ipa.dates_and_calendars import date_schedule
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.helpers import (
    check_response_status,
    get_async_response_from_definitions,
    check_dataframe_column_date_for_datetime_type,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
    check_extended_params_were_sent_in_request,
)

first_definition = date_schedule.Definition(
    start_date=timedelta(-180),
    end_date=timedelta(-10),
    calendars=["BAR", "KOR", "JAP"],
    currencies=["USD"],
    frequency=date_schedule.DateScheduleFrequency.WEEKLY,
    day_of_week=date_schedule.DayOfWeek.MONDAY,
)


invalid_definition = date_schedule.Definition(
    start_date="2021.04.24",
    end_date=timedelta(-10),
    calendars=["BAR", "KOR", "JAP"],
    frequency=date_schedule.DateScheduleFrequency.WEEKLY,
)


@allure.suite("Dates And Calendars")
@allure.feature("Content object - Date Schedule")
@allure.severity(allure.severity_level.CRITICAL)
class TestDateSchedule:
    @allure.title("Create a date_schedule definition with valid params")
    @pytest.mark.caseid("C45666963")
    @pytest.mark.parametrize(
        "start_date, end_date, calendars, currencies, count, frequency, day_of_week",
        [
            (
                "2018-12-31",
                "2019-12-31",
                ["UKR", "FRA"],
                ["EUR"],
                None,
                date_schedule.DateScheduleFrequency.WEEKLY,
                date_schedule.DayOfWeek.MONDAY,
            ),
            (
                timedelta(-60),
                timedelta(0),
                ["UKR", "FRA"],
                ["EUR"],
                None,
                "Daily",
                None,
            ),
            (
                datetime(2019, 4, 13),
                None,
                ["UKR", "FRA"],
                ["EUR"],
                20,
                "BiWeekly",
                "Wednesday",
            ),
            ("2019-12-31", datetime.now(), None, ["EUR"], None, "BiWeekly", "Friday"),
        ],
    )
    def test_date_schedule_definition_with_valid_params(
        self,
        open_session,
        start_date,
        end_date,
        calendars,
        currencies,
        count,
        frequency,
        day_of_week,
    ):
        response = date_schedule.Definition(
            start_date=start_date,
            end_date=end_date,
            calendars=calendars,
            currencies=currencies,
            count=count,
            frequency=frequency,
            day_of_week=day_of_week,
        ).get_data()

        assert isinstance(response.data.dates, list)
        assert isinstance(response.data.dates[0], numpy.datetime64)

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, ["dates"])
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create a date_schedule definition with valid and invalid definition asynchronously"
    )
    @pytest.mark.caseid("C46670889")
    async def test_date_schedule_definition_with_valid_and_invalid_def_async(
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
            expected_status_code=HttpStatusCode.FOUR_HUNDRED,
            expected_http_reason=HttpReason.BAD_REQUEST,
            expected_error_code=HttpStatusCode.FOUR_HUNDRED,
            expected_error_message="Invalid input: 'dayOfWeek' must be specified when 'frequency' is set to 'Weekly' or 'BiWeekly'",
        )

    @allure.title("Create a date_schedule with end_date and count fields and get error")
    @pytest.mark.parametrize(
        "expected_error",
        [
            (
                "Error code 400 | Invalid input: only one of 'endDate' or 'count' must be set."
            )
        ],
    )
    @pytest.mark.caseid("C45667021")
    def test_date_schedule_definition_with_invalid_param(
        self, open_session, expected_error
    ):
        with pytest.raises(RDError) as error:
            date_schedule.Definition(
                start_date="2018-12-31",
                end_date="2019-12-31",
                calendars=["UKR", "FRA"],
                count=5,
                frequency=date_schedule.DateScheduleFrequency.WEEKLY,
                day_of_week=date_schedule.DayOfWeek.MONDAY,
            ).get_data()
        assert str(error.value) == expected_error

    @allure.title("Create date_schedule definition with extended params and get data")
    @pytest.mark.parametrize(
        "extended_param",
        [
            {
                "startDate": "2022-07-04",
                "calendars": ["USA"],
            }
        ],
    )
    @pytest.mark.caseid("C45666968")
    def test_date_schedule_definition_with_extended_params(
        self, open_session, extended_param
    ):
        response = date_schedule.Definition(
            start_date=timedelta(-360),
            end_date="2022-08-31",
            calendars=["UKR", "FRA"],
            currencies=["EUR"],
            extended_params=extended_param,
            frequency=date_schedule.DateScheduleFrequency.WEEKLY,
            day_of_week=date_schedule.DayOfWeek.MONDAY,
        ).get_data()

        check_extended_params_were_sent_in_request(response, extended_param)
        check_non_empty_response_data(response)
        check_response_status(
            response=response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
        )
