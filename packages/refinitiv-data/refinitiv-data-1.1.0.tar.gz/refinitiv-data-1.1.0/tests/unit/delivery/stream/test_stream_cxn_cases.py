import threading
from typing import Optional

import pytest
from mock.mock import patch

from refinitiv.data import OpenState
from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery._data._api_type import APIType
from refinitiv.data.delivery._stream import (
    OMMStream,
    StreamConnection,
    get_cxn_cfg_provider,
)
from refinitiv.data.delivery._stream._protocol_type import ProtocolType
from refinitiv.data.delivery._stream._stream_cxn_cache import (
    StreamCxnCache,
    stream_cxn_cache,
)
from refinitiv.data.delivery._stream._stream_factory import StreamDetails
from tests.unit.conftest import StubSession, StubResponse
from tests.unit.delivery.stream import raw_infos
from tests.unit.delivery.stream.conftest import StubWebSocketApp
import sys

# --------------------------------------------------------------------------------------
#
# TEST CASES
#
# --------------------------------------------------------------------------------------

"""
Given opened Stream
When network failure happens
Then Cxn is disposed, the Stream is closed
"""


# Stream perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_stream_closes_when_cxn_get_network_failure():
    cxn, ws = None, None
    cxn_ready = threading.Event()
    stream_cxn_cache.cxn_created.clear()

    def get_cxn_ready():
        nonlocal cxn, ws

        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws

        ws.cmd("on_open")
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)
        cxn_ready.set()

    def send():
        cxn_ready.wait()
        message = '[{"Type": "Refresh", "Complete": true, "ID": 5}]'
        ws.cmd("on_message", message)

    session = StubSession(is_open=True, response=StubResponse(raw_infos.data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")

    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=get_cxn_ready, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()
    omm_stream.open()

    assert omm_stream.open_state is OpenState.Opened

    network_failure_event = threading.Event()

    def on_network_failure():
        network_failure_event.set()
        ws.cmd("on_close")

    threading.Thread(
        name=f"{func_name}-3", target=on_network_failure, daemon=True
    ).start()

    network_failure_event.wait()
    cxn.start_disconnecting()
    cxn.end_disconnecting()
    cxn.dispose()
    cxn.join()

    assert omm_stream.open_state is OpenState.Closed

    assert stream_cxn_cache.get_cxns(session) == []

    session.close()


# --------------------------------------------------------------------------------------

"""
Given the Stream is connecting
When user close the Session
Then Cxn is disposed, the Stream is opened
And user can close the Stream
"""


# Stream perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_close_session_when_stream_is_connecting():
    def close_session():
        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        session.close()

    stream_cxn_cache.cxn_created.clear()

    session = StubSession(is_open=True, response=StubResponse(raw_infos.data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=close_session, daemon=True).start()
    omm_stream.open()

    assert omm_stream.open_state is OpenState.Opened

    assert stream_cxn_cache.get_cxns(session) == []

    omm_stream.close()

    assert omm_stream.open_state is OpenState.Closed

    session.close()


"""
Given the Stream is opened
When user close the Session
Then Cxn is disposed, the Stream is closed
"""


# Stream perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_access_granted_then_close_session():
    ws, cxn = None, None
    cxn_ready = threading.Event()

    def get_cxn_ready():
        nonlocal cxn, ws

        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws

        ws.cmd("on_open")
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)
        message = '[{"Type": "Refresh", "Complete": true, "ID": 5}]'
        ws.cmd("on_message", message)
        cxn_ready.set()

    def send():
        cxn_ready.wait()
        message = '[{"Type": "Refresh", "Complete": true, "ID": 5}]'
        ws.cmd("on_message", message)

    stream_cxn_cache.cxn_created.clear()

    session = StubSession(is_open=True, response=StubResponse(raw_infos.data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=get_cxn_ready, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()
    omm_stream.open()

    assert omm_stream.open_state is OpenState.Opened

    assert stream_cxn_cache.get_cxns(session) != []

    session.close()

    assert stream_cxn_cache.get_cxns(session) == []

    assert omm_stream.open_state is OpenState.Closed


# --------------------------------------------------------------------------------------

"""
Given the Stream is connecting
When server response "State - Stream is Open"
Then Cxn is in message processing state
"""


# Stream perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_access_granted_when_stream_is_opening():
    cxn_ready = threading.Event()
    cxn, ws = None, None

    def get_cxn_ready():
        nonlocal cxn, ws

        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws
        ws.cmd("on_open")
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)
        cxn_ready.set()

    def send():
        cxn_ready.wait()
        message = '[{"Type": "Refresh", "Complete": true, "ID": 5}]'
        ws.cmd("on_message", message)

    stream_cxn_cache.cxn_created.clear()

    session = StubSession(is_open=True, response=StubResponse(raw_infos.data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=get_cxn_ready, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()
    omm_stream.open()

    assert stream_cxn_cache.get_cxns(session) != []

    assert omm_stream.open_state is OpenState.Opened

    session.close()


# Cache perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_access_granted_when_cache_get_cxn():
    def get_response():
        cache.cxn_created.wait()
        cxn, *_ = cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws
        ws.cmd("on_open")
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)

    session = StubSession(response=StubResponse(raw_infos.data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    details = StreamDetails(
        ContentType.STREAMING_PRICING,
        ProtocolType.OMM,
        APIType.STREAMING_PRICING,
    )
    cache = StreamCxnCache()
    cache.cxn_created.clear()

    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=get_response, daemon=True).start()
    cxn = cache.get_cxn(session, details)

    assert cxn.is_message_processing, cxn.state

    # teardown
    cxn.start_disconnecting()
    cxn.end_disconnecting()
    cxn.dispose()
    cxn.join()
    session.close()


# --------------------------------------------------------------------------------------

"""
Given the Stream is connecting
When server response "State - Stream is Closed"
Or server response "State - Text is Login Rejected."
Or server response "State - Code is UserUnknownToPermSys"
Then Cxn is disposed
And raise ConnectionError
"""


# Stream perspective


@pytest.mark.skipif(reason="hangs")
@pytest.mark.parametrize(
    "message",
    [
        '[{"State": {"Stream": "Closed"}}]',
        '[{"State": {"Text": "Login Rejected."}}]',
        '[{"State": {"Text": "Login Rejected."}}]',
    ],
)
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_access_denied_when_stream_is_opening_will_raise_error(message):
    cxn: Optional["StreamConnection"] = None
    stream_cxn_cache.cxn_created.clear()

    def get_cxn_result():
        nonlocal cxn
        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws
        ws.cmd("on_open")
        ws.cmd("on_message", message)

    session = StubSession(is_open=True, response=StubResponse(raw_infos.data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=get_cxn_result, daemon=True).start()

    try:
        omm_stream.open()
    except ConnectionError:
        assert True
    else:
        assert False

    assert stream_cxn_cache.get_cxns(session) == []

    assert cxn.is_disposed is True, cxn.state

    assert omm_stream.open_state is OpenState.Pending

    # teardown
    cxn.start_disconnecting()
    cxn.end_disconnecting()
    cxn.dispose()
    cxn.join()
    session.close()


# Cache perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_access_denied_when_cache_get_cxn_will_raise_error():
    cxn = None

    def stream_closed_message():
        nonlocal cxn
        cache.cxn_created.wait()
        cxn, *_ = cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws
        ws.cmd("on_open")
        message = '[{"State": {"Stream": "Closed"}}]'
        ws.cmd("on_message", message)

    from tests.unit.delivery.stream.raw_infos import data

    session = StubSession(response=StubResponse(data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    details = StreamDetails(
        ContentType.STREAMING_PRICING,
        ProtocolType.OMM,
        APIType.STREAMING_PRICING,
    )
    cache = StreamCxnCache()
    cache.cxn_created.clear()

    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=stream_closed_message, daemon=True).start()
    try:
        cache.get_cxn(session, details)
    except ConnectionError:
        assert cxn.is_disposed, cxn.state
    else:
        assert False

    # teardown
    cxn.start_disconnecting()
    cxn.end_disconnecting()
    cxn.dispose()
    cxn.join()
    session.close()


# --------------------------------------------------------------------------------------

# Stream perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_access_granted_then_close_stream_then_close_session():
    ws, cxn = None, None
    cxn_ready = threading.Event()

    def get_cxn_ready():
        nonlocal cxn, ws

        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws
        ws.cmd("on_open")
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)
        cxn_ready.set()

    def send():
        cxn_ready.wait()
        message = '[{"Type": "Refresh", "Complete": true, "ID": 5}]'
        ws.cmd("on_message", message)

    stream_cxn_cache.cxn_created.clear()

    session = StubSession(is_open=True, response=StubResponse(raw_infos.data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=get_cxn_ready, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()
    omm_stream.open()

    omm_stream.close()

    session.close()

    assert stream_cxn_cache.get_cxns(session) == []

    assert omm_stream.open_state is OpenState.Closed

    # teardown
    cxn.start_disconnecting()
    cxn.end_disconnecting()
    cxn.dispose()
    cxn.join()


# Stream perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_access_granted_then_close_stream_then_close_session():
    ws, cxn = None, None
    cxn_ready = threading.Event()

    def get_cxn_ready():
        nonlocal cxn, ws

        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws
        ws.cmd("on_open")
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)
        cxn_ready.set()

    def send():
        cxn_ready.wait()
        message = '[{"Type": "Refresh", "Complete": true, "ID": 5}]'
        ws.cmd("on_message", message)

    stream_cxn_cache.cxn_created.clear()

    session = StubSession(is_open=True, response=StubResponse(raw_infos.data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=get_cxn_ready, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()
    omm_stream.open()

    session.close()

    omm_stream.close()

    assert stream_cxn_cache.get_cxns(session) == []

    assert omm_stream.open_state is OpenState.Closed

    # teardown
    cxn.start_disconnecting()
    cxn.end_disconnecting()
    cxn.dispose()
    cxn.join()


# Stream perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_access_granted_then_close_stream_cxn_is_in_message_processing():
    ws, cxn = None, None
    cxn_ready = threading.Event()

    def get_cxn_ready():
        nonlocal cxn, ws

        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws
        ws.cmd("on_open")
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)
        cxn_ready.set()

    def send():
        cxn_ready.wait()
        message = '[{"Type": "Refresh", "Complete": true, "ID": 5}]'
        ws.cmd("on_message", message)

    stream_cxn_cache.cxn_created.clear()

    session = StubSession(is_open=True, response=StubResponse(raw_infos.data))
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=get_cxn_ready, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()
    omm_stream.open()

    omm_stream.close()

    cxn, *_ = stream_cxn_cache.get_cxns(session)

    assert cxn.is_message_processing is True, cxn.state

    # teardown
    cxn.start_disconnecting()
    cxn.end_disconnecting()
    cxn.dispose()
    cxn.join()
    session.close()
