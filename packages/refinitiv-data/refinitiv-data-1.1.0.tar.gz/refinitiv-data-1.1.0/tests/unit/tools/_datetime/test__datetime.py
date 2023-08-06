import datetime

import pytest

from refinitiv.data._tools._datetime import (
    hp_datetime_adapter,
    cfs_datetime_adapter,
    tds_datetime_adapter,
    NanosecondsFormatter,
    ownership_datetime_adapter,
)


@pytest.fixture(scope="function", params=[hp_datetime_adapter, tds_datetime_adapter])
def zbase_datetime_adapter(request):
    adapter = request.param
    return adapter


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("12.02.2021", "2021-12-02T00:00:00.000000000Z"),
        ("12/02/2021", "2021-12-02T00:00:00.000000000Z"),
        (datetime.date(2021, 12, 2), "2021-12-02T00:00:00.000000000Z"),
    ],
)
def test_zbased_datetime_adapter_get_str(input_value, expected, zbase_datetime_adapter):
    # when
    testing_value = zbase_datetime_adapter.get_str(input_value)

    # then
    assert testing_value == expected, testing_value


def test_zbased_datetime_adapter_get_str_will_raise_error_is_pass_none(
    zbase_datetime_adapter,
):
    # given
    input_value = None

    # then
    with pytest.raises(AttributeError):
        # when
        zbase_datetime_adapter.get_str(input_value)


@pytest.mark.parametrize(
    "input_value, expected",
    (
        ("11.10.2020 15:00", "2020-11-10T15:00:00Z"),
        ("11.10.2020", "2020-11-10T00:00:00Z"),
        ("11.10.2020 15:21:01", "2020-11-10T15:21:01Z"),
        ("11/10/2020 15:21:01", "2020-11-10T15:21:01Z"),
        ("11/10/2020", "2020-11-10T00:00:00Z"),
        ("11-10-2020", "2020-11-10T00:00:00Z"),
    ),
)
def test_cfs_datetime_adapter_get_str(input_value, expected):
    # when
    testing_value = cfs_datetime_adapter.get_str(input_value)

    # then
    assert testing_value == expected


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (datetime.timedelta(0), NanosecondsFormatter.NANOSECOND_LENGTH),
        (datetime.timedelta(-2), NanosecondsFormatter.NANOSECOND_LENGTH),
        (datetime.timedelta(2), NanosecondsFormatter.NANOSECOND_LENGTH),
    ],
)
def test_hp_datetime_adapter_return_correct_nanoseconds_with_timedelta(
    input_value, expected_value
):
    # when
    testing_value = hp_datetime_adapter.get_str(input_value)
    *_, nanoseconds_with_z = testing_value.split(".", maxsplit=1)
    nanoseconds = nanoseconds_with_z.replace("Z", "")
    testing_value = len(nanoseconds)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    ("input_value", "expected_value"),
    [
        ("20211210", "20211210"),
        ("2021.12.10", "20211210"),
        ("-1QA", "-1QA"),
    ],
)
def test_ownership_datetime_adapter(input_value, expected_value):
    # given
    # when
    result = ownership_datetime_adapter.get_str(input_value)

    # then
    assert result == expected_value
