import pytest

from refinitiv.data._tools._common import (
    args_parser,
    is_all_str,
    hp_universe_parser,
)


def test_args_parser_with_str():
    test_str = "EUR"

    result = args_parser(test_str)

    assert result == [test_str], f"String is not wrapped in list, result: {test_str}"


def test_args_parser_with_expect_none():
    input_val = None
    result = args_parser(input_val, expect_none=True)

    assert result is None, f"initial input was changed, result:{result}"


def test_args_parser_with_list():
    input_val = ["1", "2", "3"]
    result = args_parser(input_val)

    assert result == input_val, f"initial input was changed, result:{result}"


@pytest.mark.parametrize(
    "input_val",
    [
        123,
        ["1", 2, 3],
        (1, 2, 3),
        {"1": 1, "2": 3},
        None,
    ],
)
def test_args_parser_with_invalid_inputs(input_val):
    with pytest.raises(ValueError):
        args_parser(input_val)


@pytest.mark.parametrize(
    "input_val, expected",
    [
        ([1, "3", 2], False),
        (["1", "3", "2"], True),
    ],
)
def test_only_str_in(input_val, expected):
    assert is_all_str(input_val) == expected


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (["", " ", "boo"], ["boo"]),
        (["foo", "boo", "foo"], ["foo", "boo", "foo"]),
    ],
)
def test_hp_universe_parser(input_value, expected_value):
    actual = hp_universe_parser.get_list(input_value)

    assert actual == expected_value


def test_hp_universe_parser_with_empty_list():
    with pytest.raises(ValueError):
        hp_universe_parser.get_list([])
