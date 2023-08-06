from unittest.mock import Mock, patch

import pytest

from refinitiv.data.delivery._data._data_factory import DataFactory
from refinitiv.data.delivery._data._data_provider import (
    Response,
    RequestFactory,
    ParsedData,
)
from refinitiv.data.delivery._data._endpoint_data import RequestMethod
from tests.unit.conftest import StubSession, args


@pytest.mark.parametrize(
    "arg",
    [
        "data",
        "is_success",
        "errors",
        "requests_count",
        "request_message",
        "closure",
        "http_status",
        "http_headers",
    ],
)
def test_response_args(arg):
    # given
    # when
    response = Response(True, ParsedData({}, {}), DataFactory())

    # then
    assert hasattr(response, arg)


def test_response_requests_count_not_list():
    # given
    # when
    response = Response(True, ParsedData({}, {}), DataFactory())

    # then
    assert response.requests_count == 1


def test_response_requests():
    # given
    count = 10
    # when
    response = Response(True, ParsedData({}, {}), DataFactory())
    response.http_response = list(range(count))

    # then
    assert response.requests_count == count


def test_extend_query_parameters_method_for_request_factory():
    class StubRequestFactory(RequestFactory):
        def get_query_parameters(self, *args, **kwargs):
            return kwargs.get("query_parameters") or {}

    # given
    session = StubSession(is_open=True)
    request_factory = StubRequestFactory()
    request_factory.extend_query_parameters = Mock()
    request_factory.update_url = Mock()

    query_parameters = ("parameter", "value")
    extended_params = {"test": "value"}
    kwargs = {"query_parameters": query_parameters, "extended_params": extended_params}

    # when
    request_factory.create(session, ..., **kwargs)

    # then
    request_factory.extend_query_parameters.assert_called_once_with(
        query_parameters, extended_params=extended_params
    )


@patch("refinitiv.data.delivery._data._request_factory.Request")
def test_body_parameters_method_create_for_request_factory_default(patch_request_class):
    # given
    patch_request_class.return_value = Mock()

    session = StubSession(is_open=True)
    request_factory = RequestFactory()
    request_factory.update_url = Mock(return_value="url")

    # when
    request_factory.create(session, ..., **{})

    # then
    patch_request_class.assert_called_once_with(
        url=request_factory.update_url.return_value,
        method=RequestMethod.GET,
        headers={},
        json=None,
    )


@pytest.mark.parametrize(
    "method,headers,body_parameters",
    [
        args(
            method=RequestMethod.GET,
            headers={},
            body_parameters=None,
        ),
        args(
            method=RequestMethod.POST,
            headers={"Content-Type": "application/json"},
            body_parameters={},
        ),
        args(
            method=RequestMethod.PUT,
            headers={"Content-Type": "application/json"},
            body_parameters={},
        ),
        args(
            method=RequestMethod.DELETE,
            headers={"Content-Type": "application/json"},
            body_parameters=None,
        ),
    ],
)
@patch("refinitiv.data.delivery._data._request_factory.Request")
def test_body_parameters_method_create_for_request_factory(
    patch_request_class, method, headers, body_parameters
):
    # given
    patch_request_class.return_value = Mock()

    session = StubSession(is_open=True)
    request_factory = RequestFactory()
    request_factory.update_url = Mock(return_value="url")
    kwargs = {"method": method}

    # when
    request_factory.create(session, ..., **kwargs)

    # then
    patch_request_class.assert_called_once_with(
        url=request_factory.update_url.return_value,
        method=method,
        headers=headers,
        json=body_parameters,
    )
