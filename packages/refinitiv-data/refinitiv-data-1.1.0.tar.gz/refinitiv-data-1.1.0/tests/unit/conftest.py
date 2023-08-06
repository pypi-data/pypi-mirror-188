import json
import os
import sys
import threading
from collections.abc import Iterable
from types import SimpleNamespace

import pytest

from refinitiv.data import _configure as configure
from refinitiv.data._core.session import set_default
from refinitiv.data._core.session._session import Session
from refinitiv.data._core.session._session_cxn_factory import SessionConnection
from refinitiv.data._core.session._session_cxn_type import SessionCxnType
from refinitiv.data._core.session._session_type import SessionType
from refinitiv.data._core.session.grant_password import GrantPassword
from refinitiv.data._open_state import OpenState
from refinitiv.data.delivery._stream import stream_cxn_cache, get_cxn_cfg_provider

PROJECT_CONFIG_PATH = os.path.join(os.getcwd(), configure._default_config_file_name)


@pytest.fixture(autouse=True, scope="session")
def setup_teardown_session(request):
    print("\nDoing setup")

    def fin():
        print("\nDoing teardown")
        import threading

        s = "\n\t".join([str(t) for t in threading.enumerate()])
        print(f"Threads:\n\t{s}")

    request.addfinalizer(fin)


@pytest.fixture(autouse=True)
def setup_teardown_function():
    import refinitiv.data as rd

    rd.session.set_default(None)

    cxns = stream_cxn_cache.get_all_cxns()
    for c in cxns:
        c.dispose()
        c.join()


@pytest.fixture(scope="function")
def write_project_config(project_config_path):
    def inner(arg):
        if isinstance(arg, dict):
            arg = json.dumps(arg)
        f = open(project_config_path, "w")
        f.write(arg)
        f.close()
        return project_config_path

    yield inner

    configure._dispose()

    remove_project_config()


@pytest.fixture()
def project_config_path():
    return PROJECT_CONFIG_PATH


def remove_project_config():
    remove_config(PROJECT_CONFIG_PATH)


def remove_config(path):
    while os.path.exists(path):
        try:
            os.remove(path)
        except (PermissionError, FileNotFoundError):
            pass


def is_dunder_method(s):
    return s.startswith("__") and s.endswith("__")


def remove_dunder_methods(iterable):
    return [item for item in iterable if not is_dunder_method(item)]


def assert_error(e):
    expected_message = "__init__() got an unexpected keyword argument 'extended_params'"
    if sys.version_info >= (3, 10):
        expected_message = (
            "Definition.__init__() got an unexpected keyword argument 'extended_params'"
        )
    testing_message = str(e)
    assert testing_message == expected_message, e


def kwargs(**_):
    return _


def args(**_):
    return _.values()


def remove_private_attributes(iterable):
    return [item for item in iterable if not item.startswith("_")]


def get_property_names(cls):
    return [p for p in dir(cls) if isinstance(getattr(cls, p, None), property)]


def has_property_names_in_class(cls, expected_property_names):
    if isinstance(expected_property_names, dict):
        expected_property_names = list(expected_property_names.keys())
    return set(get_property_names(cls)) == set(expected_property_names)


def load_json(filepath):
    with open(filepath, "r") as f:
        s = f.read()
        o = json.loads(s)
    return o


class StubConfig(dict):
    def __init__(self, d=None) -> None:
        super().__init__()
        d = d or {}
        for k, v in d.items():
            self[k] = v

    def get_str(self, key):
        return str(self[key])

    def remove_listener(self, *args, **kwargs):
        pass

    def get_list(self, key):
        return list(self[key])

    def get_param(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"Config object doesn't have '{key}' attribute")


class StubConfigure(object):
    def __init__(self, config=None) -> None:
        super().__init__()
        config = config or StubConfig()
        self.config = config

        keys = SimpleNamespace()
        keys.platform_session = lambda key: f"platform_{key}"
        keys.desktop_session = lambda key: f"desktop_{key}"
        keys.log_file_enabled = "key_log_file_enabled"
        keys.log_console_enabled = "key_log_console_enabled"
        keys.log_level = "key_log_level"
        keys.log_filter = "key_log_filter"
        self.keys = keys

    def get(self, key, default=None):
        if "platform" in key and self.config.get("platform_config"):
            return self.config.get("platform_config")

        if "desktop" in key and self.config.get("desktop_config"):
            return self.config.get("desktop_config")

        if self.config.get(key):
            return self.config.get(key)

        return default

    def get_str(self, key):
        return str(self.get(key))


class StubResponse:
    def __init__(self, content_data=None, status_code=None, mocked_json=None) -> None:
        self.status_code = status_code or 200
        self.text = "test_text"

        request = SimpleNamespace()
        request.headers = {}
        request.url = SimpleNamespace()
        request.url.path = "test_url"

        self.request = request

        self.http_headers = {"content-type": "application/json; charset=utf-8"}
        self.headers = self.http_headers

        self._json = mocked_json or {"data": [{}], "headers": []}
        if content_data:
            self._json = content_data

    def json(self):
        return self._json


class StubSession(Session):
    type = SessionType.NONE

    def __init__(
        self,
        is_open=False,
        config=None,
        response=None,
        fail_if_error=False,
        deployed_platform_host=None,
        session_cxn_type=SessionCxnType.REFINITIV_DATA,
        stream_auto_reconnection=False,
    ) -> None:
        super().__init__(app_key="app_key")

        self._session_cxn_type = session_cxn_type
        self._deployed_platform_host = deployed_platform_host

        def error(message):
            if fail_if_error:
                pytest.fail(str(message))
            else:
                print(message)

        if isinstance(response, list):
            response = iter(response)

        self._response = response
        self.log = lambda *_, **__: None
        self.info = lambda *_, **__: None
        self.debug = lambda *_, **__: None
        self.error = error
        self.exception = error
        self.warning = lambda *_, **__: None
        self._log = lambda *_, **__: None
        self._info = lambda *_, **__: None
        self._debug = lambda *_, **__: None
        self._error = error
        self._exception = error
        self._warning = lambda *_, **__: None

        logger = SimpleNamespace()
        logger.handlers = []
        logger.log = lambda *_, **__: None
        logger.info = lambda *_, **__: None
        logger.debug = lambda *_, **__: None
        logger.error = error
        logger.exception = error
        logger.warning = lambda *_, **__: None
        self._logger = logger
        self._grant = GrantPassword(username="username", password="password")
        import random

        self._logger.name = f"StubSession_{random.random()}"

        self._is_open = is_open

        self._config = config
        if config is None:
            from refinitiv.data import _configure

            self._config = _configure.get_config()

        self._async_mode = False
        self.http_responses = success_http_response_generator()

        self._stream_auto_reconnection = stream_auto_reconnection

    @property
    def signon_control(self):
        return True

    @property
    def stream_auto_reconnection(self):
        return self._stream_auto_reconnection

    @property
    def authentication_token_endpoint_url(self):
        return ""

    @property
    def server_mode(self):
        return False

    @property
    def _connection(self) -> "SessionConnection":
        connection = SimpleNamespace()
        return connection

    @property
    def is_open(self):
        return self._is_open

    @property
    def is_closed(self):
        return not self._is_open

    @property
    def config(self):
        return self._config

    def logger(self):
        return self._logger

    @property
    def open_state(self):
        return OpenState.Opened if self.is_open else OpenState.Closed

    def _get_rdp_url_root(self):
        return "test_get_rdp_url_root"

    def _get_udf_url(self):
        return "test_get_udf_url"

    async def http_request_async(self, *_, **__):
        if self.async_mode:
            return next(self.http_responses)
        elif isinstance(self._response, Iterable):
            return next(self._response)
        else:
            return self._response or StubResponse()

    def http_request(self, *_, **__):
        if self.async_mode:
            return next(self.http_responses)
        elif isinstance(self._response, Iterable):
            return next(self._response)
        else:
            return self._response or StubResponse()

    async def open_async(self) -> OpenState:
        # do nothing
        pass

    def close(self):
        self._is_open = False
        stream_cxn_cache.close_cxns(self)

    @property
    def async_mode(self):
        return self._async_mode

    @async_mode.setter
    def async_mode(self, value: bool):
        self._async_mode = bool(value)

    def get_omm_login_message(self):
        return {}

    def _get_session_cxn_type(self) -> SessionCxnType:
        return self._session_cxn_type

    def get_rdp_login_message(self, stream_id):
        return {}


class Stub404OperationResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 404
        self.reason = "Page not found"
        self.text = "Not found"


class Stub202AcceptedRequestResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 202
        self.text = "Accepted"
        self.http_headers.update({"location": "location_url"})


class Stub202NoLocationRequestResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 202
        self.reason = "accepted"
        self.text = "Accepted"


class Stub200NotStartedOperationResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 200
        self.reason = "not_started"
        self.text = "Not started"
        self._json = {"status": "not_started"}


class Stub200RunningOperationResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 200
        self.reason = "OK"
        self.text = "Running"
        self._json.update({"status": "running"})


class StubNoPermissionsResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 200
        self.text = ""
        self._json = [
            {
                "universe": {"ric": "VOD.L"},
                "status": {
                    "code": "TS.Intraday.UserNotPermission.92000",
                    "message": "User has no permission.",
                },
            }
        ]


SUCCESS_RESPONSE_ID = "success_response_id"
FAILED_RESPONSE_ID = "failed_response_id"


class Stub403AccessDeniedResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 403
        self._json = {"error": {"message": "access denied."}}


class Stub200SucceededOperationResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 200
        self.reason = "OK"
        self.text = "Succeeded"

        self._json.update(
            {"status": "succeeded", "resourceLocation": SUCCESS_RESPONSE_ID}
        )


class Stub200FailedOperationResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 200
        self.reason = "OK"
        self.text = "Failed"

        self._json = {"status": "failed", "resourceLocation": FAILED_RESPONSE_ID}


class StubFailedResponse(StubResponse):
    def __init__(self) -> None:
        super().__init__()

        self.status_code = 400
        self.status = "failed"
        self.text = "Failed"

        self._json = {
            "error": {
                "id": FAILED_RESPONSE_ID,
                "code": "UNKNOWN_CODE",
                "status": "Bad Request",
                "message": "{id=03579501-f9dd-4bea-a9a3-bb115c882d8a, status=Error, message=Invalid input: Unsupported 'instrumentType' value., code=QPS-DPS.Error_InvalidInput_UnsupportedInstrumentType}",
            }
        }


def success_http_response_generator():
    for response in [
        Stub202AcceptedRequestResponse(),
        Stub200RunningOperationResponse(),
        Stub200SucceededOperationResponse(),
        StubResponse(),
    ]:
        yield response


def error_404_http_response_generator():
    for response in [Stub404OperationResponse()]:
        yield response


def error_403_access_denied_http_response_generator():
    for response in [Stub403AccessDeniedResponse()]:
        yield response


def error_no_location_http_response_generator():
    for response in [Stub202NoLocationRequestResponse()]:
        yield response


def error_request_failed_http_response_generator():
    for response in [
        Stub202AcceptedRequestResponse(),
        Stub200RunningOperationResponse(),
        Stub200FailedOperationResponse(),
        StubFailedResponse(),
    ]:
        yield response


def error_user_has_no_permissions():
    for response in [StubNoPermissionsResponse()]:
        yield response


def parametrize_with_test_case(args_names, test_cases, *test_case_ids):
    return pytest.mark.parametrize(
        args_names,
        [
            pytest.param(*test_case_data, id=test_case_id)
            for test_case_id, test_case_data in test_cases.items()
            if test_case_id in test_case_ids
        ],
    )


def send_ws_messages(session, stream_data):
    cxn_cfg_provider = get_cxn_cfg_provider(session)
    cxn_cfg_provider.start_connecting()

    cxn, ws = None, None
    stream_cxn_cache.cxn_created.clear()

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
        for message in stream_data:
            ws.cmd("on_message", json.dumps([message]))

    set_default(session)
    if stream_data:
        func_name = sys._getframe().f_code.co_name
        threading.Thread(
            name=f"{func_name}-1", target=get_cxn_ready, daemon=True
        ).start()
        threading.Thread(name=f"{func_name}-2", target=send, daemon=True).start()


class StubLogger:
    def __init__(self) -> None:
        dummy = lambda *args, **kwargs: None
        self.log = dummy
        self.warning = dummy
        self.error = dummy
        self.debug = dummy
        self.info = dummy
