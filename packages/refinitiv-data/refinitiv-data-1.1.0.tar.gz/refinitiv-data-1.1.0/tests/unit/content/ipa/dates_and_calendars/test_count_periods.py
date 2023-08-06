from refinitiv.data.content.ipa.dates_and_calendars import count_periods
from refinitiv.data.content.ipa.dates_and_calendars.count_periods._count_periods_data_provider import (
    CountPeriodsResponseFactory,
)
from refinitiv.data.delivery._data._data_provider import ParsedData


MOCKED_COUNT_PERIODS_DATA = ParsedData(
    {"http_status_code": 200, "http_reason": "OK"},
    {},
    [{"count": 6.0, "tag": "first tag", "tenor": "WD"}],
)

MOCKED_MULTIPLE_COUNT_PERIODS_DATA = ParsedData(
    {"http_status_code": 200, "http_reason": "OK"},
    {},
    [
        {"count": 6.0, "tag": "first tag", "tenor": "WD"},
        {"count": 9.0, "tag": "second tag", "tenor": "WD"},
    ],
)


def test_date_schedule():
    definition = count_periods.Definition(
        tag="first tag",
        start_date="2019-04-30",
        end_date="2020-04-30",
        period_type=count_periods.PeriodType.WORKING_DAY,
        currencies=["EUR"],
        calendars=["EMU"],
    )

    assert definition.request_item.tag == "first tag"
    assert definition.request_item.start_date == "2019-04-30"
    assert definition.request_item.end_date == "2020-04-30"
    assert definition.request_item.calendars == ["EMU"]
    assert definition.request_item.currencies == ["EUR"]
    assert definition.request_item.period_type == count_periods.PeriodType.WORKING_DAY


def test_holidays_create_success():
    response_factory = CountPeriodsResponseFactory()
    response = response_factory.create_success(MOCKED_COUNT_PERIODS_DATA)
    assert not response.data.df.empty
    assert response.data.raw == MOCKED_COUNT_PERIODS_DATA.content_data
    assert response.data.counted_period.count == 6
    assert response.data.counted_period.tag == "first tag"
    assert response.data.counted_period.tenor == "WD"


def test_holidays_definitions_create_success():
    response_factory = CountPeriodsResponseFactory()
    response = response_factory.create_success(MOCKED_MULTIPLE_COUNT_PERIODS_DATA)
    assert not response.data.df.empty
    assert response.data.raw == MOCKED_MULTIPLE_COUNT_PERIODS_DATA.content_data
    assert response.data.counted_periods[0].count == 6
    assert response.data.counted_periods[0].tag == "first tag"
    assert response.data.counted_periods[0].tenor == "WD"
    assert response.data.counted_periods[1].count == 9
    assert response.data.counted_periods[1].tag == "second tag"
    assert response.data.counted_periods[1].tenor == "WD"
