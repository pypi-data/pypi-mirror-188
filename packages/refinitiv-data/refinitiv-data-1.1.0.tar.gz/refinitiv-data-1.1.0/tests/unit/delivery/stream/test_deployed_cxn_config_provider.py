import pytest

from refinitiv.data._core.session._session_cxn_type import SessionCxnType
from refinitiv.data.delivery._stream._stream_cxn_config_provider import (
    DeployedCxnConfigProvider,
)
from tests.unit.conftest import StubSession, StubConfig, StubResponse, args


def create_deployed_cxn_config_provider(rawconfig):
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    config = StubConfig(rawconfig)
    session = StubSession(
        config=config, response=response, session_cxn_type=SessionCxnType.DEPLOYED
    )
    provider = DeployedCxnConfigProvider()
    return provider, session


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
    provider, session = create_deployed_cxn_config_provider(rawconfig)

    # when
    config = provider.get_cfg(session, "head.endpoints.tail")

    # then
    assert config.url == expected_url


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
        deployed_platform_host=deployed_host, session_cxn_type=SessionCxnType.DEPLOYED
    )
    provider = DeployedCxnConfigProvider()

    # when
    config = provider.get_cfg(session, "head.endpoints.tail")

    # then
    assert config.url == expected_url
