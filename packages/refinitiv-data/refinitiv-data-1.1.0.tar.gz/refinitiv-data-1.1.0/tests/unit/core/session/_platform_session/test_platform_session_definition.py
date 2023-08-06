import pytest
from mock import MagicMock
from refinitiv.data.session import platform
from refinitiv.data._core.session import GrantPassword


def test_definition_keyword_arguments():
    app_key_mock = MagicMock(name="MOCK-app_key")
    grant_mock = GrantPassword(
        MagicMock(name="MOCK-username"), MagicMock(name="MOCK-password")
    )
    signon_control_mock = MagicMock(name="MOCK-signon_control")
    deployed_platform_host_mock = MagicMock(name="MOCK-deployed_platform_host")
    deployed_platform_username_mock = MagicMock(name="MOCK-deployed_platform_username")
    dacs_position_mock = MagicMock(name="MOCK-dacs_position")
    dacs_application_id_mock = MagicMock(name="MOCK-dacs_application_id")

    definition = platform.Definition(
        grant=grant_mock,
        app_key=app_key_mock,
        signon_control=signon_control_mock,
        deployed_platform_host=deployed_platform_host_mock,
        deployed_platform_username=deployed_platform_username_mock,
        dacs_position=dacs_position_mock,
        dacs_application_id=dacs_application_id_mock,
    )
    session = definition.get_session()

    assert session.app_key == app_key_mock
    assert session._grant is grant_mock
    assert session._grant.get_username() == grant_mock.get_username()
    assert session._grant.get_password() == grant_mock.get_password()
    assert session._take_signon_control == signon_control_mock
    assert session._deployed_platform_host == deployed_platform_host_mock

    assert session.name == "default"
    assert (
        session._dacs_params.deployed_platform_username
        == deployed_platform_username_mock
    )
    assert session._dacs_params.dacs_position == dacs_position_mock
    assert session._dacs_params.dacs_application_id == dacs_application_id_mock


def test_definition_positional_arguments():
    session_name = "default"
    app_key_mock = MagicMock(name="MOCK-app_key")
    grant_mock = GrantPassword(
        MagicMock(name="MOCK-username"), MagicMock(name="MOCK-password")
    )
    signon_control_mock = MagicMock(name="MOCK-signon_control")
    deployed_platform_host_mock = MagicMock(name="MOCK-deployed_platform_host")
    authentication_token_mock = MagicMock(name="MOCK-authentication_token")
    deployed_platform_username_mock = MagicMock(name="MOCK-deployed_platform_username")
    dacs_position_mock = MagicMock(name="MOCK-dacs_position")
    dacs_application_id_mock = MagicMock(name="MOCK-dacs_application_id")

    definition = platform.Definition(
        session_name,
        app_key_mock,
        grant_mock,
        signon_control_mock,
        deployed_platform_host_mock,
        deployed_platform_username_mock,
        dacs_position_mock,
        dacs_application_id_mock,
    )
    session = definition.get_session()

    assert session.name == session_name
    assert session.app_key == app_key_mock
    assert session._grant is grant_mock
    assert session._grant.get_username() == grant_mock.get_username()
    assert session._grant.get_password() == grant_mock.get_password()
    assert session._take_signon_control == signon_control_mock
    assert session._deployed_platform_host == deployed_platform_host_mock
    assert session.name == "default"
    assert not authentication_token_mock.called
    assert (
        session._dacs_params.deployed_platform_username
        == deployed_platform_username_mock
    )
    assert session._dacs_params.dacs_position == dacs_position_mock
    assert session._dacs_params.dacs_application_id == dacs_application_id_mock


def test_definition_mix_of_positional_and_named_arguments():
    session_name = "default"
    app_key_mock = MagicMock(name="MOCK-app_key")
    grant_mock = GrantPassword(
        MagicMock(name="MOCK-username"), MagicMock(name="MOCK-password")
    )
    signon_control_mock = MagicMock(name="MOCK-signon_control")
    deployed_platform_host_mock = MagicMock(name="MOCK-deployed_platform_host")
    authentication_token_mock = MagicMock(name="MOCK-authentication_token")
    deployed_platform_username_mock = MagicMock(name="MOCK-deployed_platform_username")
    dacs_position_mock = MagicMock(name="MOCK-dacs_position")
    dacs_application_id_mock = MagicMock(name="MOCK-dacs_application_id")

    definition = platform.Definition(
        session_name,
        app_key_mock,
        grant_mock,
        signon_control_mock,
        deployed_platform_host=deployed_platform_host_mock,
        deployed_platform_username=deployed_platform_username_mock,
        dacs_position=dacs_position_mock,
        dacs_application_id=dacs_application_id_mock,
    )
    session = definition.get_session()

    assert session.app_key == app_key_mock
    assert session._grant is grant_mock
    assert session._grant.get_username() == grant_mock.get_username()
    assert session._grant.get_password() == grant_mock.get_password()
    assert session._take_signon_control == signon_control_mock
    assert session._deployed_platform_host == deployed_platform_host_mock
    assert session.name == "default"
    assert not authentication_token_mock.called
    assert (
        session._dacs_params.deployed_platform_username
        == deployed_platform_username_mock
    )
    assert session._dacs_params.dacs_position == dacs_position_mock
    assert session._dacs_params.dacs_application_id == dacs_application_id_mock


def test_deployed_platform_session():
    session_name = "default"
    app_key_mock = "MOCK-app_key"
    deployed_platform_host_mock = "MOCK-deployed_platform_host"
    deployed_platform_username_mock = "MOCK-deployed_platform_username"

    definition = platform.Definition(
        session_name,
        app_key_mock,
        deployed_platform_host=deployed_platform_host_mock,
        deployed_platform_username=deployed_platform_username_mock,
    )
    session = definition.get_session()
    assert session.app_key == app_key_mock
    assert session._deployed_platform_host == deployed_platform_host_mock
    assert session.name == "default"
    assert (
        session._dacs_params.deployed_platform_username
        == deployed_platform_username_mock
    )


def test_deployed_platform_session_with_missing_argument():
    session_name = "default"
    app_key_mock = MagicMock(name="MOCK-app_key")
    deployed_platform_host_mock = MagicMock(name="MOCK-deployed_platform_host")
    msg = (
        "To create platform session, please provide 'grant' attribute to the "
        "definition or set 'username' and 'password' in the config file. "
        "To create deployed session, please provide 'deployed_platform_host' "
        "and 'deployed_platform_username' to the definition or the config file."
    )

    with pytest.raises(
        AttributeError,
        match=msg,
    ):
        definition = platform.Definition(
            session_name,
            app_key_mock,
            deployed_platform_host=deployed_platform_host_mock,
        )
        definition.get_session()


def test_app_key_raise_error_if_empty_string():
    with pytest.raises(Exception) as error:
        platform.Definition(app_key="")

    assert "Can't find 'app-key' in config object." in str(error.value)


def test_app_key_raise_error_if_none():
    msg = (
        "Please, set app-key in [session.platform.default] section of "
        "the config file or provide 'app-key' attribute to the definition."
    )
    with pytest.raises(Exception) as error:
        platform.Definition(app_key=None)

    assert msg in str(error.value)


def test_signon_control_default_value():
    grant_mock = GrantPassword(
        MagicMock(name="MOCK-username"), MagicMock(name="MOCK-password")
    )

    # when
    session = platform.Definition(app_key="app_key", grant=grant_mock).get_session()

    # then
    assert session._take_signon_control is True


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        (True, True),
        (False, False),
    ],
)
def test_signon_control(input_value, expected_value):
    grant_mock = GrantPassword(
        MagicMock(name="MOCK-username"), MagicMock(name="MOCK-password")
    )

    # when
    session = platform.Definition(
        app_key="app_key", grant=grant_mock, signon_control=input_value
    ).get_session()

    # then
    assert session._take_signon_control is expected_value
