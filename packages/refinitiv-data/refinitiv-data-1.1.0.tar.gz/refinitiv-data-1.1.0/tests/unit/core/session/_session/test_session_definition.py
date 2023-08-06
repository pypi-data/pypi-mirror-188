import pytest

import refinitiv.data as rd
from refinitiv.data import get_config
from refinitiv.data._core.session import GrantPassword


def test_session_definition_session_name():
    config = get_config()
    config.set_param("sessions.desktop.workspace.app-key", "mocked-app-key")

    definition = rd.session.Definition(name="desktop.workspace")
    session = definition.get_session()

    assert session.name == "workspace"


def test_desktop_session_definition_scope():
    expected_attributes = "get_session"
    config = get_config()
    config.set_param("sessions.desktop.workspace.app-key", "mocked-app-key")

    definition = rd.session.Definition(name="desktop.workspace")

    assert expected_attributes in dir(definition)


def test_definition_from_config(write_project_config):
    from refinitiv.data import _configure as configure

    configure.reload()

    app_key_mock = "MOCK-app_key"
    grant_mock = GrantPassword("MOCK-username", "MOCK-password")
    signon_control_mock = "MOCK-signon_control"
    deployed_platform_host_mock = "MOCK-deployed_platform_host"
    deployed_platform_username_mock = "MOCK-deployed_platform_username"
    dacs_position_mock = "MOCK-dacs_position"
    dacs_application_id_mock = "MOCK-dacs_application_id"

    d = {
        "sessions": {
            "platform": {
                "custom-session": {
                    "app-key": app_key_mock,
                    "username": grant_mock.get_username(),
                    "password": grant_mock.get_password(),
                    "signon_control": signon_control_mock,
                    "realtime-distribution-system": {
                        "url": deployed_platform_host_mock,
                        "dacs": {
                            "username": deployed_platform_username_mock,
                            "application-id": dacs_application_id_mock,
                            "position": dacs_position_mock,
                        },
                    },
                }
            }
        },
    }
    write_project_config(d)
    configure.reload()
    definition = rd.session.Definition("platform.custom-session")
    session = definition.get_session()
    assert session.app_key == app_key_mock
    assert session._grant is not grant_mock
    assert session._grant.get_username() == grant_mock.get_username()
    assert session._grant.get_password() == grant_mock.get_password()
    assert session._take_signon_control == signon_control_mock
    assert session._deployed_platform_host == deployed_platform_host_mock

    assert session.name == "custom-session"
    assert (
        session._dacs_params.deployed_platform_username
        == deployed_platform_username_mock
    )
    assert session._dacs_params.dacs_position == dacs_position_mock
    assert session._dacs_params.dacs_application_id == dacs_application_id_mock


def test_definition_from_config_without_error_for_desktop_session(write_project_config):
    from refinitiv.data import _configure as configure

    configure.reload()

    config = {
        "sessions": {
            "default": "desktop.custom-session",
            "desktop": {
                "custom-session": {
                    "app-key": "DEFAULT_WORKSPACE_APP_KEY",
                }
            },
        },
    }
    write_project_config(config)
    configure.reload()
    try:
        definition = rd.session.Definition()
        definition.get_session()
    except Exception as e:
        assert False, str(e)
    else:
        assert True


def test_definition_from_config_error_invalid_session_type(write_project_config):
    from refinitiv.data import _configure as configure

    configure.reload()

    config = {
        "sessions": {
            "default": "desktop.custom-session",
            "desktop": {
                "custom-session": {
                    "app-key": "DEFAULT_WORKSPACE_APP_KEY",
                }
            },
        },
    }
    write_project_config(config)
    configure.reload()
    with pytest.raises(
        Exception, match="Cannot get session type by value:invalid-type"
    ):
        definition = rd.session.Definition("invalid-type.default")
        definition.get_session()


def test_definition_from_config_specific_apis(write_project_config):
    from refinitiv.data import _configure as configure

    configure.reload()

    app_key_mock = "MOCK-app_key"
    grant_mock = GrantPassword("MOCK-username", "MOCK-password")
    signon_control_mock = "MOCK-signon_control"

    d = {
        "sessions": {
            "platform": {
                "custom-session": {
                    "app-key": app_key_mock,
                    "username": grant_mock.get_username(),
                    "password": grant_mock.get_password(),
                    "signon_control": signon_control_mock,
                    "apis": {"test_key": "test_value"},
                }
            }
        },
    }
    write_project_config(d)
    configure.reload()
    definition = rd.session.Definition("platform.custom-session")
    session = definition.get_session()

    assert session.name == "custom-session"
    test_value = session.config.get("apis.test_key")
    assert test_value == "test_value"
