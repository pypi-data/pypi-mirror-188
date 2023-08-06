import numpy

from refinitiv.data.content.ipa.dates_and_calendars import date_schedule
from refinitiv.data.content.ipa.dates_and_calendars._request_factory import (
    DatesAndCalendarsResponseFactory,
)
from refinitiv.data.content.ipa.dates_and_calendars.date_schedule._date_schedule_data_provider import (
    DateSchedule,
)
from refinitiv.data.delivery._data._data_provider import ParsedData


CONVERTED_DATES = [
    numpy.datetime64("2019-05-07"),
    numpy.datetime64("2019-05-14"),
    numpy.datetime64("2019-05-21"),
    numpy.datetime64("2019-05-28"),
    numpy.datetime64("2019-06-04"),
    numpy.datetime64("2019-06-11"),
    numpy.datetime64("2019-06-18"),
    numpy.datetime64("2019-06-25"),
    numpy.datetime64("2019-07-02"),
    numpy.datetime64("2019-07-09"),
]

MOCKED_DATE_SCHEDULE_DATA = ParsedData(
    {"http_status_code": 200, "http_reason": "OK"},
    {},
    {
        "dates": [
            "2019-05-07",
            "2019-05-14",
            "2019-05-21",
            "2019-05-28",
            "2019-06-04",
            "2019-06-11",
            "2019-06-18",
            "2019-06-25",
            "2019-07-02",
            "2019-07-09",
        ]
    },
)


def test_date_schedule():
    definition = date_schedule.Definition(
        start_date="2019-04-30",
        count=10,
        frequency="Weekly",
        calendars=["EMU", "GER"],
        currencies=["EUR"],
        day_of_week=date_schedule.DayOfWeek.TUESDAY,
    )

    assert (
        definition.request_item.frequency == date_schedule.DateScheduleFrequency.WEEKLY
    )
    assert definition.request_item.start_date == "2019-04-30"
    assert definition.request_item.count == 10
    assert definition.request_item.calendars == ["EMU", "GER"]
    assert definition.request_item.currencies == ["EUR"]
    assert definition.request_item.day_of_week == date_schedule.DayOfWeek.TUESDAY


def test_holidays_create_success():
    response_factory = DatesAndCalendarsResponseFactory(data_class=DateSchedule)
    response = response_factory.create_success(MOCKED_DATE_SCHEDULE_DATA)
    assert not response.data.df.empty
    assert response.data.raw == MOCKED_DATE_SCHEDULE_DATA.content_data
    assert response.data.dates == CONVERTED_DATES
