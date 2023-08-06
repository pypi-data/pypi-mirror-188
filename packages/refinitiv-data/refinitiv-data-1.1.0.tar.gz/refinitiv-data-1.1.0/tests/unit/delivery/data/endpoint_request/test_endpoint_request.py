from refinitiv.data.delivery._data._request import Request

try:
    from unittest.mock import MagicMock, AsyncMock
except ImportError:
    from mock.mock import AsyncMock
    from unittest.mock import MagicMock

import pytest

from refinitiv.data.delivery import endpoint_request
from refinitiv.data.delivery._data._endpoint_data import RequestMethod
from tests.unit.conftest import StubSession, StubResponse


def test_get_data():
    # given
    session = StubSession(is_open=True)
    definition = endpoint_request.Definition(
        url="test_url",
        method="test_method",
        path_parameters={"path_parameters_key": "path_parameters_value"},
        query_parameters={"query_parameters_key": "query_parameters_value"},
        header_parameters={"header_parameters_key": "header_parameters_value"},
        body_parameters={"body_parameters_key": "body_parameters_value"},
    )

    # when
    response = definition.get_data(session)

    # then
    assert response is not None


def test_get_data_multiple_body_parameters():
    # given
    session = StubSession(is_open=True)
    definition = endpoint_request.Definition(
        url="test_url",
        method="test_method",
        path_parameters={"path_parameters_key": "path_parameters_value"},
        query_parameters={"query_parameters_key": "query_parameters_value"},
        header_parameters={"header_parameters_key": "header_parameters_value"},
        body_parameters=[
            {"header_parameters_key": "header_parameters_value"},
            {"another_header_parameters_key": "another_header_parameters_value"},
        ],
    )

    # when
    response = definition.get_data(session)

    # then
    assert response is not None


def test_get_data_raise_error_if_no_session_passed_and_no_default_session():
    # given
    definition = endpoint_request.Definition(url="test_url")

    # then
    with pytest.raises(AttributeError) as error:
        # when
        definition.get_data()
    assert (
        error.value.args[0]
        == "No default session created yet. Please create a session first!"
    )


def test_get_data_simple():
    # given
    session = StubSession(is_open=True)
    definition = endpoint_request.Definition(url="test_url")

    # when
    response = definition.get_data(session)

    # then
    assert response is not None


@pytest.mark.asyncio
async def test_get_data_async():
    # given
    session = StubSession(is_open=True)
    definition = endpoint_request.Definition(url="test_url")

    # when
    response = await definition.get_data_async(session)

    # then
    assert response is not None


@pytest.mark.asyncio
async def test_get_data_async_raise_error_if_no_session_passed():
    # given
    definition = endpoint_request.Definition(url="test_url")

    # then
    with pytest.raises(AttributeError):
        # when
        await definition.get_data_async()


def test_get_data_raise_error_if_path_params_not_provided():
    definition = endpoint_request.Definition(
        url="/data/historical-pricing/v1/views/events/{universe}"
    )

    with pytest.raises(
        ValueError,
        match="Path parameter 'universe' is missing, please provide path parameter",
    ):
        definition.get_data()


def test_get_data_raise_error_if_url_empty():
    definition = endpoint_request.Definition(url="")

    with pytest.raises(
        ValueError, match="Requested URL is missing, please provide valid URL"
    ):
        definition.get_data()


@pytest.mark.parametrize(
    "property",
    [
        "url",
        "method",
        "path_parameters",
        "query_parameters",
        "header_parameters",
        "body_parameters",
    ],
)
def test_definition_has_properties(property):
    definition = endpoint_request.Definition("")

    assert hasattr(definition, property)


def test_changed_url_is_passing_to_get_data():
    # given
    expected_value = "expected_url"

    session = StubSession(is_open=True)
    definition = endpoint_request.Definition(url="url")
    definition._provider = MagicMock()

    # when
    definition.url = expected_value

    # then
    definition.get_data(session)
    definition._provider.get_data.assert_called_once_with(
        session,
        expected_value,
        method=None,
        path_parameters=None,
        query_parameters=None,
        header_parameters=None,
        body_parameters=None,
    )


def test_changed_method_is_passing_to_get_data():
    # given
    expected_value = RequestMethod.POST

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, method=RequestMethod.GET)
    definition._provider = MagicMock()

    # when
    definition.method = expected_value

    # then
    definition.get_data(session)
    definition._provider.get_data.assert_called_once_with(
        session,
        url,
        method=expected_value,
        path_parameters=None,
        query_parameters=None,
        header_parameters=None,
        body_parameters=None,
    )


def test_changed_path_parameters_is_passing_to_get_data():
    # given
    expected_value = {"path_parameters_key": "path_parameters_value"}

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, path_parameters={})
    definition._provider = MagicMock()

    # when
    definition.path_parameters = expected_value

    # then
    definition.get_data(session)
    definition._provider.get_data.assert_called_once_with(
        session,
        url,
        method=None,
        path_parameters=expected_value,
        query_parameters=None,
        header_parameters=None,
        body_parameters=None,
    )


def test_changed_query_parameters_is_passing_to_get_data():
    # given
    expected_value = {"query_parameters_key": "query_parameters_value"}

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, query_parameters={})
    definition._provider = MagicMock()

    # when
    definition.query_parameters = expected_value

    # then
    definition.get_data(session)
    definition._provider.get_data.assert_called_once_with(
        session,
        url,
        method=None,
        path_parameters=None,
        query_parameters=expected_value,
        header_parameters=None,
        body_parameters=None,
    )


def test_changed_header_parameters_is_passing_to_get_data():
    # given
    expected_value = {"header_parameters_key": "header_parameters_value"}

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, header_parameters={})
    definition._provider = MagicMock()

    # when
    definition.header_parameters = expected_value

    # then
    definition.get_data(session)
    definition._provider.get_data.assert_called_once_with(
        session,
        url,
        method=None,
        path_parameters=None,
        query_parameters=None,
        header_parameters=expected_value,
        body_parameters=None,
    )


def test_changed_body_parameters_is_passing_to_get_data():
    # given
    expected_value = {"body_parameters_key": "body_parameters_value"}

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, body_parameters={})
    definition._provider = MagicMock()

    # when
    definition.body_parameters = expected_value

    # then
    definition.get_data(session)
    definition._provider.get_data.assert_called_once_with(
        session,
        url,
        method=None,
        path_parameters=None,
        query_parameters=None,
        header_parameters=None,
        body_parameters=expected_value,
    )


def test_error_is_a_string():
    # given
    expected_value = "BAD_REQUEST"
    response = StubResponse(
        {
            "requestId": "f4a1eae6-de2b-4946-8f59-00185a217145",
            "timestamp": "2022-05-19T08:53:43.631Z",
            "status": 400,
            "message": "Missing required parameter: type",
            "error": expected_value,
        },
        status_code=400,
    )
    session = StubSession(is_open=True, response=response)
    definition = endpoint_request.Definition(
        method=RequestMethod.POST,
        url="https://api.refinitiv.com/discovery/symbology/v1/lookup",
    )

    # when
    try:
        response = definition.get_data(session)
    except Exception as e:
        assert False, str(e)
    else:
        # then
        error = response.errors[0]
        assert error.message == expected_value


@pytest.mark.asyncio
async def test_changed_url_is_passing_to_get_data_async():
    # given
    expected_value = "expected_url"

    session = StubSession(is_open=True)
    definition = endpoint_request.Definition(url="url")
    definition._provider = AsyncMock()

    # when
    definition.url = expected_value

    # then
    await definition.get_data_async(session)
    definition._provider.get_data_async.assert_called_once_with(
        session,
        expected_value,
        method=None,
        path_parameters=None,
        query_parameters=None,
        header_parameters=None,
        body_parameters=None,
    )


@pytest.mark.asyncio
async def test_changed_method_is_passing_to_get_data_async():
    # given
    expected_value = RequestMethod.POST

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, method=RequestMethod.GET)
    definition._provider = AsyncMock()

    # when
    definition.method = expected_value

    # then
    await definition.get_data_async(session)
    definition._provider.get_data_async.assert_called_once_with(
        session,
        url,
        method=expected_value,
        path_parameters=None,
        query_parameters=None,
        header_parameters=None,
        body_parameters=None,
    )


@pytest.mark.asyncio
async def test_changed_path_parameters_is_passing_to_get_data_async():
    # given
    expected_value = {"path_parameters_key": "path_parameters_value"}

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, path_parameters={})
    definition._provider = AsyncMock()

    # when
    definition.path_parameters = expected_value

    # then
    await definition.get_data_async(session)
    definition._provider.get_data_async.assert_called_once_with(
        session,
        url,
        method=None,
        path_parameters=expected_value,
        query_parameters=None,
        header_parameters=None,
        body_parameters=None,
    )


@pytest.mark.asyncio
async def test_changed_query_parameters_is_passing_to_get_data_async():
    # given
    expected_value = {"query_parameters_key": "query_parameters_value"}

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, query_parameters={})
    definition._provider = AsyncMock()

    # when
    definition.query_parameters = expected_value

    # then
    await definition.get_data_async(session)
    definition._provider.get_data_async.assert_called_once_with(
        session,
        url,
        method=None,
        path_parameters=None,
        query_parameters=expected_value,
        header_parameters=None,
        body_parameters=None,
    )


@pytest.mark.asyncio
async def test_changed_header_parameters_is_passing_to_get_data_async():
    # given
    expected_value = {"header_parameters_key": "header_parameters_value"}

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, header_parameters={})
    definition._provider = AsyncMock()

    # when
    definition.header_parameters = expected_value

    # then
    await definition.get_data_async(session)
    definition._provider.get_data_async.assert_called_once_with(
        session,
        url,
        method=None,
        path_parameters=None,
        query_parameters=None,
        header_parameters=expected_value,
        body_parameters=None,
    )


@pytest.mark.asyncio
async def test_changed_body_parameters_is_passing_to_get_data_async():
    # given
    expected_value = {"body_parameters_key": "body_parameters_value"}

    session = StubSession(is_open=True)
    url = "url"
    definition = endpoint_request.Definition(url=url, body_parameters={})
    definition._provider = AsyncMock()

    # when
    definition.body_parameters = expected_value

    # then
    await definition.get_data_async(session)
    definition._provider.get_data_async.assert_called_once_with(
        session,
        url,
        method=None,
        path_parameters=None,
        query_parameters=None,
        header_parameters=None,
        body_parameters=expected_value,
    )


@pytest.mark.parametrize(
    "input_method, expected_method",
    [
        (RequestMethod.GET, "GET"),
        (RequestMethod.POST, "POST"),
        (RequestMethod.DELETE, "DELETE"),
        (RequestMethod.PUT, "PUT"),
        ("GET", "GET"),
        ("POST", "POST"),
        ("DELETE", "DELETE"),
        ("PUT", "PUT"),
        ("ANY_METHOD__", "ANY_METHOD__"),
    ],
)
def test_endpoint_request_definition_method_argument(input_method, expected_method):
    def assert_method(session):
        def inner(request: Request):
            # then
            assert request.method == expected_method
            return StubResponse()

        session.http_request = inner

    # given
    session = StubSession(is_open=True)
    definition = endpoint_request.Definition(
        url="test_url",
        method=input_method,
    )

    # when
    assert_method(session)
    definition.get_data(session)
