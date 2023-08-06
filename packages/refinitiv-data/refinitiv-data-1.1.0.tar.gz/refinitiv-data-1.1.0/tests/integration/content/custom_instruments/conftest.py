import datetime
import uuid
from time import sleep

import pytest

import refinitiv.data as rd
from refinitiv.data import OpenState
from refinitiv.data.content import custom_instruments as ci
from refinitiv.data.content.ipa import dates_and_calendars
from tests.integration.conftest import create_desktop_session, create_platform_session_with_rdp_creds

instrument_data = {
    "description": "Glory tale about instrument",
    "exchange_name": "8080",
    "instrument_name": "Trading St. tool",
    "time_zone": "LON",
    "currency": "GBP",
}

new_instrument_data = {
    "description": "Something new with trading tool",
    "exchange_name": "9832",
    "instrument_name": "GMBH fintech t.",
    "time_zone": "LON",
    "currency": "EUR",
}

volume_based_udc = ci.manage.UDC(
    root="CC",
    months=ci.manage.Months(
        number_of_years=3,
        include_all_months=True,
        start_month=1,
    ),
    rollover=ci.manage.VolumeBasedRollover(
        method=ci.VolumeBasedRolloverMethod.VOLUME,
        number_of_days=1,
        join_at_day=1,
        roll_occurs_within_months=4,
        roll_on_expiry=True,
    ),
    spread_adjustment=ci.manage.SpreadAdjustment(
        adjustment="arithmetic",
        method=ci.SpreadAdjustmentMethod.CLOSE_TO_CLOSE,
        backwards=True,
    ),
)

day_based_udc = ci.manage.UDC(
    root="CC",
    months=ci.manage.Months(number_of_years=3, include_months=[1, 2, 3], start_month=2),
    rollover=ci.manage.DayBasedRollover(
        method=ci.DayBasedRolloverMethod.DAYS_BEFORE_END_OF_MONTH,
        number_of_days=3,
        months_prior=1,
    ),
    spread_adjustment=ci.manage.SpreadAdjustment(
        adjustment="arithmetic",
        method=ci.SpreadAdjustmentMethod.CLOSE_TO_CLOSE,
        backwards=True,
    ),
)

new_day_based_udc = ci.manage.UDC(
    root="CC",
    months=ci.manage.Months(
        number_of_years=2, include_months=[4, 5, 6, 7], start_month=3
    ),
    rollover=ci.manage.DayBasedRollover(
        method=ci.DayBasedRolloverMethod.DAYS_BEFORE_EXPIRY,
        number_of_days=2,
    ),
    spread_adjustment=ci.manage.SpreadAdjustment(
        adjustment="arithmetic",
        method=ci.SpreadAdjustmentMethod.OPEN_TO_OPEN,
        backwards=True,
    ),
)

manual_udc = ci.manage.UDC(
    root="CC",
    rollover=ci.manage.ManualRollover(
        ci.manage.ManualItem(month=7, year=2022, start_date="2022-02-01"),
        ci.manage.ManualItem(month=7, year=2021, start_date=datetime.date(2021, 3, 1)),
        ci.manage.ManualItem(
            month=3, year=2020, start_date=datetime.timedelta(days=-1550)
        ),
    ),
    spread_adjustment=ci.manage.SpreadAdjustment(
        adjustment="arithmetic",
        method="close-to-close",
        backwards=True,
    ),
)


def check_open_and_close_stream_state(
    stream, wait_before_close=None, with_updates=True
):
    stream.open(with_updates)
    assert stream.open_state == OpenState.Opened, "Stream is not in opened state"
    if wait_before_close is not None:
        sleep(wait_before_close)
    stream.close()
    assert stream.open_state == OpenState.Closed, "Stream is not in closed state"


def check_close_and_open_stream_state(stream_01, stream_02, stream_03, wait_time=None):
    stream_01.close()
    assert stream_01.open_state == OpenState.Closed, "Stream is not in closed state"
    if wait_time is not None:
        sleep(wait_time)
    assert stream_02.open_state == OpenState.Opened, "Stream is not in opened state"
    assert stream_03.open_state == OpenState.Opened, "Stream is not in opened state"


def check_stream_instrument(expected_instrument, stream):
    if isinstance(expected_instrument, list):
        actual_universe = stream._stream.universe
    else:
        actual_universe = stream._stream.universe[0]
    assert (
        expected_instrument == actual_universe
    ), f"{actual_universe} universe is not expected"


def is_stream_id_equal(stream_01, stream_02):
    return stream_02._stream._id == stream_01._stream._id


def check_stream_snapshot(stream, universe, expected_fields):
    df = stream.get_snapshot()
    assert not df.empty, f"Snapshot dataframe for {universe} is empty"
    assert universe in df.values[0], f"There is no data for {universe} in snapshot"
    actual_fields = set(df.columns)
    assert (
        actual_fields == set(expected_fields),
    ), f"{expected_fields} != {actual_fields}"


def get_holidays(session):
    calendar_holiday = dates_and_calendars.holidays.Definition(
        start_date="2015-08-24",
        end_date="2018-09-24",
        calendars=["UKR"],
        holiday_outputs=["Date", "Names"],
    ).get_data(session=session)
    return calendar_holiday.data.holidays[0]


@pytest.fixture(name="symbol")
def get_ci_symbol():
    return str(uuid.uuid4())[:8]


@pytest.fixture(
    scope="function",
    params=[create_platform_session_with_rdp_creds, create_desktop_session],
    ids=["platform_session", "desktop_session"],
)
def open_session_with_rdp_creds_for_ci(request, set_env_base_url):
    create_session = request.param
    session = create_session()
    rd.session.set_default(session)
    session.open()
    yield session
    session.close()
    rd.session.set_default(None)