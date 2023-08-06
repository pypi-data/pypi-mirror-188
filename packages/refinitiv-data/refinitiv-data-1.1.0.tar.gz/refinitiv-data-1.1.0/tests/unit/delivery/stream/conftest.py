import threading
from collections import defaultdict
from types import SimpleNamespace
from typing import Union, List, Optional

import pytest

import refinitiv.data as rd
from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery._data._api_type import APIType
from refinitiv.data.delivery._stream import (
    StreamConnection,
    RDPStreamConnection,
    OMMStreamConnection,
)
from refinitiv.data.delivery._stream._protocol_type import ProtocolType
from refinitiv.data.delivery._stream._stream_cxn_config_data import (
    PlatformStreamCxnConfig,
    StreamServiceInfo,
)
from refinitiv.data.delivery._stream._stream_factory import StreamDetails
from refinitiv.data.delivery._stream.contrib import ContribResponse
from refinitiv.data.delivery._stream.contrib._offstream import _OffStreamContrib
from refinitiv.data.delivery._stream.contrib._response import (
    AckContribResponse,
    NullContribResponse,
)
from tests.unit.conftest import StubSession


@pytest.fixture(
    scope="function",
    params=[
        rd.content.pricing.Definition("universe"),
        rd.content.trade_data_service.Definition(),
        rd.delivery.rdp_stream.Definition("", [], [], {}, "api/path"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.pricing.chain.Definition("universe"),
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=[
        "pricing",
        "trade_data_service",
        "rdp_stream",
        "omm_stream",
        "pricing.chain",
        "financial_contracts.bond",
        "custom_instruments",
    ],
)
def stream(request):
    definition = request.param
    session = StubSession(is_open=True)
    stream = definition.get_stream(session)
    return stream


class StubWebSocketApp:
    def __init__(self, **kwargs) -> None:
        self.url = kwargs["url"]
        self.on_open = kwargs["on_open"]
        self.on_message = kwargs["on_message"]
        self.on_error = kwargs["on_error"]
        self.on_close = kwargs["on_close"]
        self.on_ping = kwargs["on_ping"]
        self.on_pong = kwargs["on_pong"]

        self._is_close = False
        self._cmdname = ""
        config_by_cmdname = {
            "on_open": {"func": self.on_open, "args": []},
            "on_message": {"func": self.on_message, "args": []},
            "on_error": {"func": self.on_error, "args": [Exception()]},
            "on_close": {"func": self._do_on_close, "args": ["", ""]},
            "on_ping": {"func": self.on_ping, "args": [{}]},
            "on_pong": {"func": self.on_pong, "args": [{}]},
        }
        self._config_by_cmdname = config_by_cmdname
        self._func_called = threading.Event()
        self._cmd = threading.Event()
        self._args_for_cmd = None

    def cmd(self, name, *args):
        cmds = self._config_by_cmdname.keys()
        if name in cmds:
            self._func_called.clear()
            self._args_for_cmd = args
            self._cmdname = name
            self._cmd.set()
            self._func_called.wait()
        else:
            raise ValueError(f"No such command: {name}, has: {cmds}")

    def _cmd_applet(self):
        while not self._is_close:
            self._cmd.wait()
            if self._is_close:
                break
            config = self._config_by_cmdname[self._cmdname]
            func = config["func"]
            args = self._args_for_cmd or config["args"]
            try:
                func(self, *args)
            except Exception as e:
                print(e)
            self._func_called.set()
            self._cmdname = ""
            if not self._is_close:
                self._cmd.clear()

    def run_forever(self, *args, **kwargs):
        t = threading.Thread(target=self._cmd_applet)
        t.start()
        t.join()

    def send(self, s):
        # do nothing
        pass

    def close(self):
        self._is_close = True
        self._cmd.set()
        self._func_called.set()

    def _do_on_close(self, ws, close_status_code: str, close_msg: str):
        self.on_close(ws, close_status_code, close_msg)
        self.close()


class StubStreamCxn(StreamConnection):
    def send(self, data: dict) -> None:
        # do nothing
        pass


class StubStreamCxnConfig(PlatformStreamCxnConfig):
    def __init__(
        self,
        infos: Union[List["StreamServiceInfo"], "StreamServiceInfo"] = None,
        protocols: Union[List[str], str] = None,
        transport: str = "websocket",
    ):
        infos = infos or [StreamServiceInfo("", "", "", "", "", "", "")]
        protocols = protocols or [""]
        super().__init__(infos, protocols, transport)


def create_stream_cxn(session, details):
    return StubStreamCxn(1, "name", session, {}, 1)


class StubStreamConnection:
    def __init__(self, *args, **kwargs) -> None:
        self.id = "id"
        self.name = "name"
        self.daemon = True
        self._connection_result_ready = threading.Event()
        self.is_disposed = False
        self.is_disconnecting = False
        self.is_disconnected = False
        self._callbacks = defaultdict(list)
        self.session = StubSession()

    def wait_connection_result(self):
        # do nothing
        pass

    def start(self):
        self._connection_result_ready.set()

    def on(self, event, callback):
        self._callbacks[event].append(callback)

    def send_message(self, msg):
        for event, callbacks in self._callbacks.items():
            if (
                "complete_stream" in event
                or "response_stream" in event
                or "refresh_stream" in event
            ):
                for cb in callbacks.copy():
                    try:
                        cb(self, {"key": "value"})
                    except:
                        pass

    def remove_listener(self, *args, **kwargs):
        pass

    def dispose(self, *args, **kwargs):
        pass

    def join(self, *args, **kwargs):
        pass


def dummy(*args, **kwargs):
    pass


timer_mock = SimpleNamespace()
timer_mock.wait = dummy

event_mock = SimpleNamespace()
event_mock.wait = dummy
event_mock.clear = dummy


@pytest.fixture(scope="function")
def create_rdp_cxn():
    cxn: Optional[RDPStreamConnection] = None

    def creator(stream_auto_reconnection=False) -> RDPStreamConnection:
        nonlocal cxn
        sess = StubSession(stream_auto_reconnection=stream_auto_reconnection)
        cfg = StubStreamCxnConfig()
        cxn = RDPStreamConnection(
            connection_id=1, name="fixture-name", session=sess, config=cfg
        )
        return cxn

    yield creator

    if not cxn.is_disposed:
        cxn.start_disconnecting()
        cxn.end_disconnecting()
        cxn.dispose()
        cxn.join()

    assert cxn.is_disposed, cxn.state


@pytest.fixture(scope="function")
def create_omm_cxn():
    cxn: Optional[OMMStreamConnection] = None

    def creator(stream_auto_reconnection=False) -> OMMStreamConnection:
        nonlocal cxn
        sess = StubSession(stream_auto_reconnection=stream_auto_reconnection)
        cfg = StubStreamCxnConfig()
        cxn = OMMStreamConnection(
            connection_id=1, name="fixture-name", session=sess, config=cfg
        )
        return cxn

    yield creator

    if not cxn.is_disposed:
        cxn.start_disconnecting()
        cxn.end_disconnecting()
        cxn.dispose()
        cxn.join()

    assert cxn.is_disposed, cxn.state


class StubOffStreamContrib(_OffStreamContrib):
    def __init__(self, session, raise_err=False, was_send=True) -> None:
        self.was_send = was_send
        self.raise_err = raise_err

        details = StreamDetails(
            ContentType.STREAMING_OFF_CONTRIB,
            ProtocolType.OMM_OFF_CONTRIB,
            APIType.STREAMING_CONTRIB,
        )
        super().__init__(1, session, "name", details, "service", "domain")

    def _do_open(self, *args, **kwargs):
        if self.raise_err:
            raise ConnectionError("Error message here")

    def send(self, data: dict) -> bool:
        return self.was_send

    def _dispose(self):
        pass

    def contribute(
        self,
        fields: dict,
        contrib_type: Union[str, "ContribType", None] = None,
        post_user_info: Optional[dict] = None,
    ) -> ContribResponse:
        if self.was_send:
            return AckContribResponse(
                {
                    "ID": 2,
                    "Type": "Ack",
                    "AckID": 5,
                    "Text": "[1]: Contribution Accepted",
                    "Key": {"Service": "ATS_GLOBAL_1", "Name": "TEST"},
                }
            )
        else:
            return NullContribResponse()

    async def contribute_async(
        self,
        fields: dict,
        contrib_type: Union[str, "ContribType", None] = None,
        post_user_info: Optional[dict] = None,
    ) -> ContribResponse:
        if self.was_send:
            return AckContribResponse(
                {
                    "ID": 2,
                    "Type": "Ack",
                    "AckID": 5,
                    "Text": "[1]: Contribution Accepted",
                    "Key": {"Service": "ATS_GLOBAL_1", "Name": "TEST"},
                }
            )
        else:
            return NullContribResponse()


def mock_create_offstream_contrib(session, *args, **kwargs):
    return StubOffStreamContrib(session)


def make_mock_create_offstream_contrib(raise_err=False, was_send=True):
    def inner(session, *args, **kwargs):
        return StubOffStreamContrib(session, raise_err, was_send)

    return inner
