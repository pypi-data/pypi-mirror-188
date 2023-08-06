from enum import Enum, unique

import pytest

from refinitiv.data.content.news._news_data_provider import sort_order_news_arg_parser
from refinitiv.data.content.news._sort_order import SortOrder


@unique
class SomeEnum(Enum):
    Foo = "foo"
    Buzz = "buzz"


@pytest.mark.unit
def test_throw_error_when_convert_some_enum():
    some_enum = SomeEnum.Foo

    with pytest.raises(AttributeError):
        sort_order_news_arg_parser.get_str(some_enum)


@pytest.mark.unit
def test_throw_error_when_convert_incorrect_symbol_str():
    some_str = "foo"

    with pytest.raises(AttributeError):
        sort_order_news_arg_parser.get_str(some_str)


@pytest.mark.unit
def test_convert_symbol_type_to_correct_str():
    for sym_type in SortOrder:
        sym_str = sort_order_news_arg_parser.get_str(sym_type)

        assert sym_str == sym_type.value


@pytest.mark.unit
def test_convert_correct_symbol_str_to_correct_str():
    for sym_str, item in SortOrder.__members__.items():
        with pytest.raises(AttributeError):
            sort_order_news_arg_parser.get_str(sym_str)


@pytest.mark.unit
def test_convert_lower_symbol_str_to_correct_str():
    for sym_str, item in SortOrder.__members__.items():
        sym_str_lower = sym_str.lower()
        with pytest.raises(AttributeError):
            sort_order_news_arg_parser.get_str(sym_str_lower)


@pytest.mark.unit
def test_convert_upper_symbol_str_to_correct_str():
    for sym_str, item in SortOrder.__members__.items():
        sym_str_upper = sym_str.upper()
        with pytest.raises(AttributeError):
            sort_order_news_arg_parser.get_str(sym_str_upper)
