from refinitiv.data.content.ipa.dates_and_calendars import holidays
from refinitiv.data.content.ipa.dates_and_calendars._request_factory import (
    DatesAndCalendarsResponseFactory,
)
from refinitiv.data.content.ipa.dates_and_calendars.holidays._holidays_data_provider import (
    HolidaysData,
)
from refinitiv.data.delivery._data._data_provider import ParsedData

MOCKED_HOLIDAYS_DATA = ParsedData(
    {"http_status_code": 200, "http_reason": "OK"},
    {},
    [
        {
            "tag": "my request",
            "holidays": [
                {
                    "date": "2018-12-31",
                    "names": [
                        {
                            "name": "New Year's Bridge Holiday '18",
                            "calendars": ["UKR"],
                            "countries": ["UKR"],
                        }
                    ],
                    "calendars": ["UKR"],
                    "countries": ["UKR"],
                },
                {
                    "date": "2019-01-01",
                    "names": [
                        {
                            "name": "New Year's Day (day 1)",
                            "calendars": ["UKR"],
                            "countries": ["UKR"],
                        },
                        {
                            "name": "New Year's Day",
                            "calendars": ["FRA", "EMU"],
                            "countries": ["FRA", ""],
                        },
                    ],
                    "calendars": ["UKR", "FRA", "EMU"],
                    "countries": ["UKR", "FRA", ""],
                },
                {
                    "date": "2019-01-02",
                    "names": [
                        {
                            "name": "New Year's Day (Day 2) '19",
                            "calendars": ["UKR"],
                            "countries": ["UKR"],
                        }
                    ],
                    "calendars": ["UKR"],
                    "countries": ["UKR"],
                },
            ],
        }
    ],
)

MOCKED_DATA_ERROR = ParsedData(
    {"http_status_code": 200, "http_reason": "OK"},
    {},
    [
        {
            "tag": "my request",
            "error": {
                "status": "Error",
                "message": "Business Calendar: calendar not found.",
                "code": "IPA_library.ErrorBusinessCalendar_CalendarNotFound",
            },
        }
    ],
    ["IPA_library.ErrorBusinessCalendar_CalendarNotFound"],
    ["Business Calendar: calendar not found."],
)


def test_holidays():
    definition = holidays.Definition(
        tag="my request",
        start_date="2018-12-31",
        end_date="2019-01-03",
        calendars=["UKR", "FRA"],
        currencies=["EUR"],
        holiday_outputs=[
            holidays.HolidayOutputs.DATE,
            holidays.HolidayOutputs.NAMES,
            holidays.HolidayOutputs.CALENDARS,
            holidays.HolidayOutputs.COUNTRIES,
        ],
    )

    assert definition.request_item.tag == "my request"
    assert definition.request_item.start_date == "2018-12-31"
    assert definition.request_item.end_date == "2019-01-03"
    assert definition.request_item.calendars == ["UKR", "FRA"]
    assert definition.request_item.currencies == ["EUR"]
    assert definition.request_item.holiday_outputs == [
        holidays.HolidayOutputs.DATE,
        holidays.HolidayOutputs.NAMES,
        holidays.HolidayOutputs.CALENDARS,
        holidays.HolidayOutputs.COUNTRIES,
    ]


def test_holidays_create_success():
    response_factory = DatesAndCalendarsResponseFactory(data_class=HolidaysData)
    response = response_factory.create_success(MOCKED_HOLIDAYS_DATA)
    assert not response.data.df.empty
    assert response.data.raw == MOCKED_HOLIDAYS_DATA.content_data
    assert response.data.holidays[1].countries == ["UKR", "FRA", ""]
    assert response.data.holidays[0].tag == "my request"


def test_holidays_create_fail():
    response_factory = DatesAndCalendarsResponseFactory(data_class=HolidaysData)
    response = response_factory.create_fail(MOCKED_DATA_ERROR)
    assert response.data.raw == MOCKED_DATA_ERROR.content_data
    assert len(response.errors)
