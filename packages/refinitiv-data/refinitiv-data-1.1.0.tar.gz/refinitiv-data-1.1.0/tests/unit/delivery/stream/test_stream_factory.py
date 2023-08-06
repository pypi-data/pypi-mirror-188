from unittest.mock import patch

import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery._stream._stream_factory import StreamDetails, load_config
from tests.unit.conftest import StubSession


def fake_func(*args):
    return args


@pytest.mark.parametrize(
    ("api_config_str", "expected_config_str"),
    [
        ["streaming.pricing.endpoints.main", "apis.streaming.pricing.endpoints.main"],
        [
            "streaming.pricing.endpoints.main.path",
            "apis.streaming.pricing.endpoints.main",
        ],
        [
            "apis.streaming.pricing.endpoints.main",
            "apis.streaming.pricing.endpoints.main",
        ],
        [
            "apis.streaming.pricing.endpoints.main.path",
            "apis.streaming.pricing.endpoints.main",
        ],
    ],
)
def test_load_config(api_config_str, expected_config_str):
    # given
    session = StubSession()
    stream_details = StreamDetails(
        ContentType.STREAMING_CUSTOM, ..., ..., api_config_str
    )

    # when
    with patch(
        "refinitiv.data.delivery._stream._stream_factory.get_cxn_config",
        wraps=fake_func,
    ) as mock_func:
        load_config(stream_details, session)
        mock_func.assert_called_once_with(expected_config_str, session)


def test_load_config_raise_exception_with_empty_api_config_str():
    # given
    api_config_str = ""
    session = StubSession()
    stream_details = StreamDetails(
        ContentType.STREAMING_CUSTOM, ..., ..., api_config_str
    )

    # when
    with pytest.raises(
        ValueError,
        match="For ContentType.STREAMING_CUSTOM, api_config_key cannot be None",
    ):
        load_config(stream_details, session)


@pytest.mark.parametrize(
    "api_config_str",
    [
        "streaming.pricing.main",
        "apis.streaming.pricing.main",
        "apis.streaming.pricing.endpoints.",
        "apis.streaming.pricing.main.path",
        "streaming.pricing.main.path",
    ],
)
def test_load_config_raise_exception(api_config_str):
    # given
    session = StubSession()
    stream_details = StreamDetails(
        ContentType.STREAMING_CUSTOM, ..., ..., api_config_str
    )

    # when
    with pytest.raises(ValueError, match="Not an existing path"):
        load_config(stream_details, session)


@pytest.mark.parametrize(
    "api_config_str",
    [
        "streaming.pricing.endpoints",
        "apis.streaming.pricing.endpoints",
    ],
)
def test_load_config_raise_exception_not_valid_format(api_config_str):
    # given
    session = StubSession()
    stream_details = StreamDetails(
        ContentType.STREAMING_CUSTOM, ..., ..., api_config_str
    )

    # when
    with pytest.raises(
        ValueError, match="Not a valid format, use `apis.streaming.xxx.endpoints.xxx"
    ):
        load_config(stream_details, session)
