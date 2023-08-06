import pytest

from refinitiv.data._tools import merge_dict_to_dict
from refinitiv.data._tools._utils import camel_to_snake
from tests.unit.conftest import args


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("", ""),
        ("CamelCase", "camel_case"),
        ("camelCamelCase", "camel_camel_case"),
        ("camel2_camel2_case", "camel2_camel2_case"),
        ("getHTTPResponseCode", "get_http_response_code"),
        ("get2HTTPResponse123Code", "get2_http_response123_code"),
        ("HTTPResponseCodeXYZ", "http_response_code_xyz"),
        ("10CoolDudes", "10_cool_dudes"),
    ],
)
def test_base_create_str_definition_without_correct_module_path(input_str, expected):
    result = camel_to_snake(input_str)

    assert result == expected


@pytest.mark.parametrize(
    "dest, source, expected",
    [
        args(dest={}, source={}, expected={}),
        args(dest={"key": "value"}, source={"key": "value"}, expected={"key": "value"}),
        args(
            dest={"key": "value_old"},
            source={"key": "value_new"},
            expected={"key": "value_new"},
        ),
        args(
            dest={"key_old": "value_old"},
            source={"key_new": "value_new"},
            expected={"key_old": "value_old", "key_new": "value_new"},
        ),
        args(dest={"key": 1}, source={"key": 2}, expected={"key": 2}),
        args(
            dest={"key": [1, 2, 3]},
            source={"key": [4, 5, 6]},
            expected={"key": [4, 5, 6]},
        ),
        args(
            dest={"key1": {"key2": "value2"}},
            source={"key1": {"key2": "value_new", "key3": "value3"}},
            expected={"key1": {"key2": "value_new", "key3": "value3"}},
        ),
    ],
)
def test_merge_dict_to_dict(dest, source, expected):
    testing = merge_dict_to_dict(dest, source)
    assert testing == expected
