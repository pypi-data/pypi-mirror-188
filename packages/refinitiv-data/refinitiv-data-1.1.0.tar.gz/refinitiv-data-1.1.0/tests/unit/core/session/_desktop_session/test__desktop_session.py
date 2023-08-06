import os
from unittest.mock import MagicMock, Mock, patch

import pytest
from httpx import Client

from refinitiv.data import OpenState
from refinitiv.data._core.session import DesktopSession
from refinitiv.data.delivery._data._request import Request
from refinitiv.data.session import desktop


# --------------------------------------------------------------------------------------
# self._base_url
# --------------------------------------------------------------------------------------


def test__base_url_property():
    # given
    expected_value = "http://localhost:9000"
    definition = desktop.Definition(app_key="app_key")
    session = definition.get_session()

    # when
    testing_value = session._get_base_url()

    # then
    assert testing_value == expected_value


# --------------------------------------------------------------------------------------
# self.set_port_number()
# --------------------------------------------------------------------------------------


def test__set_port_number():
    # given
    expected_value = "http://localhost:9000"
    definition = desktop.Definition(app_key="app_key")
    session = definition.get_session()

    session.set_port_number(9600)

    # when
    testing_value = session._get_base_url()

    # then
    assert testing_value == "http://localhost:9600"


# --------------------------------------------------------------------------------------
# self._dp_proxy_base_url
# --------------------------------------------------------------------------------------
def test__dp_proxy_base_url_property():
    # given
    expected_value = "https://dp_proxy_base_url:9000"
    os.environ["DP_PROXY_BASE_URL"] = expected_value
    session = desktop.Definition(app_key="app_key").get_session()

    # when
    testing_value = session._get_base_url()

    # then
    assert testing_value == expected_value

    os.environ.pop("DP_PROXY_BASE_URL")


# --------------------------------------------------------------------------------------
# self._rdp_url
# --------------------------------------------------------------------------------------


def test__rdp_url_property():
    # given
    expected_value = "http://localhost:9000/api/rdp"
    definition = desktop.Definition(app_key="app_key")
    session = definition.get_session()

    # when
    testing_value = session._get_rdp_url_root()

    # then
    assert testing_value == expected_value


# --------------------------------------------------------------------------------------
# self.get_port_number_from_range
# --------------------------------------------------------------------------------------


@pytest.mark.asyncio
async def test__get_port_number_from_range_successfully():
    # given
    expected_port = "36035"

    definition = desktop.Definition(app_key="app_key")
    session = definition.get_session()

    session._connection.debug = Mock()
    session._connection.check_proxy = Mock(return_value=True)

    # when
    testing_value = session._connection.get_port_number_from_range(
        ports=(expected_port,), url="http://localhost:1245"
    )

    # then
    assert testing_value == expected_port
    session._connection.debug.assert_called_with(
        f"Default proxy port {expected_port} was successfully checked"
    )


@pytest.mark.asyncio
async def test__get_port_number_from_range_fail():
    # given
    expected_port = "36035"

    definition = desktop.Definition(app_key="app_key")
    session = definition.get_session()

    session._connection.debug = Mock()
    session._connection.check_proxy = Mock(return_value=False)

    # when
    testing_value = session._connection.get_port_number_from_range(
        ports=(expected_port,), url="http://localhost:1245"
    )

    # then
    assert testing_value is None
    session._connection.debug.assert_called_with(
        f"Default proxy port #{expected_port} failed"
    )


def test_desktop_session_opens_and_closes_with_context_manager():
    def open_mock():
        return True

    # given
    session = DesktopSession(app_key="app_key")
    session._connection.open = open_mock

    # when
    with session:
        assert session.open_state is OpenState.Opened

    # then
    assert session.open_state is OpenState.Closed


@pytest.mark.asyncio
async def test_desktop_session_opens_and_closes_with_async_context_manager():
    def open_mock():
        return True

    # given
    session = DesktopSession(app_key="app_key")
    session._connection.open = open_mock

    # when
    async with session:
        assert session.open_state is OpenState.Opened

    # then
    assert session.open_state is OpenState.Closed
