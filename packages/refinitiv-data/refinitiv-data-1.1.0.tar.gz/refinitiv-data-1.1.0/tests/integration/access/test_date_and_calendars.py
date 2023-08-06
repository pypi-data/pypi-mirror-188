from datetime import datetime, timedelta

import allure
import numpy
import pandas as pd
import pytest
from pandas._libs.tslibs.offsets import CustomBusinessDay

from refinitiv.data import dates_and_calendars
from tests.integration.helpers import (
    check_response_dataframe_contains_columns_names,
    check_dataframe_column_date_for_datetime_type,
)
from refinitiv.data._fin_coder_layer.dates_and_calendars._count_periods import (
    CountedPeriods,
)

end_date = datetime.utcnow()
start_date = end_date - timedelta(days=130)


@allure.suite("FinCoder layer")
@allure.feature("FinCoder - Date and Calendars")
@allure.severity(allure.severity_level.CRITICAL)
class TestDateAndCalendars:
    @allure.title("Create add_periods and get data")
    @pytest.mark.caseid("C53990671")
    def test_add_periods_and_get_data(self, open_session):
        response = dates_and_calendars.add_periods(
            start_date=start_date,
            period="4D",
            calendars=["BAR", "KOR", "JAP"],
            currencies=["USD"],
            date_moving_convention="NextBusinessDay",
            end_of_month_convention="Last28",
        )

        assert isinstance(response, numpy.datetime64)

    @allure.title("Create count_periods and get data")
    @pytest.mark.caseid("C53990673")
    def test_count_periods_and_get_data(self, open_session):
        response = dates_and_calendars.count_periods(
            start_date=timedelta(-30),
            end_date=end_date,
            period_type=dates_and_calendars.PeriodType.DAY,
            calendars=["EMU"],
            currencies=["USD"],
            day_count_basis=dates_and_calendars.DayCountBasis.DCB_ACTUAL_ACTUAL,
        )

        assert isinstance(response, CountedPeriods)
        assert isinstance(response.count, float)
        assert response.tenor is not None

    @allure.title("Create date_schedule and get data")
    @pytest.mark.caseid("C53990674")
    def test_date_schedule_and_get_data(self, open_session):
        response = dates_and_calendars.date_schedule(
            start_date=start_date,
            calendars=["EMU"],
            count=10,
            frequency=dates_and_calendars.DateScheduleFrequency.WEEKLY,
            day_of_week=dates_and_calendars.DayOfWeek.MONDAY,
        )

        for date in response:
            assert isinstance(date, numpy.datetime64)

    @allure.title("Create is_working_day and get data")
    @pytest.mark.caseid("C53990675")
    def test_is_working_day_and_get_data(self, open_session):
        response = dates_and_calendars.is_working_day(
            date="22-09-01",
            currencies=["UAH"],
            calendars=["UKR", "FRA"],
        )

        assert type(response) == bool
        assert not response

    @allure.title("Create holidays and check data with offset")
    @pytest.mark.parametrize(
        "expected_columns,expected_calendars,expected_bd_range",
        [
            (
                [
                    "name",
                    "calendars",
                    "countries",
                    "tag",
                    "date",
                ],
                ["UKR", "FRA", "USA", "EMU"],
                [
                    "2019-12-02",
                    "2019-12-03",
                    "2019-12-04",
                    "2019-12-05",
                    "2019-12-06",
                    "2019-12-09",
                    "2019-12-10",
                ],
            )
        ],
    )
    @pytest.mark.caseid("C53990690")
    def test_holidays_and_get_data(
        self, open_session, expected_columns, expected_calendars, expected_bd_range
    ):
        response = dates_and_calendars.holidays(
            start_date="2018-12-31",
            end_date="2020-01-01",
            calendars=["UKR", "FRA"],
            currencies=["USD", "EUR"],
        )

        usa_bd_range = pd.date_range(
            start="2019-12-01", end="2019-12-10", freq=response.calendars["USA"].offset
        )

        for date in usa_bd_range:
            date = date.strftime("%Y-%m-%d")
            assert (
                date in expected_bd_range
            ), f"Date {date} is not in the expected date range"

        for calendars in expected_calendars:
            assert (
                calendars in response.calendars
            ), f"{calendars} doesn`t exist in the response"

        assert isinstance(response.offset, CustomBusinessDay)
        check_response_dataframe_contains_columns_names(response, expected_columns)
        check_dataframe_column_date_for_datetime_type(response)
