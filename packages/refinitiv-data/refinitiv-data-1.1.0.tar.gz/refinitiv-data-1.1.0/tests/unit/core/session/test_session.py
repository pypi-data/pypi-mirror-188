import logging
from threading import Thread
from unittest.mock import MagicMock, patch
import refinitiv.data as rd
import pytest

from refinitiv.data import _configure
from refinitiv.data._core.session import (
    RDDefaultSessionManager,
    EikonDefaultSessionManager,
    _rd_default_session_manager,
    _eikon_default_session_manager,
    DesktopSession,
    Session,
    PlatformSession,
)


def test_rd_default_session_manager_try_get_default_session_error():
    # given
    manager = RDDefaultSessionManager()

    with pytest.raises(
        AttributeError,
        match="No default session created yet. Please create a session first!",
    ):
        manager.try_get_default_session()


def test_rd_default_session_manager_try_get_default_session():
    # given
    mock_session = MagicMock()
    manager = RDDefaultSessionManager(mock_session)

    result = manager.try_get_default_session()

    assert result == mock_session


def test_rd_default_session_manager_set_default_session_error():
    manager = RDDefaultSessionManager()

    with pytest.raises(TypeError, match="Invalid argument"):
        manager.set_default_session("invalid-type")


def test_rd_default_session_manager_close_default_session():
    mock_session = MagicMock()
    manager = RDDefaultSessionManager(mock_session)

    manager.close_default_session()

    mock_session.close.assert_called_once()


def test_rd_default_session_manager_clear_default_session():
    mock_session = MagicMock()
    manager = RDDefaultSessionManager(mock_session)

    manager.set_default_session(None)

    assert manager.has_session() is False


def test_rd_default_session_manager_set_default_session_set_session():
    manager = RDDefaultSessionManager()

    manager.set_default_session(DesktopSession(""))

    assert manager.has_session() is True


def test_eikon_default_session_manager_get_default_session():
    manager = EikonDefaultSessionManager()

    default_session = manager.get_default_session()

    assert default_session is None


def test_eikon_default_session_manager_get_default_session_set_session():
    manager = EikonDefaultSessionManager()

    default_session = manager.get_default_session("mocked-app-key")

    assert default_session is not None


def test_eikon_default_session_manager_set_default_session_set_session():
    manager = EikonDefaultSessionManager()

    manager.set_default_session(DesktopSession(""))

    assert manager.has_session() is True


@patch("refinitiv.data._core.session.DesktopSession")
def test_eikon_default_session_manager_get_session_with_app_key(mock_desktop_session):
    mock_session = MagicMock()
    manager = EikonDefaultSessionManager(mock_session)

    default_session = manager.get_default_session("mocked-app-key")

    assert default_session is not None


def test_eikon_default_session_manager_close_default_session():
    mock_session = MagicMock()
    manager = EikonDefaultSessionManager(mock_session)

    manager.close_default_session()

    mock_session.close.assert_called_once()


def test_eikon_default_session_manager_clear_default_session():
    mock_session = MagicMock()
    manager = EikonDefaultSessionManager(mock_session)

    manager.clear_default_session()

    assert manager.has_session() is False


def test_if_rd_manager_clear_session_in_eikon_manager_session_is_empty():
    _rd_default_session_manager.set_default_session(DesktopSession(""))

    _rd_default_session_manager.set_default_session(None)

    assert _eikon_default_session_manager.has_session() is False


def test_if_eikon_manager_clear_session_in_rd_manager_session_is_empty():
    _eikon_default_session_manager.set_default_session(DesktopSession(""))

    _eikon_default_session_manager.clear_default_session()

    assert _rd_default_session_manager.has_session() is False


def test_get_log_level_return_default_config_value_if_not_set(session):
    # given
    expected_level = _configure.defaults.log_level

    # when
    testing_level = session.get_log_level()

    # then
    assert testing_level == expected_level


def test_get_log_level_return_int_value(session):
    # when
    testing_level = session.get_log_level()

    # then
    assert isinstance(testing_level, int)


def test_get_log_level_returns_same_that_pass_in_set_log_level(session):
    # given
    expected_level = 1

    # when
    session.set_log_level(expected_level)
    testing_level = session.get_log_level()

    # then
    assert testing_level == expected_level


def test_set_log_level_return_none(session):
    # given
    input_level = 1

    # when
    testing_value = session.set_log_level(input_level)

    # then
    assert testing_value is None


@pytest.mark.parametrize(
    "input_level,expected_level",
    [
        [logging.DEBUG, logging.DEBUG],
        [logging.INFO, logging.INFO],
        [logging.WARNING, logging.WARNING],
        [logging.ERROR, logging.ERROR],
        [logging.FATAL, logging.FATAL],
        [logging.CRITICAL, logging.CRITICAL],
    ],
)
def test_set_logging_levels_as_int_and_get_same_int_levels(
    input_level, expected_level, session
):
    # given
    session.set_log_level(input_level)

    # when
    testing_level = session.get_log_level()

    # then
    assert testing_level == expected_level and isinstance(testing_level, int)


@pytest.mark.parametrize(
    "input_level,expected_level",
    [
        ("DEBUG", 10),
        ("INFO", 20),
        ("WARNING", 30),
        ("ERROR", 40),
        ("FATAL", 50),
        ("CRITICAL", 50),
    ],
)
def test_set_logging_levels_as_string_and_get_same_int_levels(
    input_level, expected_level, session
):
    # given
    session.set_log_level(input_level)

    # when
    testing_level = session.get_log_level()

    # then
    assert testing_level == expected_level and isinstance(testing_level, int)


@pytest.mark.parametrize(
    "session",
    [
        PlatformSession(
            app_key="app_key", deployed_platform_host="deployed_platform_host"
        ),
        DesktopSession(app_key="app_key"),
    ],
    ids=["PlatformSession", "DesktopSession"],
)
def test_session_has_pending_state(session):
    def check_state():
        nonlocal testing_state
        testing_state = session.open_state

    def open():
        while not stop:
            pass

    # given
    testing_state = None
    expected_state = rd.OpenState.Pending
    stop = False
    session._connection.open = open

    # when
    Thread(target=session.open, daemon=True).start()
    Thread(target=check_state, daemon=True).start()

    # then
    stop = True
    assert testing_state == expected_state, testing_state
