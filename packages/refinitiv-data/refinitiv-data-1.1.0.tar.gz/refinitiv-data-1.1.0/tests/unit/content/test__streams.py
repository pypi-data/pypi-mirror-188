import copy
from unittest.mock import MagicMock, ANY

import pytest

from refinitiv.data._core.session import SessionType, DesktopSession
from refinitiv.data._content_type import ContentType
from refinitiv.data.content import pricing
from refinitiv.data.content._universe_streams import (
    _UniverseStreams,
    UniverseStreamFacade,
)
from refinitiv.data.delivery._stream import StreamState, StreamEvent
from tests.unit.conftest import StubSession
from concurrent.futures import ThreadPoolExecutor, wait


def test_get_item_error():
    # given
    session = StubSession()
    universe = ["RIC"]

    # when
    stream = _UniverseStreams(
        content_type=ContentType.NONE, universe=universe, session=session
    )

    # then
    assert stream["__mock__"] == {}


def test_universe_str():
    # given
    session = StubSession()
    universe = "RIC"

    try:
        # when
        _UniverseStreams(
            content_type=ContentType.NONE, universe=universe, session=session
        )
    except Exception as e:
        assert False, e


def test_stream__repr__(streams):
    # when
    testing_value = repr(streams)

    # then
    assert testing_value is not None


def test_stream__iter__(streams):
    # when
    iterator = iter(streams)

    # then
    assert next(iterator) is not None


def test_stream__getitem__(streams):
    # when
    streaming_price = streams["item"]

    # then
    assert streaming_price == {}


def test_stream__getitem__wrapper(streams):
    # when
    streams = streams["name"]

    # then
    assert isinstance(streams, UniverseStreamFacade)


def test_stream__len__(streams):
    # when
    testing_value = len(streams)

    # then
    assert testing_value == 1


def test_call_streams_close_for_unopened_streams(streams):
    # when
    state = streams.close()

    # then
    assert state is StreamState.Unopened, state


def test_stream_on_update(streams):
    # given
    callback_called = False

    def on_update(owner, name, fields):
        nonlocal callback_called
        callback_called = True

    streams.on_update(on_update)

    # when
    streams["name"]._stream._on_stream_update({}, {"Fields": {}})

    # then
    assert callback_called is True


def test_stream_on_status(streams):
    # given
    callback_called = False

    def on_status(owner, name, fields):
        nonlocal callback_called
        callback_called = True

    streams.on_status(on_status)

    # when
    streams["name"]._stream._on_stream_status({}, {"State": {}, "Fields": {}})

    # then
    assert callback_called is True


def test_stream_on_complete(streams):
    # given
    callback_called = False

    def on_complete(owner):
        nonlocal callback_called
        callback_called = True

    streams.on_complete(on_complete)

    # when
    streams["name"]._stream._on_stream_complete({})

    # then
    assert callback_called is True


def test_stream_on_error(streams):
    # given
    callback_called = False

    def on_error(owner, name, fields):
        nonlocal callback_called
        callback_called = True

    streams.on_error(on_error)

    # when
    streams["name"]._stream._on_stream_error({}, {})

    # then
    assert callback_called is True


def test_stream_keys(streams):
    keys = streams.keys()

    assert keys is not None


def test_stream_values(streams):
    values = streams.values()

    assert values is not None


def test_stream_items(streams):
    items = streams.items()

    assert items is not None


def test_stream___iter___raise_error(streams):
    iterator = iter(streams)

    next(iterator)

    with pytest.raises(StopIteration):
        next(iterator)


def test_stream___iter___():
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        content_type=ContentType.NONE,
        universe="universe",
        fields=["field"],
        session=session,
    )

    iterator = iter(stream)
    testing_value = next(iterator)

    assert testing_value is not None


def test_stream___len__(streams):
    length = len(streams)

    assert length == 1


def test_stream___str__(streams):
    s = str(streams)

    assert s is not None


def test__do_on_stream_update():
    # given
    data = [
        {
            "Fields": {"DATETIME": "2020-12-31T11:55:59.000Z", "TRDPRC_1": 123.456},
            "ID": 2,
            "Key": {"Name": "S)MySymbol.UUID", "Service": "CUSTOM_BASKETS"},
            "Type": "Update",
            "UpdateType": "Quote",
        }
    ]
    test_result = copy.copy(data[0])

    # when
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        content_type=ContentType.NONE, universe="", session=session
    )
    stream._record = data
    mock_stream = MagicMock()
    mock_stream.name = "Stream"
    result = stream._do_on_stream_update(mock_stream, *data)

    # then
    assert result[1] == test_result
    assert stream._record == data


def test__do_on_stream_refresh():
    # given
    data = [
        {
            "Fields": {"DATETIME": "2020-12-31T11:55:59.000Z", "TRDPRC_1": 123.456},
            "ID": 2,
            "Key": {"Name": "S)MySymbol.UUID", "Service": "CUSTOM_BASKETS"},
            "Type": "Update",
            "UpdateType": "Quote",
        }
    ]
    test_result = copy.copy(data[0])

    # when
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        content_type=ContentType.NONE, universe="", session=session
    )
    stream._record = data
    mock_stream = MagicMock()
    mock_stream.name = "Stream"
    result = stream._do_on_stream_refresh(mock_stream.MagicMock(), *data)

    # then
    assert result[1] == test_result
    assert stream._record == data


def test__add_instruments_when_close():
    test_data = ["VOD.L", "EUR=", "IBM"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(ContentType.NONE, universe="", session=session)
    stream.add_instruments(test_data)
    for i in test_data:
        assert i in stream._universe
    assert not stream.__dict__.get("_stream_by_name")


def test__remove_instruments_when_close():
    test_data = ["VOD.L", "IBM"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE, universe=["VOD.L", "EUR=", "IBM"], session=session
    )
    stream.remove_instruments(test_data)

    for i in test_data:
        assert i not in stream._universe
    assert not stream.__dict__.get("_stream_by_name")
    assert "EUR=" in stream._universe


def test__add_instruments_when_open():
    test_data = ["VOD.L", "EUR=", "IBM"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(ContentType.NONE, universe="", session=session)

    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._create_stream_by_name = lambda name: MagicMock()

    stream.add_instruments(test_data)
    for i in test_data:
        assert i in stream._stream_by_name
        assert i in stream._universe
    stream.close()


def test__remove_instruments_when_open():
    test_data = ["VOD.L", "IBM"]

    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE, universe=["VOD.L", "EUR=", "IBM"], session=session
    )
    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._create_stream_by_name = lambda name: MagicMock()

    stream.remove_instruments(test_data)
    for i in test_data:
        assert i not in stream._stream_by_name
        assert i not in stream._universe
    assert "EUR=" in stream._stream_by_name
    assert "EUR=" in stream._universe


def test__remove_instruments_when_universe_is_empty():
    test_data = ["VOD.L", "IBM"]
    call_counter = 0

    def _error(_):
        nonlocal call_counter
        call_counter += 1

    session = StubSession(is_open=True)
    stream = _UniverseStreams(ContentType.NONE, universe=[], session=session)
    stream._error = _error
    stream.remove_instruments(test_data)
    assert call_counter == 1


def test__remove_instruments_when_name_not_in_universe():
    test_data = ["VOD.L", "IBM"]
    call_counter = 0

    def _error(_):
        nonlocal call_counter
        call_counter += 1

    session = StubSession(is_open=True)
    stream = _UniverseStreams(ContentType.NONE, universe=["EUR="], session=session)
    stream._error = _error
    stream.remove_instruments(test_data)
    assert call_counter == 2


def test__only_one_complete():
    def on_complete(*args, **kwargs):
        pass

    test_data = ["VOD.L", "EUR=", "IBM"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(ContentType.NONE, universe="", session=session)
    stream.on_complete(on_complete)

    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._create_stream_by_name = lambda name: MagicMock()

    stream.add_instruments(test_data)
    for i in test_data:
        stream._stream_by_name[i].off.assert_called_with(StreamEvent.COMPLETE, ANY)


def test__add_fields_when_close():
    test_data = ["BID", "ASK"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE,
        universe=["VOD.L", "EUR=", "IBM"],
        fields=["TRDPRC_1"],
        session=session,
    )
    stream.add_fields(test_data)

    for i in test_data:
        assert i in stream.fields
    assert not stream.__dict__.get("_stream_by_name")


def test__add_fields_when_open():
    test_data = ["BID", "ASK"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE,
        universe=["VOD.L", "EUR=", "IBM"],
        fields=["TRDPRC_1"],
        session=session,
    )

    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._reopen_all_streams = lambda: ...

    stream.add_fields(test_data)
    for i in test_data:
        assert i in stream.fields
    stream.close()


def test__remove_fields_when_close():
    test_data = ["BID", "ASK"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE,
        universe=["VOD.L", "EUR=", "IBM"],
        fields=["TRDPRC_1", "BID", "ASK"],
        session=session,
    )
    stream.remove_fields(test_data)

    for i in test_data:
        assert i not in stream.fields
    assert not stream.__dict__.get("_stream_by_name")


def test__remove_fields_when_open():
    test_data = ["BID", "ASK"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE,
        universe=["VOD.L", "EUR=", "IBM"],
        fields=["TRDPRC_1", "BID", "ASK"],
        session=session,
    )

    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._reopen_all_streams = lambda: ...

    stream.remove_fields(test_data)
    for i in test_data:
        assert i not in stream.fields
    stream.close()


def make_error(expected_msg):
    def _error(msg):
        assert msg == expected_msg

    return make_error


def test_remove_not_exists_field():
    test_data = ["INVAL"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE,
        universe=["VOD.L", "EUR=", "IBM"],
        fields=["TRDPRC_1", "BID", "ASK"],
        session=session,
    )

    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._reopen_all_streams = lambda: ...
    stream._error = make_error("{'INVAL'} not in fields list")
    stream.remove_fields(test_data)

    stream.close()


def test_add_exists_field():
    test_data = ["TRDPRC_1"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE,
        universe=["VOD.L", "EUR=", "IBM"],
        fields=["TRDPRC_1", "BID", "ASK"],
        session=session,
    )

    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._reopen_all_streams = lambda: ...
    stream._error = make_error("{'TRDPRC_1'} already in fields list")
    stream.add_fields(test_data)

    stream.close()


def test_remove_not_exists_item():
    test_data = ["INVAL"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE,
        universe=["VOD.L", "EUR=", "IBM"],
        fields=["TRDPRC_1", "BID", "ASK"],
        session=session,
    )

    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._reopen_all_streams = lambda: ...
    stream._error = make_error("{'INVAL'} not in universe list")
    stream.remove_instruments(test_data)

    stream.close()


def test_add_exists_item():
    test_data = ["VOD.L"]
    session = StubSession(is_open=True)
    stream = _UniverseStreams(
        ContentType.NONE,
        universe=["VOD.L", "EUR=", "IBM"],
        fields=["TRDPRC_1", "BID", "ASK"],
        session=session,
    )

    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._reopen_all_streams = lambda: ...
    stream._error = make_error("{'TRDPRC_1'} already in universe list")
    stream.add_instruments(test_data)

    stream.close()


class StubDesktop(DesktopSession, StubSession):
    def __init__(self, *args, **kwargs):
        StubSession.__init__(self, *args, **kwargs)


def test__add_fields_when_open_desktop_session():
    test_data = ["BID", "ASK"]
    session = StubDesktop(is_open=True)
    session.type = SessionType.DESKTOP
    stream = _UniverseStreams(
        ContentType.NONE,
        universe=["VOD.L", "EUR=", "IBM"],
        fields=["TRDPRC_1"],
        session=session,
    )

    # open
    _ = stream._stream_by_name
    stream._state = StreamState.Opened
    stream._reopen_all_streams = lambda: ...
    stream._stream_by_name = {"a": MagicMock(), "B": MagicMock()}

    stream.add_fields(test_data)
    for i in test_data:
        assert i in stream.fields
        for stream_mock in stream._stream_by_name.values():
            stream_mock.off.assert_called()
            stream_mock.close.assert_called()
            stream_mock.open.assert_called()
    stream.close()


def test_add_items_and_remove_items_do_not_work_at_the_same_time():
    # given
    session = StubSession(is_open=True)
    definition = pricing.Definition(universe=["VOD.L", "IBM.N"])
    stream = definition.get_stream(session)

    def add_items():
        stream.add_items(["EUR="])
        # then
        assert "EUR=" in stream._universe

    def remove_items():
        stream.remove_items(["EUR="])
        # then
        assert "EUR=" not in stream._universe

    # when
    with ThreadPoolExecutor() as ex:
        futures = []
        for _ in range(100):
            futures.extend([ex.submit(add_items), ex.submit(remove_items)])
        wait(futures)


def test_add_fields_and_remove_fields_do_not_work_at_the_same_time():
    # given
    session = StubSession(is_open=True)
    definition = pricing.Definition(universe=["VOD.L"], fields=["BID", "ASK"])
    stream = definition.get_stream(session)

    def add_fields():
        stream.add_fields(["TRDPRC_1"])
        # then
        assert "TRDPRC_1" in stream._universe

    def remove_fields():
        stream.remove_fields(["TRDPRC_1"])
        # then
        assert "TRDPRC_1" not in stream._universe

    # when
    with ThreadPoolExecutor() as ex:
        futures = []
        for _ in range(100):
            futures.extend([ex.submit(add_fields), ex.submit(remove_fields)])
        wait(futures)
