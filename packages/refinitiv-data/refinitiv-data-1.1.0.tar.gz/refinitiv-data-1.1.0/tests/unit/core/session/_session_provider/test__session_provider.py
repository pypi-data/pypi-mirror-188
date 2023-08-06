import pytest
from mock import Mock

from refinitiv.data._core.session._session_provider import make_session_provider


def test_make_session_provider_returns_provider(session_type):
    # when
    provider = make_session_provider(session_type)

    # then
    assert provider is not None


def test_make_session_provider_raise_error_if_invalid_session_type():
    # then
    with pytest.raises(ValueError):
        # when
        make_session_provider("invalid-session-type")


def test_session_provider_create_class_by_params(session_type):
    # given
    grant = Mock()
    config = {"app-key": "test_app_key"}
    # when
    create_session = make_session_provider(session_type, config, grant)
    session = create_session()

    # then
    assert session is not None


def test_session_provider_create_class_by_params_and_kwargs(session_type):
    # given
    grant = Mock()
    config = {"app-key": "test_app_key"}
    # when
    create_session = make_session_provider(session_type, config, grant)
    session = create_session()

    # then
    assert session is not None
