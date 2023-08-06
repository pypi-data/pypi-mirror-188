from types import SimpleNamespace

import pytest
from mock import MagicMock

from refinitiv.data import _configure as configure
from refinitiv.data.content._content_provider_layer import ContentProviderLayer
from refinitiv.data._content_type import ContentType
from refinitiv.data._core.session import _rd_default_session_manager
from refinitiv.data._core.session._default_session_manager import (
    Wrapper,
    get_valid_session,
)
from refinitiv.data.delivery._data._data_provider_factory import (
    make_provider,
    get_url,
)
from tests.unit.conftest import StubSession
from tests.unit.content.conftest import StubDefinition


def test_get_url():
    config = configure.get_config()

    url = get_url(ContentType.FORWARD_CURVE, config)
    assert url


def test_get_url_raise():
    config = configure.get_config()
    with pytest.raises(AttributeError):
        get_url(None, config)


def test_make_provider():
    provider = make_provider(ContentType.FORWARD_CURVE)
    assert provider


def test_make_provider_raise():
    with pytest.raises(Exception):
        make_provider(MagicMock())


def test_provider_get_data():
    session = StubSession(is_open=True)
    provider = make_provider(ContentType.FORWARD_CURVE)
    data = provider.get_data(
        session,
        "test_url",
        universe=[MagicMock()],
        __content_type__=ContentType.FORWARD_CURVE,
    )
    assert data


@pytest.mark.asyncio
async def test_provider_get_data_async():
    session = StubSession(is_open=True)
    provider = make_provider(ContentType.FORWARD_CURVE)

    data = await provider.get_data_async(
        session,
        "test_url",
        universe=[MagicMock()],
        universe_class=MagicMock,
        __content_type__=ContentType.FORWARD_CURVE,
    )
    assert data


def test_get_valid_session_has_session_and_has_default():
    session = StubSession()
    default_session = StubSession()
    _rd_default_session_manager.set_session(default_session)

    validated_session = get_valid_session(session)

    assert validated_session == session and validated_session != default_session


def test_get_valid_session_has_session_and_hasnot_default():
    session = StubSession()
    _rd_default_session_manager.set_session(None)

    validated_session = get_valid_session(session)

    assert validated_session == session


def test_get_valid_session_hasnot_session_and_has_default():
    default_session = SimpleNamespace()
    _rd_default_session_manager.set_session(default_session)

    validated_session = get_valid_session(None)

    assert validated_session == default_session

    _rd_default_session_manager.set_session(None)


def test_get_valid_session_hasnot_session_and_hasnot_default():
    _rd_default_session_manager.set_session(None)

    with pytest.raises(AttributeError):
        get_valid_session(None)


def test_content_provider_get_data():
    session = StubSession(is_open=True)
    try:
        provider = ContentProviderLayer(
            ContentType.FORWARD_CURVE, universe=StubDefinition()
        )
        provider.get_data(session, lambda response, inst, session: inst)
    except Exception as e:
        assert False, e


@pytest.mark.asyncio
async def test_content_provider_get_data_async():
    session = StubSession(is_open=True)
    try:
        provider = ContentProviderLayer(
            ContentType.FORWARD_CURVE, universe=StubDefinition()
        )
        await provider.get_data_async(session)
    except Exception as e:
        assert False, e
