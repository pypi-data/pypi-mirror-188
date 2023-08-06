from datetime import datetime, timedelta

import allure
import pytest

from refinitiv.data.content.ipa.dates_and_calendars import holidays
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
    "name",
    "calendars",
    "countries",
    "tag",
    "date",
]


first_definition = holidays.Definition(
    tag="my request",
    start_date=datetime(2020, 5, 2),
    end_date=timedelta(-30),
    calendars=["UKR", "FRA"],
    currencies=["EUR"],
    holiday_outputs=["Date", "Names", "Calendars", "Countries"],
)

second_definition = holidays.Definition(
    tag="my second request",
    start_date="2018-12-31",
    end_date=datetime.now(),
    calendars=["UKR", "FRA"],
    currencies=["EUR"],
    holiday_outputs=["Date", "Names", "Calendars", "Countries"],
)

invalid_definition = holidays.Definition(
    tag="my second request",
    start_date=datetime.now(),
    end_date=timedelta(-30),
    calendars=["UKR", "FRA"],
    currencies=["EUR"],
    holiday_outputs=["Date", "Names", "Calendars", "Countries"],
)


@allure.suite("Dates And Calendars")
@allure.feature("Content object - Holidays")
@allure.severity(allure.severity_level.CRITICAL)
class TestHolidays:
    @allure.title("Create a holidays definition with valid params")
    @pytest.mark.caseid("C46153589")
    @pytest.mark.parametrize(
        "start_date, end_date, calendars, currencies, holiday_outputs",
        [
            (
                "2018-12-31",
                "2019-01-03",
                ["UKR", "FRA"],
                ["EUR"],
                ["Date", "Names", "Calendars", "Countries"],
            ),
            (
                timedelta(-180),
                timedelta(0),
                ["UKR", "FRA"],
                None,
                [holidays.HolidayOutputs.DATE, holidays.HolidayOutputs.NAMES],
            ),
            (
                timedelta(-180),
                datetime.now(),
                None,
                ["USD"],
                ["Date", "Calendars", "Names"],
            ),
            (
                datetime(2019, 4, 13),
                datetime.now(),
                None,
                ["USD"],
                None,
            ),
        ],
    )
    def test_holidays_definition_with_valid_params(
        self, open_session, start_date, end_date, calendars, currencies, holiday_outputs
    ):
        response = holidays.Definition(
            tag="my request 2",
            start_date=start_date,
            end_date=end_date,
            calendars=calendars,
            currencies=currencies,
            holiday_outputs=holiday_outputs,
        ).get_data()

        assert isinstance(response.data.holidays, list)

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)

        if holiday_outputs is not None:
            check_response_dataframe_contains_columns_names(
                response, EXPECTED_COLUMN_NAMES
            )
            check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Create a holidays definition with valid params asynchronously")
    @pytest.mark.caseid("C46323263")
    async def test_holidays_definition_with_valid_params_async(self, open_session_async):
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
            expected_error_code="IPA_library.ErrorBusinessCalendar_EndDateMustBeGreaterThanStartDate",
            expected_error_message="Business Calendar: end date must be greater than start date.",
        )

    @allure.title("Create a holidays definitions with valid and invalid params")
    @pytest.mark.caseid("C46153592")
    def test_holidays_definitions_with_valid_and_invalid_params(self, open_session):
        response = holidays.Definitions(
            [first_definition, second_definition, invalid_definition]
        ).get_data()

        check_non_empty_response_data(response)
        check_response_status(
            response=response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
            expected_error_code="IPA_library.ErrorBusinessCalendar_EndDateMustBeGreaterThanStartDate",
            expected_error_message="Business Calendar: end date must be greater than start date.",
        )
        check_response_dataframe_contains_columns_names(response, EXPECTED_COLUMN_NAMES)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create a holidays definition with invalid params and getting RDError"
    )
    @pytest.mark.parametrize(
        "expected_error",
        [
            (
                "Error code 400 | Invalid input: at least one currency code or calendar code must be specified."
            )
        ],
    )
    @pytest.mark.caseid("C46153599")
    def test_holidays_definition_with_invalid_params(
        self, open_session, expected_error
    ):
        with pytest.raises(RDError) as error:
            holidays.Definition(
                start_date=timedelta(-30), end_date=timedelta(0)
            ).get_data()
        assert str(error.value) == expected_error

    @allure.title(
        "Create a holidays definitions with invalid params and getting RDError"
    )
    @pytest.mark.parametrize(
        "expected_error",
        [
            (
                "Error code IPA_library.ErrorBusinessCalendar_EndDateMustBeGreaterThanStartDate | Business Calendar: "
                "end date must be greater than start date."
            )
        ],
    )
    @pytest.mark.caseid("C46153595")
    def test_holidays_definitions_with_invalid_params(
        self, open_session, expected_error
    ):
        with pytest.raises(RDError) as error:
            holidays.Definitions(invalid_definition).get_data()
        assert str(error.value) == expected_error

    @allure.title("Create a holidays definitions with valid params asynchronously")
    @pytest.mark.caseid("C46323265")
    async def test_holidays_definitions_with_valid_params_async(self, open_session_async):
        valid_response, invalid_response = await get_async_response_from_definitions(
            holidays.Definitions([first_definition, second_definition]),
            holidays.Definitions(invalid_definition),
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
            expected_error_code="IPA_library.ErrorBusinessCalendar_EndDateMustBeGreaterThanStartDate",
            expected_error_message="Business Calendar: end date must be greater than start date.",
        )

    @allure.title("Create Holidays definition with extended params field and get data")
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
    @pytest.mark.caseid("C46153590")
    def test_holidays_definitions_with_extended_params(
        self, open_session, extended_param
    ):
        response = holidays.Definition(
            tag="my request",
            start_date=timedelta(-360),
            end_date=datetime.now(),
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
