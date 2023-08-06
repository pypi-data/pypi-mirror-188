import pytest

from refinitiv.data._core.session._session_cxn_type import SessionCxnType
from refinitiv.data.delivery._stream._stream_cxn_config_provider import (
    DesktopCxnConfigProvider,
)
from tests.unit.conftest import StubSession, StubConfig, StubResponse, args


def create_desktop_cxn_config_provider(rawconfig):
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    config = StubConfig(rawconfig)
    session = StubSession(
        config=config, response=response, session_cxn_type=SessionCxnType.DESKTOP
    )
    provider = DesktopCxnConfigProvider()
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
    ],
)
def test_configuration_parsed_correct(rawconfig, expected_url):
    # given
    provider, session = create_desktop_cxn_config_provider(rawconfig)

    # when
    config = provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")

    # then
    assert config.url == expected_url


def test_will_raise_error_if_no_url_in_config():
    # given
    provider, session = create_desktop_cxn_config_provider({})

    # then
    with pytest.raises(KeyError, match="apis.streaming.middle.url"):
        # when
        provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")


def test_will_raise_error_if_no_path_in_config():
    # given
    provider, session = create_desktop_cxn_config_provider(
        {"apis.streaming.middle.url": "/head/middle/v1"}
    )

    # then
    with pytest.raises(KeyError, match="Cannot find discovery endpoint"):
        # when
        provider.get_cfg(session, "apis.streaming.middle.endpoints.tail")


def test_will_raise_error_if_no_protocols_in_config():
    # given
    provider, session = create_desktop_cxn_config_provider(
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
    provider, session = create_desktop_cxn_config_provider(
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
