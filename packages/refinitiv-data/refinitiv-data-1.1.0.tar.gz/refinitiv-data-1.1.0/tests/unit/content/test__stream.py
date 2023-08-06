import itertools
from unittest import mock
from unittest.mock import patch

import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data.content._universe_stream import _UniverseStream
from refinitiv.data.delivery import omm_stream
from refinitiv.data.delivery._stream import StreamState
from tests.unit.conftest import StubSession
from tests.unit.delivery.stream.conftest import StubStreamConnection, event_mock

key = "ewff"
default_value = "EWGE#32"
value = "fgwFG3fd3F#Q"


def test_name_is_none():
    with pytest.raises(AttributeError):
        _UniverseStream(content_type=ContentType.NONE, name=None)


def test_with_argument():
    list_attr = [
        "_session",
        "_extended_params",
        "_stream",
    ]
    session = mock.Mock()
    session._omm_stream_counter = itertools.count(5)
    stream = _UniverseStream(
        content_type=ContentType.NONE, name="EUR=", session=session
    )
    for attr in list_attr:
        assert hasattr(stream, attr)
    assert stream._session is not None


def test_decode_partial_update_field():
    session = mock.Mock()
    sp = _UniverseStream(content_type=ContentType.NONE, name="", session=session)
    sp._record = {"Fields": dict()}
    assert sp._decode_partial_update_field(key=key, value=value) == value


def test_stream__repr__(stream):
    # given
    expected_value = "{'name': 'name', 'service': None, 'fields': {}}"

    # when
    testing_value = repr(stream)

    # then
    assert testing_value == expected_value


def test_stream__iter__(stream):
    # when
    iterator = iter(stream)

    # then
    with pytest.raises(StopIteration):
        next(iterator)


def test_stream__getitem__(stream):
    # then
    with pytest.raises(KeyError, match="not in Stream cache"):
        # when
        stream["item"]


def test_stream__len__(stream):
    # when
    testing_value = len(stream)

    # then
    assert testing_value == 0


def test_call_stream_close_for_unopened_stream(stream):
    # when
    state = stream.close()

    # then
    assert state is StreamState.Unopened, state


def test_stream_on_update(stream):
    # given
    callback_called = False

    def on_update(*owner):
        nonlocal callback_called
        callback_called = True

    stream.on_update(on_update)

    # when
    stream._stream._on_stream_update(dict(), {"Fields": {}})

    # then
    assert callback_called is True


def test_stream_on_status(stream):
    # given
    callback_called = False

    def on_status(owner, fields):
        nonlocal callback_called
        callback_called = True

    stream.on_status(on_status)

    # when
    stream._stream._on_stream_status(dict(), {"State": dict()})

    # then
    assert callback_called is True


def test_stream_on_complete(stream):
    # given
    callback_called = False

    def on_complete(owner):
        nonlocal callback_called
        callback_called = True

    stream.on_complete(on_complete)

    # when
    stream._stream._on_stream_complete(dict())

    # then
    assert callback_called is True


def test_stream_on_error(stream):
    # given
    callback_called = False

    def on_error(owner, fields):
        nonlocal callback_called
        callback_called = True

    stream.on_error(on_error)

    # when
    stream._stream._on_stream_error({}, {})

    # then
    assert callback_called is True


def test_stream_keys(stream):
    keys = stream.keys()

    assert keys is not None


def test_stream_values(stream):
    values = stream.values()

    assert values is not None


def test_stream_items(stream):
    items = stream.items()

    assert items is not None


def test_stream___iter___raise_error(stream):
    iterator = iter(stream)

    with pytest.raises(StopIteration):
        next(iterator)


def test_stream___iter___():
    session = StubSession(is_open=True)
    stream = _UniverseStream(
        content_type=ContentType.NONE,
        name="EUR=",
        fields=["field"],
        session=session,
    )

    iterator = iter(stream)
    testing_value = next(iterator)

    assert testing_value is not None


def test_stream___getitem__raise_error(stream):
    key = "key"

    with pytest.raises(KeyError, match=f"Field '{key}' not in Stream cache"):
        stream[key]


def test_stream___len__(stream):
    length = len(stream)

    assert length == 0


def test_stream___str__(stream):
    s = str(stream)

    assert s == "Unknown service|name[]"


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_ommstream_open_with_updates_true():
    # given
    session = StubSession(is_open=True)
    definition = omm_stream.Definition(name="name")
    stream = definition.get_stream(session)
    stream._stream._opened = event_mock

    # when
    stream.open(with_updates=True)

    # then
    assert stream._stream.open_message["Streaming"] is True


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_ommstream_open_with_updates_false():
    # given
    session = StubSession(is_open=True)
    definition = omm_stream.Definition(name="name")
    stream = definition.get_stream(session)
    stream._stream._opened = event_mock

    # when
    stream.open(with_updates=False)

    # then
    assert stream._stream.open_message["Streaming"] is False


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_ommstream_open_with_updates_from_true_to_false():
    # given
    session = StubSession(is_open=True)
    definition = omm_stream.Definition(name="name")
    stream = definition.get_stream(session)
    stream._stream._opened = event_mock

    # when
    stream.open(with_updates=True)
    stream.close()
    stream.open(with_updates=False)

    # then
    assert stream._stream.open_message["Streaming"] is False


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_ommstream_open_with_updates_from_false_to_true():
    # given
    session = StubSession(is_open=True)
    definition = omm_stream.Definition(name="name")
    stream = definition.get_stream(session)
    stream._stream._opened = event_mock

    # when
    stream.open(with_updates=False)
    stream.close()
    stream.open(with_updates=True)

    # then
    assert stream._stream.open_message["Streaming"] is True
