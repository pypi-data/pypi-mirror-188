import pandas as pd


def test_response(response):
    assert response


def test_success_response_is_success(response):
    success = response.is_success
    assert success, [
        response.errors,
        response.request_message.url,
    ]
    assert isinstance(success, bool)


def test_not_success_response_is_success(response):
    success = response.is_success
    assert not success
    assert isinstance(success, bool)


def test_success_response_data(response):
    data = response.data
    assert data, f"No data in response,\nresponse.data={data}"
    assert isinstance(
        data.raw, (dict, list)
    ), f"data.raw is not a dict or list it is a {type(data.raw)}"
    assert isinstance(
        data.df, pd.DataFrame
    ), f"data.df is not a DataFrame it is a {type(data.df)}"
    assert not data.df.empty, "Data frame is empty"


def test_success_response_data_empty(response):
    data = response.data
    assert data
    assert isinstance(data.raw, dict)
    assert isinstance(data.df, pd.DataFrame)
    assert data.df.empty


def test_success_response_data_text(response):
    data = response.data
    assert data
    assert isinstance(data.raw, dict)
    assert isinstance(data.text, str)
    assert data.text


def test_not_success_response_data(response):
    data = response.data
    assert data
    assert data.raw
    assert data.df is None or data.df.empty


def test_success_response_status(status):
    assert status
    assert isinstance(status, dict)
    assert status["http_status_code"] == 200, (
        status["error"] if status.get("error") else status
    )
    assert status["http_reason"] == "OK"
    has_content = status.get("content", False)
    assert not has_content or "error" not in status["content"]


def test_not_success_response_status(response):
    status = response.http_status
    assert status
    assert isinstance(status, dict)
    has_content = status.get("content", False)
    has_error = status.get("error", False)
    assert has_content or has_error
    assert (has_content and "error" in status["content"]) or "error" in status


def test_response_headers(response):
    headers = response.http_headers
    assert headers


def test_response_request_message(response):
    request_message = response.request_message
    assert request_message


def test_response_closure(response, mock_closure=None):
    closure = response.closure
    if mock_closure:
        assert closure == mock_closure
    else:
        assert closure is None


def success_response_tests(response, mock_closure=None):
    test_success_response_is_success(response)
    test_response(response)
    test_response_closure(response, mock_closure)
    test_response_request_message(response)
    test_response_headers(response)
    test_success_response_status(response.http_status)
    test_success_response_data(response)


def success_response_text_tests(response, mock_closure=None):
    test_response(response)
    test_response_closure(response, mock_closure)
    test_response_request_message(response)
    test_response_headers(response)
    test_success_response_status(response.http_status)
    test_success_response_data_text(response)
    test_success_response_is_success(response)


def success_response_data_empty_tests(response):
    test_response(response)
    test_response_closure(response)
    test_response_request_message(response)
    test_response_headers(response)
    test_success_response_status(response.http_status)
    test_success_response_data_empty(response)
    test_success_response_is_success(response)


def not_success_response_tests(response, check_status=True):
    test_response(response)
    test_response_closure(response)
    test_response_request_message(response)
    test_response_headers(response)
    check_status and test_not_success_response_status(response)
    test_not_success_response_data(response)
    test_not_success_response_is_success(response)


def test_alignment_response_success(response):
    assert response, f"Responce is empty"
    test_success_response_is_success(response)
    test_success_response_status(response.http_status)
    assert response.http_headers, f"HTTP headers are empty\n{response.http_headers}"
    assert response.data.raw, "Raw data is empty"
    test_success_response_data(response)
