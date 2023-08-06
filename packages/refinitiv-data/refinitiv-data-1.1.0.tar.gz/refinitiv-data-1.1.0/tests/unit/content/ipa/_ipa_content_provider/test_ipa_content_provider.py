import asyncio

import pytest

from refinitiv.data.content.ipa._ipa_content_provider import (
    IPAContentProviderLayer,
)
from refinitiv.data.errors import RDError
from tests.unit.conftest import (
    StubSession,
    error_request_failed_http_response_generator,
    error_no_location_http_response_generator,
    error_404_http_response_generator,
    success_http_response_generator,
)
from tests.unit.content.conftest import StubDefinition


@pytest.mark.parametrize(
    "async_mode", [False, True], ids=["async_mode=False", "async_mode=True"]
)
def test_ipa_content_provider_layer_get_data(content_type, async_mode):
    # given
    session = StubSession(is_open=True)
    session.async_mode = async_mode
    session.http_responses = success_http_response_generator()

    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # when
    data = provider_layer.get_data(session, async_mode=async_mode)

    # then
    assert data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "async_mode", [False, True], ids=["async_mode=False", "async_mode=True"]
)
async def test_ipa_content_provider_layer_get_data_async(content_type, async_mode):
    # given
    session = StubSession(is_open=True)
    session.async_mode = async_mode
    session.http_responses = success_http_response_generator()
    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # when
    data = await provider_layer.get_data_async(session, async_mode=async_mode)

    # then
    assert data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "async_mode", [False, True], ids=["async_mode=False", "async_mode=True"]
)
async def test_ipa_content_provider_layer_get_data_pass_on_response(
    content_type, async_mode
):
    # given
    fut = asyncio.Future()

    def on_response(response, provider_layer, session):
        fut.set_result(response)

    session = StubSession(is_open=True)
    session.async_mode = async_mode
    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # when
    data = provider_layer.get_data(
        session, on_response=on_response, async_mode=async_mode
    )

    response = await fut

    # then
    assert response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "async_mode", [False, True], ids=["async_mode=False", "async_mode=True"]
)
async def test_ipa_content_provider_layer_call_get_data_async_pass_on_response(
    content_type, async_mode
):
    # given
    fut = asyncio.Future()

    def on_response(response, provider_layer, session):
        fut.set_result(response)

    session = StubSession(is_open=True)
    session.async_mode = async_mode
    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # when
    await provider_layer.get_data_async(
        session, on_response=on_response, async_mode=async_mode
    )

    response = await fut

    # then
    assert response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "async_mode", [False, True], ids=["async_mode=False", "async_mode=True"]
)
async def test_ipa_content_provider_layer_call_get_data_and_pass_on_response_session(
    content_type, async_mode
):
    # given
    fut = asyncio.Future()

    def on_response(response, provider_layer, session):
        fut.set_result(response)

    session = StubSession(is_open=True)
    session.async_mode = async_mode
    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # when
    provider_layer.get_data(session, on_response=on_response, async_mode=async_mode)

    response = await fut

    # then
    assert response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "async_mode", [False, True], ids=["async_mode=False", "async_mode=True"]
)
async def test_ipa_content_provider_layer_call_get_data_async_and_pass_on_response_session(
    content_type, async_mode
):
    # given
    fut = asyncio.Future()

    def on_response(response, provider_layer, session):
        fut.set_result(response)

    session = StubSession(is_open=True)
    session.async_mode = async_mode
    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # when
    await provider_layer.get_data_async(
        session, on_response=on_response, async_mode=async_mode
    )

    response = await fut

    # then
    assert response


@pytest.mark.parametrize(
    "async_mode", [False, True], ids=["async_mode=False", "async_mode=True"]
)
def test_ipa_content_provider_layer_call_get_data_and_pass_on_response_session_will_raise_error(
    content_type, async_mode
):
    # given
    def on_response(response, provider_layer, session):
        raise ValueError("exception")

    session = StubSession(is_open=True)
    session.async_mode = async_mode
    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # when
    response = provider_layer.get_data(
        session, on_response=on_response, async_mode=async_mode
    )

    # then
    assert response


@pytest.mark.parametrize(
    "async_mode", [False, True], ids=["async_mode=False", "async_mode=True"]
)
def test_ipa_content_provider_layer_call_get_data_will_raise_error_is_session_closed(
    content_type, async_mode
):
    # given
    session = StubSession(is_open=False)
    session.async_mode = async_mode
    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # then
    with pytest.raises(Exception, match="Session is not opened."):
        # when
        provider_layer.get_data(session, async_mode=async_mode)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "async_mode", [False, True], ids=["async_mode=False", "async_mode=True"]
)
async def test_ipa_content_provider_layer_call_get_data_async_will_raise_error_is_session_closed(
    content_type, async_mode
):
    # given
    session = StubSession(is_open=False)
    session.async_mode = async_mode
    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # then
    with pytest.raises(Exception, match="Session is not opened."):
        # when
        await provider_layer.get_data_async(session, async_mode=async_mode)


def test_ipa_content_provider_layer_get_data_without_202_operation_response(
    content_type,
):
    # given
    session = StubSession(is_open=True)
    session.async_mode = True
    session.http_responses = error_404_http_response_generator()

    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # then
    with pytest.raises(RDError, match="Error code 404 | Not found"):
        # when
        provider_layer.get_data(session, async_mode=True)


def test_ipa_content_provider_layer_get_data_without_location_in_operation_response(
    content_type,
):
    # given
    session = StubSession(is_open=True)
    session.async_mode = True
    session.http_responses = error_no_location_http_response_generator()

    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # then
    with pytest.raises(
        RDError,
        match="Error code None | IPA Asynchronous request operation failed, response doesn't contain location.",
    ):
        # when
        provider_layer.get_data(session, async_mode=True)


def test_ipa_content_provider_layer_get_data_wit_failed_request_response(content_type):
    # given
    session = StubSession(is_open=True)
    session.async_mode = True
    session.http_responses = error_request_failed_http_response_generator()

    provider_layer = IPAContentProviderLayer(
        content_type, definition=StubDefinition(), universe=StubDefinition()
    )

    # then
    with pytest.raises(RDError, match="Error code 400"):
        # when
        provider_layer.get_data(session, async_mode=True)
