import asyncio

import pytest

from refinitiv.data.content._content_provider_layer import ContentProviderLayer
from tests.unit.conftest import StubSession
from tests.unit.content.conftest import StubDefinition


def test_content_provider_layer_get_data(content_type):
    # given
    session = StubSession(is_open=True)
    provider_layer = ContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # when
    data = provider_layer.get_data(session)

    # then
    assert data


@pytest.mark.asyncio
async def test_content_provider_layer_get_data_async(content_type):
    # given
    session = StubSession(is_open=True)
    provider_layer = ContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # when
    data = await provider_layer.get_data_async(session)

    # then
    assert data


@pytest.mark.asyncio
async def test_content_provider_layer_get_data_pass_on_response(content_type):
    # given
    fut = asyncio.Future()

    def on_response(response, provider_layer, session):
        fut.set_result(response)

    session = StubSession(is_open=True)
    provider_layer = ContentProviderLayer(
        content_type,
        definition=StubDefinition(),
        universe=StubDefinition(),
    )

    # when
    provider_layer.get_data(session, on_response=on_response)

    response = await fut

    # then
    assert response


@pytest.mark.asyncio
async def test_content_provider_layer_call_get_data_async_pass_on_response(
    content_type,
):
    # given
    fut = asyncio.Future()

    def on_response(response, provider_layer, session):
        fut.set_result(response)

    session = StubSession(is_open=True)
    provider_layer = ContentProviderLayer(
        content_type,
        definition=StubDefinition(),
        universe=StubDefinition(),
    )

    # when
    await provider_layer.get_data_async(session, on_response=on_response)

    response = await fut

    # then
    assert response


def test_content_provider_layer_call_get_data_will_raise_error_is_session_closed(
    content_type,
):
    # given
    session = StubSession(is_open=False)
    provider_layer = ContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # then
    with pytest.raises(Exception, match="Session is not opened."):
        # when
        provider_layer.get_data(session)


@pytest.mark.asyncio
async def test_content_provider_layer_call_get_data_async_will_raise_error_is_session_closed(
    content_type,
):
    # given
    session = StubSession(is_open=False)
    provider_layer = ContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # then
    with pytest.raises(Exception, match="Session is not opened."):
        # when
        await provider_layer.get_data_async(session)
