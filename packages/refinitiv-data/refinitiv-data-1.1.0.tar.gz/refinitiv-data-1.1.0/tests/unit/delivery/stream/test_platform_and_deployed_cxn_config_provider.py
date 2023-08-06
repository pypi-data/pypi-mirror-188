import pytest

from refinitiv.data._core.session._session_cxn_type import SessionCxnType
from refinitiv.data.delivery._stream._stream_cxn_config_provider import (
    PlatformAndDeployedCxnConfigProvider,
)
from tests.unit.conftest import StubSession, StubConfig, StubResponse, args


def create_platform_and_deployed_cxn_config_provider(rawconfig):
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    config = StubConfig(rawconfig)
    session = StubSession(
        config=config,
        response=response,
        session_cxn_type=SessionCxnType.REFINITIV_DATA_AND_DEPLOYED,
    )
    provider = PlatformAndDeployedCxnConfigProvider()
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
    provider, session = create_platform_and_deployed_cxn_config_provider(rawconfig)

    # when
    config = provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")

    # then
    assert config.url == expected_url


@pytest.mark.parametrize(
    "rawconfig,expected_url",
    [
        args(
            input={
                "sessions.platform.default.realtime-distribution-system.url": "wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
            },
            expected="wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443/WebSocket",
        ),
        args(
            input={
                "sessions.platform.default.realtime-distribution-system.url": "//amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
            },
            expected="wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443/WebSocket",
        ),
        args(
            input={
                "sessions.platform.default.realtime-distribution-system.url": "//amer-3-t3.beta.streaming-pricing-api.refinitiv.com",
            },
            expected="ws://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:80/WebSocket",
        ),
        args(
            input={
                "sessions.platform.default.realtime-distribution-system.url": "amer-3-t3.beta.streaming-pricing-api.refinitiv.com",
            },
            expected="ws://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:80/WebSocket",
        ),
    ],
)
def test_configuration_parsed_correct_without_deployed_host_in_config(
    rawconfig, expected_url
):
    provider, session = create_platform_and_deployed_cxn_config_provider(rawconfig)

    # when
    config = provider.get_cfg(session, "apis.streaming.pricing.endpoints.main")

    # then
    assert config.url == expected_url


def test_will_raise_error_if_no_url_in_config():
    # given
    provider, session = create_platform_and_deployed_cxn_config_provider({})

    # then
    with pytest.raises(KeyError, match="apis.streaming.middle.url"):
        # when
        provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")


@pytest.mark.parametrize(
    "deployed_host,expected_url",
    [
        args(
            input="wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
            expected="wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443/WebSocket",
        ),
        args(
            input="10.3.177.158:15000",
            expected="ws://10.3.177.158:15000/WebSocket",
        ),
        args(
            input="//amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
            expected="wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443/WebSocket",
        ),
        args(
            input="amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
            expected="wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443/WebSocket",
        ),
        args(
            input="//amer-3-t3.beta.streaming-pricing-api.refinitiv.com",
            expected="ws://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:80/WebSocket",
        ),
        args(
            input="amer-3-t3.beta.streaming-pricing-api.refinitiv.com",
            expected="ws://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:80/WebSocket",
        ),
    ],
)
def test_configuration_parsed_correct_with_deployed_host(deployed_host, expected_url):
    # given
    session = StubSession(
        deployed_platform_host=deployed_host,
        session_cxn_type=SessionCxnType.REFINITIV_DATA_AND_DEPLOYED,
    )
    provider = PlatformAndDeployedCxnConfigProvider()

    # when
    config = provider.get_cfg(session, "apis.streaming.pricing.endpoints.main")

    # then
    assert config.url == expected_url


def test_will_raise_error_if_no_path_in_config():
    # given
    provider, session = create_platform_and_deployed_cxn_config_provider(
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
    provider, session = create_platform_and_deployed_cxn_config_provider(
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
    provider, session = create_platform_and_deployed_cxn_config_provider(
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
    provider, session = create_platform_and_deployed_cxn_config_provider(
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
    provider, session = create_platform_and_deployed_cxn_config_provider(
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
