from datetime import datetime, timedelta

import allure
import pytest

from refinitiv.data.content.ipa.dates_and_calendars import count_periods
from refinitiv.data.content.ipa.dates_and_calendars.count_periods._count_periods_data_provider import (
    Period,
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

EXPECTED_COLUMN_NAMES = ["count", "tag", "tenor"]


first_definition = count_periods.Definition(
    tag="my request 1",
    start_date=timedelta(-180),
    end_date=datetime.now(),
    period_type=count_periods.PeriodType.WORKING_DAY,
    calendars=["BAR", "KOR", "JAP"],
    currencies=["USD"],
    day_count_basis="Dcb_30E_360_ISMA",
)

second_definition = count_periods.Definition(
    tag="my request 2",
    start_date="2020-04-24",
    end_date="2021-04-24",
    period_type="NonWorkingDay",
    calendars=["BAR", "KOR", "JAP"],
    currencies=["USD"],
    day_count_basis=count_periods.DayCountBasis.DCB_30_ACTUAL,
)

invalid_definition = count_periods.Definition(
    tag="my request 2",
    start_date="2023.04.24",
    end_date=timedelta(0),
    period_type="Day",
)


@allure.suite("Dates And Calendars")
@allure.feature("Content object - Count Periods")
@allure.severity(allure.severity_level.CRITICAL)
class TestCountPeriods:
    @allure.title("Create a count_periods definition with valid params")
    @pytest.mark.caseid("C45567339")
    @pytest.mark.parametrize(
        "start_date, end_date, calendars, currencies, day_count_basis, period_type",
        [
            (
                "2018-12-31",
                "2020-12-31",
                ["UKR", "FRA"],
                ["EUR"],
                count_periods.DayCountBasis.DCB_30_360_US,
                count_periods.PeriodType.DAY,
            ),
            (
                timedelta(-180),
                timedelta(0),
                ["UKR", "FRA"],
                None,
                "Dcb_30_365_Brazil",
                "Year",
            ),
            (
                datetime(2020, 4, 13),
                datetime.now(),
                None,
                ["USD"],
                None,
                None,
            ),
        ],
    )
    def test_add_periods_definition_with_valid_params(
        self,
        open_session,
        start_date,
        end_date,
        calendars,
        currencies,
        day_count_basis,
        period_type,
    ):
        response = count_periods.Definition(
            tag="my request",
            period_type=period_type,
            start_date=start_date,
            end_date=end_date,
            calendars=calendars,
            currencies=currencies,
            day_count_basis=day_count_basis,
        ).get_data()

        assert isinstance(response.data.counted_period, Period)
        assert response.data.counted_period.tag == "my request"
        assert isinstance(response.data.counted_period.count, float)

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, EXPECTED_COLUMN_NAMES)

    @allure.title(
        "Create a count_periods definition with valid and invalid definition asynchronously"
    )
    @pytest.mark.caseid("C46606039")
    async def test_count_periods_definition_with_valid_and_invalid_def_async(
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
            expected_error_message="Business Calendar: end date must be greater than start date.",
        )

    @allure.title(
        "Create a count_periods definitions with valid and invalid definition and getting RDError"
    )
    @pytest.mark.parametrize(
        "expected_error",
        [
            (
                "Error code 400 | Business Calendar: end date must be greater than start date."
            )
        ],
    )
    @pytest.mark.caseid("C45567347")
    def test_count_periods_definitions_with_valid_and_invalid_def(
        self, open_session, expected_error
    ):
        with pytest.raises(RDError) as error:
            count_periods.Definitions(
                [first_definition, second_definition, invalid_definition]
            ).get_data()
        assert str(error.value) == expected_error

    @allure.title(
        "Create a count_periods definitions with valid and invalid definition params asynchronously"
    )
    @pytest.mark.caseid("C46606806")
    async def test_count_periods_definitions_with_valid_and_invalid_def_async(
        self, open_session_async
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            count_periods.Definitions([first_definition, second_definition]),
            count_periods.Definitions(invalid_definition),
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
            expected_error_message="Business Calendar: end date must be greater than start date.",
        )

    @allure.title("Create count_periods definition with extended params and get data")
    @pytest.mark.parametrize(
        "extended_param",
        [
            {
                "tag": "new tag",
                "startDate": "2022-07-04",
            }
        ],
    )
    @pytest.mark.caseid("C45567341")
    def test_count_periods_definition_with_extended_params(
        self, open_session, extended_param
    ):
        response = count_periods.Definition(
            tag="my request",
            period_type=count_periods.PeriodType.NON_WORKING_DAY,
            start_date=timedelta(-360),
            end_date=datetime.now(),
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

    @allure.title("Create an count_periods definition without session and get error")
    @pytest.mark.parametrize(
        "expected_error",
        ["No default session created yet. Please create a session first!"],
    )
    @pytest.mark.caseid("C45567348")
    def test_count_periods_definition_without_session(self, expected_error):
        with pytest.raises(AttributeError) as error:
            first_definition.get_data()
        assert str(error.value) == expected_error
