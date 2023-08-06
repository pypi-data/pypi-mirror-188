import pytest

from refinitiv.data.content._intervals import (
    Intervals,
    DayIntervalType,
    get_day_interval_type,
)


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (Intervals.DAILY, DayIntervalType.INTER),
        (
            Intervals.SEVEN_DAYS,
            DayIntervalType.INTER,
        ),
        (Intervals.WEEKLY, DayIntervalType.INTER),
        (Intervals.MONTHLY, DayIntervalType.INTER),
        (
            Intervals.QUARTERLY,
            DayIntervalType.INTER,
        ),
        (
            Intervals.TWELVE_MONTHS,
            DayIntervalType.INTER,
        ),
        (Intervals.YEARLY, DayIntervalType.INTER),
        ("P1Y", DayIntervalType.INTER),
        (
            Intervals.ONE_MINUTE,
            DayIntervalType.INTRA,
        ),
        (
            Intervals.FIVE_MINUTES,
            DayIntervalType.INTRA,
        ),
        (
            Intervals.TEN_MINUTES,
            DayIntervalType.INTRA,
        ),
        (
            Intervals.THIRTY_MINUTES,
            DayIntervalType.INTRA,
        ),
        (
            Intervals.SIXTY_MINUTES,
            DayIntervalType.INTRA,
        ),
        (Intervals.ONE_HOUR, DayIntervalType.INTRA),
        ("PT1H", DayIntervalType.INTRA),
        (
            DayIntervalType.INTRA,
            DayIntervalType.INTRA,
        ),
    ],
)
def test_get_day_interval_type(input_value, expected_value):
    # when
    testing_value = get_day_interval_type(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_value",
    [
        "",
        None,
        "None",
    ],
)
def test_get_day_interval_type_raise_error_value(input_value):
    # then
    with pytest.raises(AttributeError, match=f"Value '{input_value}' must be in"):
        # when
        get_day_interval_type(input_value)


@pytest.mark.parametrize("input_value", [[], [[]]])
def test_get_day_interval_type_raise_error_incorrect_day_interval(input_value):
    # then
    with pytest.raises(TypeError, match="Incorrect day interval"):
        # when
        get_day_interval_type(input_value)
