from refinitiv.data.content.ipa.dates_and_calendars import is_working_day
from refinitiv.data.content.ipa.dates_and_calendars.is_working_day._is_working_day_data_provider import (
    IsWorkingDayResponseFactory,
)
from refinitiv.data.delivery._data._data_provider import ParsedData

MOCKED_IS_WORKING_DAY_DATA = ParsedData(
    {"http_status_code": 200, "http_reason": "OK"},
    {},
    [
        {
            "isWorkingDay": False,
            "isWeekEnd": False,
            "tag": "First Jan for UAH currency",
            "holidays": [
                {
                    "names": [
                        {
                            "name": "New Year's Day",
                            "calendars": ["EMU"],
                            "countries": [""],
                        }
                    ],
                    "calendars": ["EMU"],
                }
            ],
        }
    ],
)

MOCKED_DATA_ERROR = ParsedData(
    {"http_status_code": 200, "http_reason": "OK"},
    {},
    [
        {
            "error": {
                "status": "Error",
                "message": "Business Calendar: calendar not found.",
                "code": "IPA_library.ErrorBusinessCalendar_CalendarNotFound",
            },
            "tag": "First Jan for UAH currency",
        }
    ],
    ["IPA_library.ErrorBusinessCalendar_CalendarNotFound"],
    ["Business Calendar: calendar not found."],
)


def test_is_working_day():
    definition = is_working_day.Definition(
        date="2020-01-01",
        currencies=["EUR"],
        tag="First Jan for EUR currency",
        holiday_outputs=[
            is_working_day.HolidayOutputs.NAMES,
            is_working_day.HolidayOutputs.CALENDARS,
        ],
    )

    assert definition.request_item.tag == "First Jan for EUR currency"
    assert definition.request_item.date == "2020-01-01"
    assert definition.request_item.calendars is None
    assert definition.request_item.currencies == ["EUR"]
    assert definition.request_item.holiday_outputs == [
        is_working_day.HolidayOutputs.NAMES,
        is_working_day.HolidayOutputs.CALENDARS,
    ]


def test_is_working_day_create_success():
    response_factory = IsWorkingDayResponseFactory()
    response = response_factory.create_success(MOCKED_IS_WORKING_DAY_DATA)
    assert not response.data.df.empty
    assert response.data.raw == MOCKED_IS_WORKING_DAY_DATA.content_data
    assert response.data.day.holidays[0].calendars == ["EMU"]
    assert response.data.day.is_working_day is False


def test_is_working_day_create_fail():
    response_factory = IsWorkingDayResponseFactory()
    response = response_factory.create_fail(MOCKED_DATA_ERROR)
    assert response.data.raw == MOCKED_DATA_ERROR.content_data
    assert len(response.errors)
