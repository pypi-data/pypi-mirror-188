import pytest
from mock.mock import MagicMock


@pytest.fixture(scope="function")
def session_mock():
    session_mock_ = MagicMock()
    config_mock = MagicMock()
    config_mock.get_str.return_value = "string"
    session_mock_._get_endpoint_config.return_value = config_mock
    return session_mock_
