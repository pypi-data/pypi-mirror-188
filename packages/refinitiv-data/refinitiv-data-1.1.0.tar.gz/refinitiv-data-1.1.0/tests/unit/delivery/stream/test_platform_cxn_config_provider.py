import pytest

from refinitiv.data._core.session._session_cxn_type import SessionCxnType
from refinitiv.data.delivery._stream._stream_cxn_config_provider import (
    PlatformCxnConfigProvider,
    get_discovery_url,
)
from tests.unit.conftest import StubSession, StubConfig, StubResponse, args


def create_platform_cxn_config_provider(rawconfig):
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    config = StubConfig(rawconfig)
    session = StubSession(
        config=config, response=response, session_cxn_type=SessionCxnType.REFINITIV_DATA
    )
    provider = PlatformCxnConfigProvider()
    return provider, session


@pytest.mark.parametrize(
    "rawconfig,expected_url",
    [
        args(
            input={
                "apis.streaming.middle.url": "/head/middle/v1",
                "apis.streaming.middle.endpoints.tail.path": "/",
                "apis.streaming.middle.endpoints.tail.locations": [],
                "apis.streaming.middle.endpoints.tail.protocols": [],
            },
            expected="wss://ap-southeast-1-aws-1-lrg.optimized-pricing:443/api.refinitiv.net",
        ),
        args(
            input={
                "apis.streaming.middle.url": "/head/middle/v1",
                "apis.streaming.middle.endpoints.tail.path": "/",
                "apis.streaming.middle.endpoints.tail.locations": "amer",
                "apis.streaming.middle.endpoints.tail.protocols": "OMM",
            },
            expected="wss://ap-southeast-1-aws-1-lrg.optimized-pricing:443/api.refinitiv.net",
        ),
        args(
            input={
                "apis.streaming.middle.endpoints.tail.direct-url": "wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
                "apis.streaming.middle.endpoints.tail.protocols": [],
            },
            expected="wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443/WebSocket",
        ),
        args(
            input={
                "apis.streaming.middle.endpoints.tail.direct-url": "//amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
                "apis.streaming.middle.endpoints.tail.protocols": [],
            },
            expected="wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443/WebSocket",
        ),
        args(
            input={
                "apis.streaming.middle.endpoints.tail.direct-url": "//amer-3-t3.beta.streaming-pricing-api.refinitiv.com",
                "apis.streaming.middle.endpoints.tail.protocols": [],
            },
            expected="ws://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:80/WebSocket",
        ),
        args(
            input={
                "apis.streaming.middle.endpoints.tail.direct-url": "amer-3-t3.beta.streaming-pricing-api.refinitiv.com",
                "apis.streaming.middle.endpoints.tail.protocols": [],
            },
            expected="ws://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:80/WebSocket",
        ),
    ],
)
def test_configuration_parsed_correct(rawconfig, expected_url):
    # given
    provider, session = create_platform_cxn_config_provider(rawconfig)

    # when
    config = provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")

    # then
    assert config.url == expected_url


def test_will_raise_error_if_no_url_in_config():
    # given
    provider, session = create_platform_cxn_config_provider({})

    # then
    with pytest.raises(KeyError, match="apis.streaming.middle.url"):
        # when
        provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")


def test_will_raise_error_if_no_path_in_config():
    # given
    provider, session = create_platform_cxn_config_provider(
        {
            "apis.streaming.middle.url": "/head/middle/v1",
        }
    )

    # then
    with pytest.raises(KeyError, match="Cannot find discovery endpoint"):
        # when
        provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")


def test_will_raise_error_if_no_locations_in_config():
    # given
    provider, session = create_platform_cxn_config_provider(
        {
            "apis.streaming.middle.url": "/head/middle/v1",
            "apis.streaming.middle.endpoints.tail.path": "/",
        }
    )

    # then
    with pytest.raises(
        KeyError, match="apis.streaming.middle.endpoints.tail.locations"
    ):
        # when
        provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")


def test_will_raise_error_if_no_protocols_in_config():
    # given
    provider, session = create_platform_cxn_config_provider(
        {
            "apis.streaming.middle.url": "/head/middle/v1",
            "apis.streaming.middle.endpoints.tail.path": "/",
            "apis.streaming.middle.endpoints.tail.locations": [],
        }
    )

    # then
    with pytest.raises(
        KeyError, match="apis.streaming.middle.endpoints.tail.protocols"
    ):
        # when
        provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")


def test_infos_parsed_correct():
    # given
    provider, session = create_platform_cxn_config_provider(
        {
            "apis.streaming.middle.url": "http://example.dom/head/middle/v1",
            "apis.streaming.middle.endpoints.tail.path": "/",
            "apis.streaming.middle.endpoints.tail.locations": [],
            "apis.streaming.middle.endpoints.tail.protocols": [],
        }
    )

    # when
    config = provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")

    # then
    assert len(config.urls) == 12


def test_infos_filtered_by_location_correct():
    # given
    expected_location = "ap-southeast-1a"
    provider, session = create_platform_cxn_config_provider(
        {
            "apis.streaming.middle.url": "path/to/head/middle/v1",
            "apis.streaming.middle.endpoints.tail.path": "/",
            "apis.streaming.middle.endpoints.tail.locations": [expected_location],
            "apis.streaming.middle.endpoints.tail.protocols": [],
        }
    )

    # when
    config = provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")

    # then
    assert len(config.urls) == 2


def test_infos_filtered_by_location_no_duplication():
    # given
    expected_locations = ["ap-southeast-1a", "ap-southeast-1b"]
    provider, session = create_platform_cxn_config_provider(
        {
            "apis.streaming.middle.url": "path/to/head/middle/v1",
            "apis.streaming.middle.endpoints.tail.path": "/",
            "apis.streaming.middle.endpoints.tail.locations": expected_locations,
            "apis.streaming.middle.endpoints.tail.protocols": [],
        }
    )

    # when
    config = provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")

    # then
    assert len(config.urls) == 3


@pytest.mark.parametrize(
    "config,expected_url",
    [
        args(
            config=StubConfig(
                {
                    "apis.streaming.streaming_name.url": "/streaming_name/path/v1",
                    "apis.streaming.streaming_name.endpoints.endpoint_name.path": "/",
                }
            ),
            expected="https://root_url/streaming_name/path/v1/",
        ),
        args(
            config=StubConfig(
                {
                    "apis.streaming.streaming_name.url": "https://path.com/streaming_name/path/v1",
                    "apis.streaming.streaming_name.endpoints.endpoint_name.path": "/",
                }
            ),
            expected="https://path.com/streaming_name/path/v1/",
        ),
        args(
            config=StubConfig(
                {
                    "apis.streaming.streaming_name.url": "://path.com/streaming_name/path/v1",
                    "apis.streaming.streaming_name.endpoints.endpoint_name.path": "/",
                }
            ),
            expected="https://root_url/://path.com/streaming_name/path/v1/",
        ),
        args(
            config=StubConfig(
                {
                    "apis.streaming.streaming_name.url": "//path.com/streaming_name/path/v1",
                    "apis.streaming.streaming_name.endpoints.endpoint_name.path": "/",
                }
            ),
            expected="https://root_url/path.com/streaming_name/path/v1/",
        ),
        args(
            config=StubConfig(
                {
                    "apis.streaming.streaming_name.url": "/path.com/streaming_name/path/v1",
                    "apis.streaming.streaming_name.endpoints.endpoint_name.path": "/",
                }
            ),
            expected="https://root_url/path.com/streaming_name/path/v1/",
        ),
    ],
)
def test_get_discovery_url(config, expected_url):
    # when
    base_streaming_name = "apis.streaming.streaming_name"
    full_streaming_name = f"{base_streaming_name}.endpoints.endpoint_name"
    root_url = "https://root_url"
    testing_url = get_discovery_url(
        root_url, base_streaming_name, full_streaming_name, config
    )

    # then
    assert testing_url == expected_url, testing_url


def test_tcp_filtering():
    provider, session = create_platform_cxn_config_provider(
        {
            "apis.streaming.pricing.url": "http://example.dom/apis/pricing/v5",
            "apis.streaming.pricing.endpoints.endpoint.path": "/",
            "apis.streaming.pricing.endpoints.endpoint.locations": [],
            "apis.streaming.pricing.endpoints.endpoint.protocols": [],
            "apis.streaming.pricing.use_rwf": True,
        }
    )

    # when
    config = provider.get_cfg(session, "apis.streaming.pricing.endpoints.endpoint")

    # then
    assert len(config.urls) == 12
    assert all(url.endswith(":14002") for url in config.urls)


def test_tier_filtering():
    # given
    provider, session = create_platform_cxn_config_provider(
        {
            "apis.streaming.pricing.url": "http://example.dom/apis/pricing/v5",
            "apis.streaming.pricing.endpoints.endpoint.path": "/",
            "apis.streaming.pricing.endpoints.endpoint.locations": [],
            "apis.streaming.pricing.endpoints.endpoint.protocols": [],
            "apis.streaming.pricing.use_rwf": True,
            "apis.streaming.pricing.tier": 1500,
        }
    )

    # when
    config = provider.get_cfg(session, "apis.streaming.pricing.endpoints.endpoint")

    # then
    assert len(config.urls) == 11
