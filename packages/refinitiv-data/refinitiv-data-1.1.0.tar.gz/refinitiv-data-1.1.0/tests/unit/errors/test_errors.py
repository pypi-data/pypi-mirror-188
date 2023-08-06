import pytest

from refinitiv.data import errors


@pytest.fixture(
    params=[
        attr_name
        for attr_name in dir(errors)
        if not attr_name.startswith("_") and attr_name not in {"ItemWasNotRequested", "ScopeError"}
    ],
)
def error_class(request):
    attr_name = request.param
    cls = getattr(errors, attr_name)
    return cls


def test_error_code(error_class):
    # given
    code = 1

    # when
    error = error_class(code, "")

    # then
    assert error.code == code


def test_error_message(error_class):
    # given
    message = "message"

    # when
    error = error_class(0, message)

    # then
    assert error.message == message


def test_error_to_str(error_class):
    # given
    code = 1
    message = "message"
    expected = f"Error code {code} | {message}"
    error = error_class(code, message)

    # when
    testing_string = str(error)

    # then
    assert testing_string == expected, testing_string
