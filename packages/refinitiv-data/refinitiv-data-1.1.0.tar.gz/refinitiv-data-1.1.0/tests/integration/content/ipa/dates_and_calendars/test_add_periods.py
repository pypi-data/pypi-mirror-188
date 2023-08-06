from datetime import datetime, timedelta

import allure
import pytest

from refinitiv.data.content.ipa.dates_and_calendars import add_periods
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

EXPECTED_COLUMN_NAMES = [
    "date",
    "tag",
]


first_definition = add_periods.Definition(
    tag="my request 1",
    start_date=timedelta(-180),
    period="4D",
    calendars=["BAR", "KOR", "JAP"],
    currencies=["USD"],
    date_moving_convention="NextBusinessDay",
    end_of_month_convention="Last",
    holiday_outputs=["Date", "Calendars", "Countries", "Names"],
)

second_definition = add_periods.Definition(
    tag="my request 2",
    start_date="2020-04-24",
    period="4D",
    calendars=["BAR", "KOR", "JAP"],
    currencies=["USD"],
    date_moving_convention=add_periods.DateMovingConvention.NEXT_BUSINESS_DAY,
    end_of_month_convention="Last",
    holiday_outputs=[
        add_periods.HolidayOutputs.DATE,
        add_periods.HolidayOutputs.CALENDARS,
        add_periods.HolidayOutputs.NAMES,
    ],
)

invalid_definition = add_periods.Definition(
    tag="my request 2", start_date="2023.04.24", period="inval"
)


@allure.suite("Dates And Calendars")
@allure.feature("Content object - Add Periods")
@allure.severity(allure.severity_level.CRITICAL)
class TestAddPeriods:
    @allure.title("Create a add_periods definition with valid params")
    @pytest.mark.caseid("C45475716")
    @pytest.mark.parametrize(
        "start_date, calendars, currencies, holiday_outputs, end_of_month_convention",
        [
            (
                "2018-12-31",
                ["UKR", "FRA"],
                ["EUR"],
                ["Date", "Names", "Calendars", "Countries"],
                add_periods.EndOfMonthConvention.LAST,
            ),
            (
                timedelta(-180),
                ["UKR", "FRA"],
                None,
                add_periods.HolidayOutputs.NAMES,
                "Same",
            ),
            (timedelta(-180), None, ["USD"], ["Date", "Calendars", "Names"], None),
            (
                datetime(2019, 4, 13),
                None,
                ["USD"],
                None,
                add_periods.EndOfMonthConvention.LAST28,
            ),
        ],
    )
    def test_add_periods_definition_with_valid_params(
        self,
        open_session,
        start_date,
        calendars,
        currencies,
        holiday_outputs,
        end_of_month_convention,
    ):
        response = add_periods.Definition(
            tag="my request",
            period="4D",
            start_date=start_date,
            calendars=calendars,
            currencies=currencies,
            holiday_outputs=holiday_outputs,
            date_moving_convention=add_periods.DateMovingConvention.NEXT_BUSINESS_DAY,
            end_of_month_convention=end_of_month_convention,
        ).get_data()

        assert isinstance(response.data.added_period.holidays, list)
        assert response.data.added_period.tag == "my request"
        assert response.data.added_period.date is not None

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, EXPECTED_COLUMN_NAMES)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create a add_periods definition with valid and invalid definition asynchronously"
    )
    @pytest.mark.caseid("C46335537")
    async def test_add_periods_definition_with_valid_and_invalid_def_async(
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
            expected_error_message="Invalid input: at least one currency code or calendar code must be specified.",
        )

    @allure.title(
        "Create a add_periods definitions with valid and invalid definition and getting RDError"
    )
    @pytest.mark.parametrize(
        "expected_error",
        [
            (
                "Error code 400 | Invalid input: at least one currency code or calendar code must be specified."
            )
        ],
    )
    @pytest.mark.caseid("C45475872")
    def test_add_periods_definitions_with_valid_and_invalid_def(
        self, open_session, expected_error
    ):
        with pytest.raises(RDError) as error:
            add_periods.Definitions(
                [first_definition, second_definition, invalid_definition]
            ).get_data()
        assert str(error.value) == expected_error

    @allure.title(
        "Create a add_periods definitions with valid and invalid definition params asynchronously"
    )
    @pytest.mark.caseid("C46335532")
    async def test_add_periods_definitions_with_valid_and_invalid_def_async(
        self, open_session_async
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            add_periods.Definitions([first_definition, second_definition]),
            add_periods.Definitions(invalid_definition),
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
            expected_error_message="Invalid input: at least one currency code or calendar code must be specified.",
        )

    @allure.title("Create add_periods definition with extended params and get data")
    @pytest.mark.parametrize(
        "extended_param",
        [
            {
                "tag": "new tag",
                "startDate": "2022-07-04",
                "holidayOutputs": ["Date"],
            }
        ],
    )
    @pytest.mark.caseid("C45475718")
    def test_add_periods_definition_with_extended_params(
        self, open_session, extended_param
    ):
        response = add_periods.Definition(
            tag="my request",
            period="4D",
            start_date=timedelta(-360),
            calendars=["UKR", "FRA"],
            currencies=["EUR"],
            holiday_outputs=["Date", "Names", "Calendars", "Countries"],
            extended_params=extended_param,
        ).get_data()

        check_extended_params_were_sent_in_request(response, extended_param)
        check_non_empty_response_data(response)
        check_response_status(
            response=response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
        )

    @allure.title("Create an add_periods definition with closed session and get error")
    @pytest.mark.parametrize(
        "expected_error",
        ["Session is not opened. Can't send any request"],
    )
    @pytest.mark.caseid("C45475868")
    def test_add_periods_definition_with_closed_session(
        self, expected_error, open_platform_session
    ):
        session = open_platform_session
        session.close()
        with pytest.raises(ValueError) as error:
            first_definition.get_data()
        assert str(error.value) == expected_error
