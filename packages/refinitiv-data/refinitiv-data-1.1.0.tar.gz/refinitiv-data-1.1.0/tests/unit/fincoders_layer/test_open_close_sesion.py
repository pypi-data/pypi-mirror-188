from unittest.mock import MagicMock, call

import pytest

import refinitiv.data as rd
from refinitiv.data import OpenState
from refinitiv.data._fin_coder_layer.session import (
    _open_session,
    set_default,
)


@pytest.fixture
def tools():
    def_obj_mock = MagicMock()
    def_obj_mock.get_session.return_value = MagicMock(spec=rd.session.Session)

    tools = {
        "_definition": MagicMock(return_value=def_obj_mock),
        "_load_config": MagicMock(),
        "_config_object": MagicMock(),
        "_set_default": set_default,
    }

    return tools


def test_private_open_with_defaults(tools):
    _name = "default"
    tools["_config_object"].get_param.return_value = _name

    session = _open_session(config_path=None, app_key=None, config_name=None, **tools)
    default_session = rd.session.get_default()

    tools["_definition"].assert_called_once_with(name=_name)
    assert session is default_session


def test_private_open_with_name(tools):
    _name = "MY"

    session = _open_session(config_path=_name, app_key=None, config_name=None, **tools)
    default_session = rd.session.get_default()

    tools["_definition"].assert_called_once_with(name=_name)
    assert session is default_session


def test_private_open_with_app_key(tools):
    app_key = "fooo"
    _name = "MY"

    tools["_config_object"].get_param.return_value = _name

    session = _open_session(
        config_path=None, app_key=app_key, config_name=None, **tools
    )
    default_session = rd.session.get_default()

    tools["_config_object"].get_param.assert_has_calls(
        [call("sessions.default"), call(f"sessions.{_name}")]
    )
    tools["_config_object"].set_param.assert_called_once_with(
        param=f"sessions.{_name}.app-key", value=app_key
    )
    assert session is default_session


def test_private_open_with_name_and_app_key(tools):
    app_key = "fooo2"
    _name = "MY.s"

    session = _open_session(
        config_path=_name, app_key=app_key, config_name=None, **tools
    )
    default_session = rd.session.get_default()

    tools["_config_object"].set_param.assert_called_once_with(
        param=f"sessions.{_name}.app-key", value=app_key
    )
    assert session is default_session


def test_private_open_with_config(tools):
    config_name = "foo"

    session = _open_session(
        config_path=None, app_key=None, config_name=config_name, **tools
    )
    default_session = rd.session.get_default()

    tools["_load_config"].assert_called_once_with(config_name)
    assert session is default_session


def test_close_session(tools):
    session = _open_session(config_path=None, app_key=None, config_name=None, **tools)

    session.info = MagicMock()
    session.open_state = OpenState.Opened
    rd.close_session()

    session.close.assert_called_once()


def test_bad_session_name(tools):
    tools["_config_object"] = rd.get_config()

    with pytest.raises(NameError):
        _open_session(
            config_path="desktop.invalid_session_name",
            app_key="somekey",
            config_name=None,
            **tools,
        )
