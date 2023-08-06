from refinitiv.data._errors import RDError
from refinitiv.data.content._content_data import Data
from refinitiv.data.content.ipa._enums import HolidayOutputs
from refinitiv.data.content.ipa.dates_and_calendars import is_working_day
from refinitiv.data.content.ipa.dates_and_calendars.is_working_day._is_working_day_data_provider import (
    IsWorkingDays,
    IsWorkingDay,
)
from tests.unit.conftest import StubSession, StubResponse, remove_private_attributes


def test_is_working_days_class():
    # fmt: off
    raw_response = [
    {"isWorkingDay": False, "isWeekEnd": True, "tag": "my request",
        "holidays": [{"date": "2022-01-01",
                "names": [
                    {"name": "New Year's Day", "calendars": ["BAR", "KOR", "JAP", "USA"],
                     "countries": ["BLR", "KOR", "JPN", "USA"],}],}
        ],},
    {"isWorkingDay": False, "isWeekEnd": True, "tag": "my request",
        "holidays": [{"date": "2021-12-25",
                "names": [
                    {"name": "Christmas Day", "calendars": ["BAR", "EMU"],
                     "countries": ["BLR", ""],}],}
        ],},
    ]
    # fmt: on
    session = StubSession(is_open=True, response=StubResponse(raw_response))
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
    definition = is_working_day.Definitions([first_definition, second_definition])

    response = definition.get_data(session)
    data = response.data

    assert data.raw == raw_response
    assert data.df.empty is False
    assert data.days
    assert isinstance(data, IsWorkingDays)

    assert remove_private_attributes(dir(data)) == ["days", "df", "raw"]


def test_is_working_day_class():
    # fmt: off
    raw_response = [
    {"isWorkingDay": False, "isWeekEnd": True, "tag": "my request",
        "holidays": [{"date": "2021-12-25",
                "names": [
                    {"name": "Christmas Day", "calendars": ["BAR", "EMU"],
                     "countries": ["BLR", ""],}],}
        ],},
    ]
    # fmt: on
    session = StubSession(is_open=True, response=StubResponse(raw_response))
    definition = is_working_day.Definition(
        tag="my request",
        date="2021-12-25",
        calendars=["BAR"],
        currencies=["EUR"],
        holiday_outputs=[HolidayOutputs.DATE, HolidayOutputs.NAMES],
    )
    response = definition.get_data(session)

    data = response.data
    assert data.raw == raw_response
    assert data.df.empty is False
    assert data.day
    assert isinstance(data, IsWorkingDay)

    assert remove_private_attributes(dir(data)) == ["day", "df", "raw"]


def test_data_class_when_get_data():
    # fmt: off
    raw_response = [
        {
            "error": {
                "status": "Error",
                "message": "Business Calendar: calendar not found.",
                "code": "IPA_library.ErrorBusinessCalendar_CalendarNotFound",
            },
            "tag": "First Jan for UAH currency",
        }
    ]
    # fmt: on
    session = StubSession(is_open=True, response=StubResponse(raw_response))
    definition = is_working_day.Definition(
        tag="my request",
        date="2021-12-25",
        calendars=["BAR"],
        currencies=["EUR"],
        holiday_outputs=[HolidayOutputs.DATE, HolidayOutputs.NAMES],
    )

    try:
        response = definition.get_data(session)
    except RDError as e:
        response = e.response
        assert e
    else:
        assert False

    data = response.data
    assert data.raw == raw_response
    assert data.df.empty is True
    assert isinstance(data, Data)

    assert remove_private_attributes(dir(data)) == ["df", "raw"]


async def test_data_class_when_get_data_async():
    # fmt: off
    raw_response = [
        {
            "error": {
                "status": "Error",
                "message": "Business Calendar: calendar not found.",
                "code": "IPA_library.ErrorBusinessCalendar_CalendarNotFound",
            },
            "tag": "First Jan for UAH currency",
        }
    ]
    # fmt: on
    session = StubSession(is_open=True, response=StubResponse(raw_response))
    definition = is_working_day.Definition(
        tag="my request",
        date="2021-12-25",
        calendars=["BAR"],
        currencies=["EUR"],
        holiday_outputs=[HolidayOutputs.DATE, HolidayOutputs.NAMES],
    )
    response = await definition.get_data_async(session)

    data = response.data
    assert data.raw == raw_response
    assert data.df.empty is True
    assert isinstance(data, Data)

    assert remove_private_attributes(dir(data)) == ["df", "raw"]
