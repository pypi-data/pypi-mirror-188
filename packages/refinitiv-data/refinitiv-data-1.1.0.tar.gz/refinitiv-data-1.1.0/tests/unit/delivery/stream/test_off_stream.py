from refinitiv.data.delivery._stream import StreamState, StreamEvent
from refinitiv.data.delivery._stream._stream_factory import create_offstream_contrib
from refinitiv.data.delivery._stream.contrib._stream_connection import (
    OffStreamContribConnection,
)
from tests.unit.conftest import StubSession


def test_connection():
    session = StubSession()
    cxn = OffStreamContribConnection(1, "name", session, {})

    assert cxn.can_reconnect is False


def test_stream_contributed_is_set_false():
    session = StubSession(is_open=True)
    stream = create_offstream_contrib(session, "name", "api", "domain", "service")

    assert stream._contributed.is_set() is False


def test_stream_get_next_post_id():
    session = StubSession(is_open=True)
    stream = create_offstream_contrib(session, "name", "api", "domain", "service")

    assert stream.get_next_post_id() == 5


def test_stream_get_contrib_message():
    expected_contrib_message = {
        "Ack": True,
        "Domain": "domain",
        "ID": 2,
        "Key": {"Name": "name", "Service": "service"},
        "Message": {
            "Domain": "domain",
            "Fields": {"BID": 40.83},
            "ID": 0,
            "Type": "Update",
        },
        "PostID": 5,
        "Type": "Post",
    }
    session = StubSession(is_open=True)
    stream = create_offstream_contrib(session, "name", "api", "domain", "service")

    contrib_message = stream.get_contrib_message({"BID": 40.83}, "Update")

    assert contrib_message == expected_contrib_message


def test_stream_open():
    def mock_initialize_cxn():
        stream._cxn = OffStreamContribConnection(1, "name", session, {})
        stream._event = StreamEvent.get(stream.id)

    session = StubSession(is_open=True)
    stream = create_offstream_contrib(session, "name", "api", "domain", "service")
    stream._initialize_cxn = mock_initialize_cxn

    stream_state = stream.open()

    assert stream_state is StreamState.Opened


def test_stream_close():
    def mock_initialize_cxn():
        stream._cxn = OffStreamContribConnection(1, "name", session, {})
        stream._event = StreamEvent.get(stream.id)

    session = StubSession(is_open=True)
    stream = create_offstream_contrib(session, "name", "api", "domain", "service")
    stream._initialize_cxn = mock_initialize_cxn
    stream._release_cxn = lambda: None
    stream.open()

    stream_state = stream.close()

    assert stream_state is StreamState.Closed
