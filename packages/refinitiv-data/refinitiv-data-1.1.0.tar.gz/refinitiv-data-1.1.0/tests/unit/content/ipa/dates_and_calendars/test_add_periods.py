from refinitiv.data.content.ipa.dates_and_calendars import add_periods
from refinitiv.data.content.ipa.dates_and_calendars.add_periods._add_periods_data_provider import (
    AddPeriodsResponseFactory,
)
from refinitiv.data.delivery._data._data_provider import ParsedData

MOCKED_ADD_PERIODS_DATA = ParsedData(
    {"http_status_code": 200, "http_reason": "OK"},
    {},
    [
        {
            "date": "2020-05-07",
            "holidays": [
                {
                    "date": "2020-04-28",
                    "names": [
                        {
                            "name": "Radunitsa '20",
                            "calendars": ["BAR"],
                            "countries": ["BLR"],
                        }
                    ],
                    "calendars": ["BAR"],
                },
                {
                    "date": "2020-04-29",
                    "names": [
                        {
                            "name": "Showa Day",
                            "calendars": ["JAP"],
                            "countries": ["JPN"],
                        }
                    ],
                    "calendars": ["JAP"],
                },
                {
                    "date": "2020-04-30",
                    "names": [
                        {
                            "name": "Buddha's Birthday '20",
                            "calendars": ["KOR"],
                            "countries": ["KOR"],
                        }
                    ],
                    "calendars": ["KOR"],
                },
                {
                    "date": "2020-05-01",
                    "names": [
                        {
                            "name": "Labour Day (Day 1)",
                            "calendars": ["BAR"],
                            "countries": ["BLR"],
                        },
                        {
                            "name": "Labor Day",
                            "calendars": ["KOR"],
                            "countries": ["KOR"],
                        },
                    ],
                    "calendars": ["BAR", "KOR"],
                },
                {
                    "date": "2020-05-02",
                    "names": [
                        {
                            "name": "Weekend",
                            "calendars": ["BAR", "KOR", "JAP", "USA"],
                            "countries": ["BLR", "KOR", "JPN", "USA"],
                        }
                    ],
                    "calendars": ["BAR", "KOR", "JAP", "USA"],
                },
                {
                    "date": "2020-05-03",
                    "names": [
                        {
                            "name": "Constitution Day",
                            "calendars": ["JAP"],
                            "countries": ["JPN"],
                        },
                        {
                            "name": "Weekend",
                            "calendars": ["BAR", "KOR", "USA"],
                            "countries": ["BLR", "KOR", "USA"],
                        },
                    ],
                    "calendars": ["BAR", "KOR", "JAP", "USA"],
                },
                {
                    "date": "2020-05-04",
                    "names": [
                        {
                            "name": "Greenery Day",
                            "calendars": ["JAP"],
                            "countries": ["JPN"],
                        }
                    ],
                    "calendars": ["JAP"],
                },
                {
                    "date": "2020-05-05",
                    "names": [
                        {
                            "name": "Children's Day",
                            "calendars": ["KOR", "JAP"],
                            "countries": ["KOR", "JPN"],
                        }
                    ],
                    "calendars": ["KOR", "JAP"],
                },
                {
                    "date": "2020-05-06",
                    "names": [
                        {
                            "name": "1. Constitution Day (Observed)",
                            "calendars": ["JAP"],
                            "countries": ["JPN"],
                        }
                    ],
                    "calendars": ["JAP"],
                },
            ],
            "tag": "my request",
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
                "message": "Business Calendar: invalid period.",
                "code": "IPA_library.ErrorBusinessCalendar_InvalidPeriod",
            },
            "tag": "my request",
        }
    ],
    ["IPA_library.ErrorBusinessCalendar_InvalidPeriod"],
    ["Business Calendar: invalid period."],
)


def test_add_periods():
    definition = add_periods.Definition(
        tag="my request",
        start_date="2020-04-24",
        period="4D",
        calendars=["BAR", "KOR", "JAP"],
        date_moving_convention=add_periods.DateMovingConvention.NEXT_BUSINESS_DAY,
        end_of_month_convention=add_periods.EndOfMonthConvention.LAST,
        holiday_outputs=[
            add_periods.HolidayOutputs.DATE,
            add_periods.HolidayOutputs.NAMES,
            add_periods.HolidayOutputs.CALENDARS,
            add_periods.HolidayOutputs.COUNTRIES,
        ],
    )
    assert definition.request_item.period == "4D"
    assert definition.request_item.tag == "my request"
    assert definition.request_item.start_date == "2020-04-24"
    assert definition.request_item.calendars == ["BAR", "KOR", "JAP"]
    assert (
        definition.request_item.end_of_month_convention
        == add_periods.EndOfMonthConvention.LAST
    )
    assert definition.request_item.holiday_outputs == [
        add_periods.HolidayOutputs.DATE,
        add_periods.HolidayOutputs.NAMES,
        add_periods.HolidayOutputs.CALENDARS,
        add_periods.HolidayOutputs.COUNTRIES,
    ]


def test_add_periods_create_success():
    response_factory = AddPeriodsResponseFactory()
    response = response_factory.create_success(MOCKED_ADD_PERIODS_DATA)
    assert not response.data.df.empty
    assert response.data.raw == MOCKED_ADD_PERIODS_DATA.content_data
    assert response.data.added_period.date == "2020-05-07"
    assert response.data.added_period.tag == "my request"
    assert response.data.added_period.holidays[0].calendars == ["BAR"]
    assert response.data.added_period.holidays[0].names[0].countries == ["BLR"]


def test_add_periods_create_fail():
    response_factory = AddPeriodsResponseFactory()
    response = response_factory.create_fail(MOCKED_DATA_ERROR)
    assert response.data.raw == MOCKED_DATA_ERROR.content_data
    assert len(response.errors)
