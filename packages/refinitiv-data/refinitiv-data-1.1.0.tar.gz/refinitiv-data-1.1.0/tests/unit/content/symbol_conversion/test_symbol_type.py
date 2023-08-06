from enum import Enum, unique

import pytest

from refinitiv.data.content.symbol_conversion import SymbolTypes
from refinitiv.data.content.symbol_conversion._symbol_type import (
    symbol_types_arg_parser,
)


@unique
class SomeEnum(Enum):
    Foo = "foo"
    Buzz = "buzz"


def test_throw_error_when_convert_some_enum():
    # given
    some_enum = SomeEnum.Foo

    # then
    with pytest.raises(AttributeError):
        SymbolTypes.convert_to_str(some_enum)


def test_throw_error_when_convert_incorrect_symbol_str():
    # given
    some_str = "foo"

    # then
    with pytest.raises(AttributeError):
        SymbolTypes.convert_to_str(some_str)


def test_convert_symbol_type_to_correct_str():
    # given
    for sym_type in SymbolTypes:
        # when
        sym_str = symbol_types_arg_parser.get_str(sym_type)

        # then
        assert sym_str == sym_type.value


def test_convert_correct_symbol_str_to_correct_str():
    # given
    for sym_str, item in SymbolTypes.__members__.items():
        # when
        conv_sym_str = symbol_types_arg_parser.get_str(sym_str)

        # then
        assert conv_sym_str == item.value


def test_convert_lower_symbol_str_to_correct_str():
    # given
    for sym_str, item in SymbolTypes.__members__.items():
        sym_str_lower = sym_str.lower()

        # when
        conv_sym_str = symbol_types_arg_parser.get_str(sym_str_lower)

        # then
        assert conv_sym_str == item.value


def test_convert_upper_symbol_str_to_correct_str():
    # given
    for sym_str, item in SymbolTypes.__members__.items():
        sym_str_upper = sym_str.upper()

        # when
        conv_sym_str = symbol_types_arg_parser.get_str(sym_str_upper)

        # then
        assert conv_sym_str == item.value


def test_empty_str_when_normalize_incorrect_symbol_str():
    # given
    sym_str = "RICfooo"

    # then
    with pytest.raises(AttributeError):
        # when
        symbol_types_arg_parser.get_str(sym_str)
