import os
from unittest.mock import MagicMock, patch

import pytest
from httpx import Client

from refinitiv.data import _configure as configure, OpenState
from refinitiv.data._core.session import PlatformSession, GrantPassword
from refinitiv.data.delivery._data._request import Request
from refinitiv.data.session import platform


# --------------------------------------------------------------------------------------
# self._auto_reconnect
# --------------------------------------------------------------------------------------


def test__auto_reconnect_property():
    # given
    expected_value = True
    definition = platform.Definition(
        app_key="app_key",
        grant=platform.GrantPassword(username="user", password="password"),
    )
    session = definition.get_session()

    # when
    testing_value = session.stream_auto_reconnection

    # then
    assert testing_value == expected_value


# --------------------------------------------------------------------------------------
# self._server_mode
# --------------------------------------------------------------------------------------


def test__server_mode_property():
    # given
    expected_value = False
    definition = platform.Definition(
        app_key="app_key",
        grant=platform.GrantPassword(username="user", password="password"),
    )
    session = definition.get_session()

    # when
    testing_value = session.server_mode

    # then
    assert testing_value == expected_value


# --------------------------------------------------------------------------------------
# self._base_url
# --------------------------------------------------------------------------------------


def test__base_url_property():
    # given
    expected_value = "https://api.refinitiv.com"
    definition = platform.Definition(
        app_key="app_key",
        grant=platform.GrantPassword(username="user", password="password"),
    )
    session = definition.get_session()

    # when
    testing_value = session._get_rdp_url_root()

    # then
    assert testing_value == expected_value


# --------------------------------------------------------------------------------------
# self._auth_url and self._auth_token
# --------------------------------------------------------------------------------------


def test_authentication_token_endpoint_url():
    # given
    expected_value = "https://api.refinitiv.com/auth/oauth2/v1/token"
    definition = platform.Definition(
        app_key="app_key",
        grant=platform.GrantPassword(username="user", password="password"),
    )
    session = definition.get_session()

    # when
    testing_value = session.authentication_token_endpoint_url

    # then
    assert testing_value == expected_value


def test__get_auth_token_uri():
    # given
    expected_value = "https://api.refinitiv.com/auth/oauth2/v1/token"
    definition = platform.Definition(
        app_key="app_key",
        grant=platform.GrantPassword(username="user", password="password"),
    )
    session = definition.get_session()

    # when
    testing_value = session._get_auth_token_uri()

    # then
    assert testing_value == expected_value


# --------------------------------------------------------------------------------------
# self._realtime_distribution_system_url
# --------------------------------------------------------------------------------------


def test__realtime_distribution_system_url_property():
    # given
    definition = platform.Definition(
        app_key="app_key",
        grant=platform.GrantPassword(username="user", password="password"),
    )
    session = definition.get_session()

    # when
    testing_value = session._deployed_platform_host

    # then
    assert testing_value is None


# --------------------------------------------------------------------------------------
# self._auth_authorize
# --------------------------------------------------------------------------------------


def test__auth_authorize_property():
    # given
    expected_value = "/authorize"
    definition = platform.Definition(
        app_key="app_key",
        grant=platform.GrantPassword(username="user", password="password"),
    )
    session = definition.get_session()

    # when
    testing_value = session._auth_authorize

    # then
    assert testing_value == expected_value


def test_session_name_is_set_right():
    session = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )
    assert session.name == "test"


def test_session_session_name_is_removed():
    session = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )
    with pytest.raises(AttributeError):
        session.session_name


def test_platform_session_has_config_snapshot_for_http_request_timeout_secs():
    # given
    session_a = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )

    # when
    config = configure.get_config()
    config["http.request-timeout"] = 1000
    session_b = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )

    # then
    assert session_a.http_request_timeout_secs != session_b.http_request_timeout_secs


def get_api_config(
    api_name,
    session,
):
    config = session.config
    api_config = config.get(f"apis.{api_name}")
    return api_config


def test_platform_session_has_config_snapshot_for_apis():
    # given
    session_a = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )

    # when
    config = configure.get_config()
    config["apis.data"] = {"changed key": "changed value"}
    session_b = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )

    # then
    api_config_a = get_api_config("data", session_a)
    api_config_b = get_api_config("data", session_b)
    assert api_config_a is not api_config_b


def test_platform_session_has_config_snapshot_for_get_streaming_websocket_endpoint_url():
    # given
    session_a = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )

    # when
    config = configure.get_config()
    config["apis.data"] = {"changed key": "changed value"}
    session_b = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )

    # then
    api_config_a = get_api_config("data", session_a)
    api_config_b = get_api_config("data", session_b)
    assert api_config_a is not api_config_b


def test_platform_session_has_config_snapshot_for_get_streaming_discovery_endpoint_url():
    # given
    session_a = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )

    # when
    config = configure.get_config()
    config["apis.data"] = {"changed key": "changed value"}
    session_b = PlatformSession(
        app_key="app_key",
        name="test",
        grant=platform.GrantPassword(username="user", password="password"),
    )

    # then
    api_config_a = get_api_config("data", session_a)
    api_config_b = get_api_config("data", session_b)
    assert api_config_a is not api_config_b


def test_platform_session_opens_and_closes_with_context_manager():
    def open_mock():
        return True

    # given
    grant = GrantPassword("username", "password")
    session = PlatformSession(app_key="app_key", grant=grant)
    origin_open = session._connection.open
    session._connection.open = open_mock

    # when
    with session:
        assert session.open_state is OpenState.Opened

    # then
    assert session.open_state is OpenState.Closed

    session._connection.open = origin_open


@pytest.mark.asyncio
async def test_platform_session_opens_and_closes_with_async_context_manager():
    def open_mock():
        return True

    # given
    grant = GrantPassword("username", "password")
    session = PlatformSession(app_key="app_key", grant=grant)
    origin_open = session._connection.open
    session._connection.open = open_mock

    # when
    async with session:
        assert session.open_state is OpenState.Opened

    # then
    assert session.open_state is OpenState.Closed

    session._connection.open = origin_open


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (True, True),
        (False, False),
    ],
)
def test_signon_control(input_value, expected_value):
    # when
    session = PlatformSession(app_key="app_key", signon_control=input_value)

    # then
    assert session._take_signon_control is expected_value


def test_signon_control_default_value():
    # when
    session = PlatformSession(app_key="app_key")

    # then
    assert session._take_signon_control is True
