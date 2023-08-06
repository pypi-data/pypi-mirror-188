import threading

import pytest
from mock.mock import patch

from refinitiv.data.delivery._stream import RDPStreamConnection
from refinitiv.data.delivery._stream.stream_cxn_state import StreamCxnState
from tests.unit.conftest import StubSession
from tests.unit.delivery.stream.conftest import StubStreamCxnConfig, StubWebSocketApp
import sys


# --------------------------------------------------------------------------------------
#
# TEST TRANSITIONS
#
# --------------------------------------------------------------------------------------


def test_after_cxn_is_created_state_is_initial():
    # given
    sess = StubSession()
    cfg = StubStreamCxnConfig()

    # when
    cxn = RDPStreamConnection(connection_id=1, name="name", session=sess, config=cfg)

    # then
    assert cxn.state is StreamCxnState.Initial, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_initial_to_connecting(create_omm_cxn):
    # given
    cxn = create_omm_cxn()

    assert cxn.state is StreamCxnState.Initial, cxn.state

    # when
    cxn.wait_start()

    # then
    assert cxn.is_connecting is True, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_connecting_to_message_processing(create_omm_cxn):
    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws

    # when
    ws.cmd("on_open")
    # here ws sends login message
    assert cxn.is_connecting is True, cxn.state

    # response
    message = '[{"State": {"Stream": "Open"}}]'
    ws.cmd("on_message", message)

    # then
    assert cxn.is_message_processing is True, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_message_processing_to_disconnecting(create_omm_cxn):
    def get_response():
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)

    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws
    ws.cmd("on_open")
    # here ws sends login message

    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=get_response, daemon=True).start()
    cxn.wait_connection_result()

    assert cxn.is_message_processing is True, cxn.state

    cxn.start_disconnecting()

    assert cxn.is_disconnecting, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_disconnecting_to_disconnected(create_omm_cxn):
    def get_response():
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)

    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws
    ws.cmd("on_open")
    # here ws sends login message
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=get_response, daemon=True).start()
    cxn.wait_connection_result()
    cxn.start_disconnecting()

    assert cxn.is_disconnecting, cxn.state

    cxn.end_disconnecting()

    assert cxn.is_disconnected, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_disconnected_to_disposed(create_omm_cxn):
    def get_response():
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)

    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws
    ws.cmd("on_open")
    # here ws sends login message
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=get_response, daemon=True).start()
    cxn.wait_connection_result()
    cxn.start_disconnecting()
    cxn.end_disconnecting()

    assert cxn.is_disconnected, cxn.state

    cxn.dispose()

    assert cxn.is_disposed, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_connecting_to_disconnected(create_omm_cxn):
    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws

    # when
    ws.cmd("on_open")
    # here ws sends login message

    assert cxn.is_connecting is True, cxn.state

    # response
    message = '[{"State": {"Stream": "Close"}}]'
    ws.cmd("on_message", message)
    ws.cmd("on_close")
    cxn.wait_connection_result()

    # then
    assert cxn.is_disposed is True, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_connecting_to_disposed(create_omm_cxn):
    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws

    # when
    ws.cmd("on_open")
    # here ws sends login message

    assert cxn.is_connecting is True, cxn.state

    cxn.dispose()

    # then
    assert cxn.is_disposed is True, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_connecting_cannot_to_disconnecting(create_omm_cxn):
    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws

    # when
    ws.cmd("on_open")
    # here ws sends login message

    assert cxn.is_connecting is True, cxn.state

    cxn.start_disconnecting()

    assert cxn.is_connecting is True, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_message_processing_cannot_to_disposed(create_omm_cxn):
    def get_response():
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)

    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws
    ws.cmd("on_open")
    # here ws sends login message
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=get_response, daemon=True).start()
    cxn.wait_connection_result()

    assert cxn.is_message_processing is True, cxn.state

    cxn.dispose()

    assert cxn.is_message_processing is True, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_message_processing_cannot_to_disconnected(create_omm_cxn):
    def get_response():
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)

    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws
    ws.cmd("on_open")
    # here ws sends login message
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=get_response, daemon=True).start()
    cxn.wait_connection_result()

    assert cxn.is_message_processing is True, cxn.state

    cxn.end_disconnecting()

    assert cxn.is_message_processing is True, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_from_message_processing_cannot_to_connecting_if_not_auto_reconnect(
    create_omm_cxn,
):
    def get_response():
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)

    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws
    ws.cmd("on_open")
    # here ws sends login message
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=get_response, daemon=True).start()
    cxn.wait_connection_result()

    assert cxn.is_message_processing is True, cxn.state

    ws.cmd("on_close")
    cxn.join()

    assert cxn.is_disposed is True, cxn.state


# --------------------------------------------------------------------------------------


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_cxn_cannot_cycle_infos_if_not_auto_reconnect(create_omm_cxn):
    def try_cycle_infos():
        message = '[{"State": {"Text": "Login Rejected."}}]'
        ws.cmd("on_message", message)
        ws.cmd("on_close")

    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws
    ws.cmd("on_open")

    # here ws sends login message

    def next_available_info_mock():
        assert False

    cxn._config.next_available_info = next_available_info_mock
    prev_info = cxn._config.info
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=try_cycle_infos, daemon=True).start()
    cxn.wait_connection_result()
    curr_info = cxn._config.info

    assert prev_info == curr_info
    assert cxn.is_disconnected, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_if_call_dispose_when_wait_connection_result_it_will_disposed(create_omm_cxn):
    def call_dispose():
        cxn.dispose()

    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws
    ws.cmd("on_open")
    # here ws sends login message
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=call_dispose, daemon=True).start()
    cxn.wait_connection_result()

    # then
    assert cxn.is_disposed, cxn.state


@pytest.mark.skipif(reason="hangs")
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_when_connection_result_is_success_state_is_message_processing(create_omm_cxn):
    def open_message():
        message = '[{"State": {"Stream": "Open"}}]'
        ws.cmd("on_message", message)

    # given
    cxn = create_omm_cxn()
    cxn.wait_start()
    ws = cxn._listener.ws
    ws.cmd("on_open")
    # here ws sends login message
    func_name = sys._getframe().f_code.co_name
    threading.Thread(name=func_name, target=open_message, daemon=True).start()
    cxn.wait_connection_result()

    # then
    assert cxn.is_message_processing, cxn.state
