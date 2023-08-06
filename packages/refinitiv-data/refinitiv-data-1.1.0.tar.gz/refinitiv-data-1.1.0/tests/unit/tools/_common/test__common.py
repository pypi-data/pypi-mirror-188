import pytest
from unittest.mock import MagicMock

from refinitiv.data._tools._common import (
    is_all_defined,
    is_any_defined,
    is_int,
    make_callback,
    urljoin,
    validate_types,
    CallbackHandler,
    bool_or_none_to_str,
    get_correct_filename,
)


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("1", True),
        (1, True),
        ({}, False),
        (None, False),
        ("1asb", False),
        ("", False),
    ],
)
def test_is_int(input_value, expected):
    # given

    # when
    testing_value = is_int(input_value)

    # then
    assert testing_value is expected, testing_value


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (
            ("https://api.refinitiv.com", "data/news/beta1"),
            "https://api.refinitiv.com/data/news/beta1",
        ),
        (
            ("https://api.refinitiv.com/", "data/news/beta1"),
            "https://api.refinitiv.com/data/news/beta1",
        ),
        (
            ("https://api.refinitiv.com/", "/data/news/beta1"),
            "https://api.refinitiv.com/data/news/beta1",
        ),
        (
            ("https://api.refinitiv.com/", "/data/news/beta1/"),
            "https://api.refinitiv.com/data/news/beta1/",
        ),
        (("https://api.refinitiv.com",), "https://api.refinitiv.com"),
        (("/", "data/news/beta1"), "/data/news/beta1"),
        (("/", "/data/news/beta1"), "/data/news/beta1"),
        (("data/news/beta1", "/"), "data/news/beta1/"),
        (("data/news/beta1/", "/"), "data/news/beta1/"),
        (("/data/news/beta1", "view"), "/data/news/beta1/view"),
        (("data/news/beta1/", "/{universe}"), "data/news/beta1/{universe}"),
    ],
)
def test_urljoin(input_value, expected):
    # given

    # when
    testing_url = urljoin(*input_value)

    # then
    assert testing_url == expected


def test_urljoin_without_arguments_return_empty_string():
    # given
    expected = ""

    # when
    testing_url = urljoin()

    # then
    assert testing_url == expected, testing_url


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (([1], [1]), True),
        (({1}, {1}), True),
        (({1: 1}, {1: 1}), True),
        (("1", "1"), True),
        ((1, 1), True),
        ((True, True), True),
        (([], [1]), False),
        (
            (
                set(),
                {
                    1,
                },
            ),
            False,
        ),
        (({}, {1: 1}), False),
        (("", "1"), False),
        ((0, 1), False),
        ((False, True), False),
    ],
)
def test_is_all_defined(input_value, expected):
    # given

    # when
    testing_url = is_all_defined(*input_value)

    # then
    assert testing_url == expected, testing_url


@pytest.mark.parametrize(
    "input_value, expected",
    [
        (([1], set(), {}, "", 0, False), True),
        (([], {1}, {}, "", 0, False), True),
        (([], set(), {1: 1}, "", 0, False), True),
        (([], set(), {}, "1", 0, False), True),
        (([], set(), {}, "", 1, False), True),
        (([], set(), {}, "", 0, True), True),
        (([], set(), {}, "", 0, False), False),
    ],
)
def test_is_any_defined(input_value, expected):
    # given

    # when
    testing_url = is_any_defined(*input_value)

    # then
    assert testing_url == expected, testing_url


@pytest.mark.parametrize(
    "value, types",
    [[1, [int, str]], [None, [int, str, type(None)]], [True, [bool, str]]],
)
def test_validate_types(value, types):
    validate_types(value, types)


@pytest.mark.parametrize(
    "value, types, message",
    [
        [
            1,
            [bool, str],
            "Parameter '' of invalid type provided: 'int', "
            "expected types: ['bool', 'str']",
        ],
        [
            None,
            [int, str],
            "Parameter '' of invalid type provided: 'NoneType', "
            "expected types: ['int', 'str']",
        ],
        [
            True,
            [int, str],
            "Parameter '' of invalid type provided: 'bool', "
            "expected types: ['int', 'str']",
        ],
        [
            None,
            [int, None],
            "Use 'type(None)' instead 'None', in 'types'",
        ],
    ],
)
def test_validate_types_exception(value, types, message):
    with pytest.raises(TypeError) as exc:
        validate_types(value, types)
    assert str(exc.value) == message


def test_make_callback():
    stream = MagicMock(name="stream")
    arg = {}
    func = MagicMock(name="func")
    my_callback = make_callback(func)
    my_callback(stream, arg)
    func.assert_called_once_with(arg, stream)


def test_callback_called():
    func = MagicMock(name="func")
    test_args = ("test", 1, [])
    handler = CallbackHandler()

    handler.on("test", func)
    handler.emit("test", *test_args)

    func.assert_called_once_with(*test_args)


def test_callback_not_called():
    func = MagicMock(name="func")
    test_args = ("test", 1, [])
    handler = CallbackHandler()

    handler.on("test", func)
    handler.remove_listener("test", func)
    handler.emit("test", *test_args)

    func.assert_not_called()


def test_callback_replaced():
    func = MagicMock(name="func")
    func2 = MagicMock(name="func2")
    test_args = ("test", 1, [])
    handler = CallbackHandler()

    handler.on("test", func)
    handler.on("test", func2)
    handler.emit("test", *test_args)

    func.assert_not_called()
    func2.assert_called_once_with(*test_args)


def test_all_callbacks_called():
    func = [MagicMock(name=f"func{i}") for i in range(10)]
    test_args = ("test", 1, [])
    handler = CallbackHandler(max_listeners=10)

    for f in func:
        handler.on("test", f)
    handler.emit("test", *test_args)

    for f in func:
        f.assert_called_once_with(*test_args)


def test_callback_called_multiple():
    func = MagicMock(name="func")
    test_args = ("test", 1, [])
    handler = CallbackHandler()
    test_call_count = 10

    handler.on("test", func)
    for _ in range(test_call_count):
        handler.emit("test", *test_args)

    assert func.call_count == test_call_count


def test_all_callbacks_removed():
    func = [MagicMock(name=f"func{i}") for i in range(10)]
    test_args = ("test", 1, [])
    handler = CallbackHandler(max_listeners=10)

    for f in func:
        handler.on("test", f)
    handler.remove_all_listeners()
    handler.emit("test", *test_args)

    for f in func:
        f.assert_not_called()


def test_all_callbacks_by_event_removed():
    func1 = MagicMock(name="func1")
    funcs = [MagicMock(name=f"func{i}") for i in range(10)]
    test_args = ("test", 1, [])
    handler = CallbackHandler(max_listeners=10)

    for f in funcs:
        handler.on("test", f)
    handler.on("test2", func1)
    handler.remove_all_listeners("test")
    handler.emit("test", *test_args)
    handler.emit("test2", *test_args)

    for f in funcs:
        f.assert_not_called()
    func1.assert_called_once_with(*test_args)


@pytest.mark.parametrize(
    "input_value, expected",
    [
        [True, "true"],
        [False, "false"],
        [1, 1],
        [0, 0],
        [None, ""],
        ["test", "test"],
        [[], []],
    ],
)
def test_bool_or_none_to_str(input_value, expected):
    testing_result = bool_or_none_to_str(input_value)

    assert testing_result == expected


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        (
            "RFT-DSP-VotingRights-v2-Delta15-2021-08-16T13:30:36.571Z.jsonl.gz",
            "RFT-DSP-VotingRights-v2-Delta15-2021-08-16T133036.571Z.jsonl.gz",
        ),
        (
            'RFT-DSP-VotingRights-v2-Delta15-2021-08-16T13:30:36."571Z.jsonl.gz',
            "RFT-DSP-VotingRights-v2-Delta15-2021-08-16T133036.571Z.jsonl.gz",
        ),
        (
            'RFT-DSP-VotingRights|v2-Delta15-2021-08-16T13:30:36."571Z.jsonl.gz',
            "RFT-DSP-VotingRightsv2-Delta15-2021-08-16T133036.571Z.jsonl.gz",
        ),
        ("file?name.json", "filename.json"),
    ],
)
def test_get_correct_filename(test_value, expected_result):
    # given
    # when
    result = get_correct_filename(test_value)

    # then
    assert result == expected_result
