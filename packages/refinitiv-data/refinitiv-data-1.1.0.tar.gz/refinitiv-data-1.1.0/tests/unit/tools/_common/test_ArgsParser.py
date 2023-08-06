import pytest

from refinitiv.data._tools._common import (
    ArgsParser,
    parse_list_of_str,
    fields_arg_parser,
    make_enum_arg_parser,
    make_parse_enum,
)
from .conftest import StubStrEnum


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (None, [None]),
        ([None], [None]),
        ("", [""]),
        ({}, [{}]),
        (tuple(), [()]),
        (set(), [set()]),
        ([], []),
    ],
)
def test_args_parser_get_list_return_list_type(input_value, expected_value):
    # given
    parser = ArgsParser(lambda _: _)

    # when
    l = parser.get_list(input_value)

    # then
    assert l == expected_value


def test_args_parser_get_str_return_str_type():
    # given
    parser = ArgsParser(lambda _: _)

    # when
    s = parser.get_str(None)

    # then
    assert isinstance(s, str)


def test_args_parser_get_str_with_delim_return_str_without_delim_if_only_one():
    # given
    delim = ","
    parser = ArgsParser(lambda _: _)

    # when
    s = parser.get_str([1], delim=delim)

    # then
    assert delim not in s


def test_args_parser_get_str_with_delim_return_str_with_delim_if_many():
    # given
    delim = ","
    parser = ArgsParser(lambda _: _)

    # when
    s = parser.get_str([1, 2], delim=delim)

    # then
    assert delim in s, s


@pytest.mark.parametrize(
    "input_value, expected_value",
    [([], []), ("string", ["string"]), (["string"], ["string"])],
)
def test_parse_list_of_str_success(input_value, expected_value):
    # when
    testing_value = parse_list_of_str(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_value",
    [
        [None],
        [1],
        ["string", 1],
    ],
)
def test_parse_list_of_str_raise_error_not_all_strings(input_value):
    # then
    with pytest.raises(ValueError, match="Not all elements are strings"):
        # when
        parse_list_of_str(input_value)


@pytest.mark.parametrize(
    "input_value",
    [
        None,
        1,
        {},
        set(),
        tuple(),
    ],
)
def test_parse_list_of_str_raise_error_invalid_type(input_value):
    # then
    with pytest.raises(TypeError, match="Invalid type, expected str or list"):
        # when
        parse_list_of_str(input_value)


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (StubStrEnum.VALUE_1, "VALUE_1"),
        (StubStrEnum.VALUE_1.value, "VALUE_1"),
        ("VALUE_1", "VALUE_1"),
        ([StubStrEnum.VALUE_1, "VALUE_2"], ["VALUE_1", "VALUE_2"]),
    ],
)
def test_make_parse_enum_success(input_value, expected_value):
    # given
    parse_enum = make_parse_enum(StubStrEnum)

    # when
    testing_value = parse_enum(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (StubStrEnum.VALUE_1, "VALUE_1"),
        (StubStrEnum.VALUE_1.value, "VALUE_1"),
        ("VALUE_1", "VALUE_1"),
        ([StubStrEnum.VALUE_1, "VALUE_2"], ["VALUE_1", "VALUE_2"]),
        (StubStrEnum.VALUE_1.value.lower(), "VALUE_1"),
        ("value_1", "VALUE_1"),
        ([StubStrEnum.VALUE_1.value.lower(), "value_2"], ["VALUE_1", "VALUE_2"]),
    ],
)
def test_make_parse_enum_with_can_be_lower_success(input_value, expected_value):
    # given
    parse_enum = make_parse_enum(StubStrEnum, can_be_lower=True)

    # when
    testing_value = parse_enum(input_value)

    # then
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_value",
    [
        None,
        1,
        {},
        "",
        "None",
    ],
)
def test_make_parse_enum_success_raise_error(input_value):
    # given
    parse_enum = make_parse_enum(StubStrEnum)

    # then
    with pytest.raises(AttributeError, match=f"Value '{input_value}' must be in"):
        # when
        parse_enum(input_value)


def test_fields_arg_parser():
    # given, when, then
    assert fields_arg_parser


def test_make_enum_arg_parser():
    # when
    parser = make_enum_arg_parser(StubStrEnum)

    # then
    assert parser


def test_args_parser_get_unique_return_list_type():
    # given
    parser = ArgsParser(lambda _: _)

    # when
    testing_value = parser.get_unique(None)

    # then
    assert isinstance(testing_value, list)


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ([1, 1, 1, 2, 2, 3], [1, 2, 3]),
        (["B", "C", "B", "A", "D"], ["B", "C", "A", "D"]),
        ([], []),
        (None, [None]),
    ],
)
def test_args_parser_get_unique_return_unique_list(input_value, expected_value):
    # given
    parser = ArgsParser(lambda _: _)

    # when
    testing_value = parser.get_unique(input_value)

    # then
    assert testing_value == expected_value
