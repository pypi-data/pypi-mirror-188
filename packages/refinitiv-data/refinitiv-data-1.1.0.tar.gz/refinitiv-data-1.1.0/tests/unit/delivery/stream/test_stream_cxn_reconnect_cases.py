import threading
from types import SimpleNamespace
from typing import Optional
import sys

import pytest
from mock.mock import patch

from refinitiv.data import OpenState
from refinitiv.data.delivery._stream import (
    OMMStream,
    StreamConnection,
    get_cxn_cfg_provider,
)
from refinitiv.data.delivery._stream._stream_cxn_cache import (
    stream_cxn_cache,
)
from tests.unit.conftest import StubSession, StubResponse
from tests.unit.delivery.stream import raw_infos
from tests.unit.delivery.stream.conftest import StubWebSocketApp

# --------------------------------------------------------------------------------------
#
# TEST CASES
#
# --------------------------------------------------------------------------------------

"""
Given opened Stream
When network failure happens
Then Cxn is reconnecting, the Stream is opened
"""


# Stream perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_stream_does_not_close_when_cxn_get_network_failure_and_starts_reconnect():
    cxn: Optional["StreamConnection"] = None
    ws = None
    stream_cxn_cache.cxn_created.clear()

    def get_cxn_ready():
        nonlocal cxn, ws
        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws
        assert cxn.is_connecting is True, cxn.state

        ws.cmd("on_open")
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)
        message = '[{"Type": "Refresh", "Complete": true, "ID": 5}]'
        ws.cmd("on_message", message)

    session = StubSession(
        is_open=True,
        response=StubResponse(raw_infos.data),
        stream_auto_reconnection=True,
    )

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=get_cxn_ready, daemon=True).start()
    omm_stream.open()

    assert omm_stream.open_state is OpenState.Opened

    ws.cmd("on_close")
    cxn._listener_created.wait()

    assert cxn.is_connecting is True, cxn.state

    assert omm_stream.open_state is OpenState.Opened

    assert stream_cxn_cache.get_cxns(session) != []


"""
Given opened Stream
When network failure happens
Then Cxn starts cycling infos
And after of all waits some seconds
"""


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_cxn_cycle_infos_and_waits_after_iteration_of_all():
    cxn, ws = None, None
    cxn_ready = threading.Event()
    testing_num_reconnect = 0
    timer_starts = threading.Event()
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

    session = StubSession(
        is_open=True,
        response=StubResponse(raw_infos.data),
        stream_auto_reconnection=True,
    )
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=get_cxn_ready, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()
    omm_stream.open()

    timer_mock = SimpleNamespace()
    timer_mock.wait = lambda *args, **kwargs: timer_starts.set()
    cxn._timer = timer_mock
    expected_num_reconnect = cxn._config.num_infos

    while not timer_starts.is_set():
        ws.cmd("on_close")  # network failure
        cxn._listener_created.wait()  # wait start connecting
        ws = cxn._listener.ws
        testing_num_reconnect += 1

    assert cxn.is_connecting is True, cxn.state

    assert expected_num_reconnect == testing_num_reconnect


"""
Given opened Stream
And network failure happens
When Cxn cycling all infos
And waits from sequence
Then Timeout is the last time in the sequence
"""


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_when_cxn_cycle_infos_timer_get_timeout_in_sequence():
    cxn, ws = None, None
    cxn_ready = threading.Event()
    testing_delay = None
    testing_num_timer_starts = 0
    expected_num_timer_starts = 5
    timer_starts = threading.Event()
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

    session = StubSession(
        is_open=True,
        response=StubResponse(raw_infos.data),
        stream_auto_reconnection=True,
    )
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=get_cxn_ready, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()
    omm_stream.open()

    def timer_wait_mock(timeout):
        nonlocal testing_num_timer_starts, testing_delay
        testing_delay = timeout
        testing_num_timer_starts += 1
        timer_starts.set()

    timer_mock = SimpleNamespace()
    timer_mock.wait = timer_wait_mock
    cxn._timer = timer_mock

    delays = [5, 10, 15, 60, 60]
    for idx in range(expected_num_timer_starts):
        while not timer_starts.is_set():
            ws.cmd("on_close")  # network failure
            cxn._listener_created.wait()  # wait start connecting
            ws = cxn._listener.ws
        timer_starts.clear()
        expected_delay = delays[idx]
        assert expected_delay == testing_delay

    assert cxn.is_connecting is True, cxn.state

    assert testing_num_timer_starts == expected_num_timer_starts


"""
Given opened Stream
And network failure happens
When Cxn cycling all infos
And waits from sequence
And network restored
Then delays reset
And timeout take the first of the sequence
"""


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_when_cxn_cycle_infos_and_restore_network():
    ws, cxn = None, None
    testing_delay = None
    cxn_ready = threading.Event()
    timer_starts = threading.Event()
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

    session = StubSession(
        is_open=True,
        response=StubResponse(raw_infos.data),
        stream_auto_reconnection=True,
    )
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=get_cxn_ready, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()
    omm_stream.open()

    def timer_wait_mock(timeout):
        nonlocal testing_delay
        testing_delay = timeout
        timer_starts.set()

    timer_mock = SimpleNamespace()
    timer_mock.wait = timer_wait_mock
    cxn._timer = timer_mock

    delays = [5, 10, 15, 60, 60]
    for idx in range(5):
        while not timer_starts.is_set():
            ws.cmd("on_close")  # network failure
            cxn._listener_created.wait()  # wait start connecting
            ws = cxn._listener.ws
        timer_starts.clear()
        expected_delay = delays[idx]
        assert expected_delay == testing_delay

    reset_called = False

    def delays_reset_mock():
        nonlocal reset_called
        reset_called = True
        origin_delays_reset()

    origin_delays_reset = cxn._delays.reset
    cxn._delays.reset = delays_reset_mock

    ws.cmd("on_open")  # network restore

    assert reset_called is True

    assert cxn.is_connecting is True, cxn.state


"""
Given the Stream is connecting
When network failure happens
Then Cxn is reconnecting, the Stream is pending
"""


# Stream perspective


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_stream_does_not_close_when_cxn_get_network_failure_and_starts_reconnect():
    cxn, ws = None, None
    open_event = threading.Event()
    stream_cxn_cache.cxn_created.clear()

    def ws_open():
        nonlocal cxn, ws

        stream_cxn_cache.cxn_created.wait()
        cxn, *_ = stream_cxn_cache.get_cxns(session)
        cxn._listener_created.wait()
        ws = cxn._listener.ws
        ws.cmd("on_open")
        open_event.set()

    def ws_close():
        nonlocal ws
        open_event.wait()
        ws.cmd("on_close")  # network failure
        cxn._listener_created.wait()  # wait start connecting
        ws = cxn._listener.ws

        assert cxn.is_connecting is True, cxn.state
        assert omm_stream.open_state is OpenState.Pending

        # teardown
        cxn._is_auto_reconnect = False
        ws.cmd("on_close")
        omm_stream._stream._opened.set()

    session = StubSession(
        is_open=True,
        response=StubResponse(raw_infos.data),
        stream_auto_reconnection=True,
    )
    cxn_cfg_provider = get_cxn_cfg_provider(session._get_session_cxn_type())
    cxn_cfg_provider.start_connecting()

    omm_stream = OMMStream(session=session, name="name")
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=f"{func_name}-1", target=ws_open, daemon=True).start()
    threading.Thread(name=f"{func_name}-2", target=ws_close, daemon=True).start()
    omm_stream.open()


# --------------------------------------------------------------------------------------
