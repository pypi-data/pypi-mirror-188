import types
from datetime import datetime
from functools import partial

import pytest

import refinitiv.data as rd
from refinitiv.data.delivery._data._request import Request
from tests.unit.conftest import StubSession, StubResponse
from .test_enums import get_json, get_query_params_from_url

items = [
    rd.get_history,
    rd.content.news.headlines.Definition,
    rd.content.custom_instruments.summaries.Definition,
    rd.content.custom_instruments.events.Definition,
    rd.content.historical_pricing.events.Definition,
    rd.content.historical_pricing.summaries.Definition,
    rd.content.ownership.fund.shareholders_history_report.Definition,
    rd.content.ownership.consolidated.shareholders_history_report.Definition,
    rd.content.ownership.insider.transaction_report.Definition,
    rd.dates_and_calendars.add_periods,
    rd.dates_and_calendars.count_periods,
    rd.dates_and_calendars.date_schedule,
    rd.dates_and_calendars.is_working_day,
    rd.dates_and_calendars.holidays,
    rd.content.ipa.dates_and_calendars.add_periods.Definition,
    rd.content.ipa.dates_and_calendars.count_periods.Definition,
    rd.content.ipa.dates_and_calendars.date_schedule.Definition,
    rd.content.ipa.dates_and_calendars.is_working_day.Definition,
    rd.content.ipa.dates_and_calendars.holidays.Definition,
    rd._qpl.fx_swp_to_swp,
]


def test_datetime_arguments():
    for item in items:
        if not isinstance(item, types.FunctionType):
            item = getattr(item, "__init__")
        annotations = item.__annotations__
        if not annotations:
            continue

        has = False
        for param_name, type_notation in annotations.items():
            if type_notation == "OptDateTime":
                has = True
                break

        assert has, item


def make_checker(param_name, value, func_get_params, mocked_json):
    def http_request(request: Request):
        params = func_get_params(request)

        if isinstance(params, list):
            params = params[0]

        assert params[param_name] == str(value), (
            f"Param{param_name}:\n"
            f"Expected value {params[param_name]}. \n"
            f"Value {str(value)}"
        )
        return StubResponse(mocked_json=mocked_json)

    return http_request


@pytest.mark.xfail
@pytest.mark.parametrize(
    argnames=(
        "definition",
        "date",
        "date_arg_name",
        "request_param_name",
        "func_get_params",
        "mocked_json",
    ),
    argvalues=[
        (
            rd.content.news.headlines.Definition(
                query="Refinitiv", count=10, date_from=datetime(2020, 1, 1)
            ),
            "2020-01-01T00%3A00%3A00",
            "date_from",
            "dateFrom",
            get_query_params_from_url,
            None,
        ),
        (
            rd.content.ipa.dates_and_calendars.add_periods.Definition(
                start_date=datetime(2020, 1, 1), period="1Y"
            ),
            "2020-01-01",
            "start_date",
            "startDate",
            get_json,
            [{"data": [{}], "headers": [], "error": []}],
        ),
        (
            rd.content.ipa.dates_and_calendars.count_periods.Definition(
                start_date=datetime(2020, 1, 1), end_date="2022-01-01"
            ),
            "2020-01-01",
            "start_date",
            "startDate",
            get_json,
            [{"data": [{}], "headers": [], "error": []}],
        ),
        (
            rd.content.ipa.dates_and_calendars.date_schedule.Definition(
                start_date=datetime(2020, 1, 1), frequency="Daily"
            ),
            "2020-01-01",
            "start_date",
            "startDate",
            get_json,
            [{"data": [{}], "headers": [], "error": []}],
        ),
        (
            rd.content.ipa.dates_and_calendars.is_working_day.Definition(
                date=datetime(2020, 1, 1)
            ),
            "2020-01-01",
            "date",
            "date",
            get_json,
            [{"data": [{}], "headers": [], "error": []}],
        ),
        (
            rd.content.ipa.dates_and_calendars.holidays.Definition(
                start_date=datetime(2020, 1, 1), end_date="2022-01-01"
            ),
            "2020-01-01",
            "date",
            "date",
            get_json,
            [{"data": [{}], "headers": [], "error": []}],
        ),
        (
            rd.content.custom_instruments.summaries.Definition(
                universe=["EUR"], start=datetime(2020, 1, 1)
            ),
            "2020-01-01",
            "start",
            "start",
            get_json,
            None,
        ),
        (
            rd.content.custom_instruments.events.Definition(
                universe=["EUR"], start=datetime(2020, 1, 1)
            ),
            "2020-01-01",
            "start",
            "start",
            get_json,
            None,
        ),
        (
            rd.content.historical_pricing.events.Definition(
                universe=["EUR"], start=datetime(2020, 1, 1)
            ),
            "2020-01-01T00%3A00%3A00.000000000Z",
            "start",
            "start",
            get_query_params_from_url,
            None,
        ),
        (
            rd.content.historical_pricing.summaries.Definition(
                universe=["EUR"], start=datetime(2020, 1, 1)
            ),
            "2020-01-01T00%3A00%3A00.000000000Z",
            "start",
            "start",
            get_query_params_from_url,
            None,
        ),
        (
            rd.content.ownership.fund.shareholders_history_report.Definition(
                universe="TRI.N", frequency="Q", start=datetime(2020, 1, 1)
            ),
            "2020-01-01T00%3A00%3A00.000000000Z",
            "start",
            "start",
            get_query_params_from_url,
            None,
        ),
        (
            rd.content.ownership.consolidated.shareholders_history_report.Definition(
                universe="TRI.N", frequency="Q", start=datetime(2020, 1, 1)
            ),
            "2020-01-01T00%3A00%3A00.000000000Z",
            "start",
            "start",
            get_query_params_from_url,
            None,
        ),
        (
            rd.content.ownership.insider.transaction_report.Definition(
                universe="TRI.N", start=datetime(2020, 1, 1)
            ),
            "2020-01-01T00%3A00%3A00.000000000Z",
            "start",
            "start",
            get_query_params_from_url,
            None,
        ),
    ],
    ids=(
        "rd.content.news.headlines.Definition",
        "rd.content.ipa.dates_and_calendars.add_periods.Definition",
        "rd.content.ipa.dates_and_calendars.count_periods.Definition",
        "rd.content.ipa.dates_and_calendars.date_schedule.Definition",
        "rd.content.ipa.dates_and_calendars.is_working_day.Definition",
        "rd.content.ipa.dates_and_calendars.holidays.Definition",
        "rd.content.custom_instruments.summaries.Definition",
        "rd.content.custom_instruments.events.Definition",
        "rd.content.historical_pricing.events.Definition",
        "rd.content.historical_pricing.summaries.Definition",
        "rd.content.ownership.fund.shareholders_history_report.Definition",
        "rd.content.ownership.consolidated.shareholders_history_report.Definition",
        "rd.content.ownership.insider.transaction_report.Definition",
    ),
)
def test_datetime_in_definition(
    definition, date, date_arg_name, request_param_name, func_get_params, mocked_json
):
    session = StubSession(is_open=True)
    session.config.set_param("apis.data.news.underlying-platform", "rdp")

    session.http_request = make_checker(
        request_param_name, date, func_get_params, mocked_json
    )

    try:
        definition.get_data(session=session)
    except (KeyError, IndexError):
        pass


@pytest.mark.parametrize(
    (
        "function",
        "date",
        "date_arg_name",
        "request_param_name",
        "func_get_params",
        "mocked_json",
    ),
    [
        (
            partial(
                rd._qpl.fx_swp_to_swp,
                fx_cross_code="code",
                market_data_date_time=datetime(2020, 1, 1),
            ),
            "2020-01-01",
            "market_data_date_time",
            "marketDataDate",
            get_json,
            None,
        ),
    ],
)
def test_datetime_in_function(
    function, date, date_arg_name, request_param_name, func_get_params, mocked_json
):
    session = StubSession(is_open=True)
    rd.session.set_default(session)
    session.http_request = make_checker(
        request_param_name, date, func_get_params, mocked_json
    )

    try:
        function()
    except (KeyError, IndexError):
        pass

    rd.session.set_default(None)
