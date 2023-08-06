from unittest.mock import MagicMock

from refinitiv.data.session import desktop
from tests.unit.conftest import remove_dunder_methods


def test_desktop_session_scope():
    expected_attributes = [
        "Definition",
    ]
    testing_attributes = dir(desktop)
    testing_attributes = remove_dunder_methods(testing_attributes)
    assert expected_attributes == testing_attributes


def test_definition_keyword_arguments():
    app_key_mock = MagicMock(name="MOCK-app_key")

    definition = desktop.Definition(
        app_key=app_key_mock,
    )
    session = definition.get_session()
    assert session.app_key == app_key_mock


def test_definition_positional_arguments():
    session_name = "workspace"
    app_key_mock = MagicMock(name="MOCK-app_key")

    definition = desktop.Definition(
        session_name,
        app_key_mock,
    )
    session = definition.get_session()
    assert session.name == session_name
    assert session.app_key == app_key_mock


def test_definition_mix_of_positional_and_named_arguments():
    session_name = "workspace"
    app_key_mock = MagicMock(name="MOCK-app_key")

    definition = desktop.Definition(
        session_name,
        app_key_mock,
    )
    session = definition.get_session()
    assert session.name == session_name
    assert session.app_key == app_key_mock


def test_default_workspace_app_key_not_raise_error_if_exists(write_project_config):
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
        definition = desktop.Definition()
        definition.get_session()
    except Exception as e:
        assert False, str(e)
    else:
        assert True
