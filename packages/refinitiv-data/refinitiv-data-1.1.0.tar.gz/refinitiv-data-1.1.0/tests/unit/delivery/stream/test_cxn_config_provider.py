import warnings
from contextlib import nullcontext as does_not_raise

import pytest

import refinitiv.data._external_libraries.python_configuration as ext_config
from refinitiv.data._core.session._session_cxn_type import SessionCxnType
from refinitiv.data.delivery._stream._stream_cxn_config_provider import (
    CxnConfigProvider,
    PlatformAndDeployedCxnConfigProvider,
    DeployedCxnConfigProvider,
    PlatformCxnConfigProvider,
    DesktopCxnConfigProvider,
    get_cxn_config,
)
from refinitiv.data.errors import RDError
from tests.unit.conftest import (
    StubConfig,
    StubSession,
    args,
    error_403_access_denied_http_response_generator,
    StubResponse,
)


@pytest.mark.parametrize(
    "transport,url,expected",
    [
        args(
            transport="websocket",
            url="/head/middle/v1",
            expected=pytest.raises(ValueError),
        ),
        args(
            transport="websocket",
            url="://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
            expected=pytest.raises(ValueError),
        ),
        args(
            transport="websocket",
            url="ws://:443",
            expected=pytest.raises(ValueError),
        ),
        args(
            transport="websocket",
            url="ws:///head/middle/v1",
            expected=pytest.raises(ValueError),
        ),
        args(
            transport="websocket",
            url="wss://amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
            expected=does_not_raise(),
        ),
        args(
            transport="websocket",
            url="10.3.177.158:15000",
            expected=does_not_raise(),
        ),
        args(
            transport="websocket",
            url="//amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
            expected=does_not_raise(),
        ),
        args(
            transport="websocket",
            url="amer-3-t3.beta.streaming-pricing-api.refinitiv.com:443",
            expected=does_not_raise(),
        ),
        args(
            transport="websocket",
            url="//amer-3-t3.beta.streaming-pricing-api.refinitiv.com",
            expected=does_not_raise(),
        ),
        args(
            transport="websocket",
            url="amer-3-t3.beta.streaming-pricing-api.refinitiv.com",
            expected=does_not_raise(),
        ),
        args(
            transport="websocket",
            url="head/middle/v1",
            expected=does_not_raise(),
        ),
    ],
)
def test_url_parsed_success(transport, url, expected):
    with expected:
        CxnConfigProvider.info_from_url(transport=transport, url=url)


def test__request_infos_raises_exception_if_you_dont_have_access():
    discovery_url = "just-an-url"
    api_config_key = "just-a-key.endpoints.value"

    config = StubConfig()
    session = StubSession()
    session._response = error_403_access_denied_http_response_generator()

    config_provider = CxnConfigProvider()
    with pytest.raises(RDError):
        config_provider._request_infos(discovery_url, api_config_key, config, session)


@pytest.mark.parametrize(
    "provider_class, expected_num_infos",
    [
        (DesktopCxnConfigProvider, 3),
        (PlatformCxnConfigProvider, 3),
        (DeployedCxnConfigProvider, 1),
        (PlatformAndDeployedCxnConfigProvider, 1),
    ],
)
def test_possibility_to_set_list_of_streaming_urls(provider_class, expected_num_infos):
    config = ext_config.config_from_dict(
        {
            "sessions": {
                "platform": {
                    "default": {
                        "realtime-distribution-system": {"url": "10.3.177.158:15000"}
                    }
                }
            },
            "apis": {
                "streaming": {
                    "pricing": {
                        "endpoints": {
                            "main": {
                                "direct-url": [
                                    "beta.streaming-pricing.com",
                                    "wss://beta.streaming-pricing.com:443",
                                    "10.3.177.158:15000",
                                ],
                                "protocols": ["OMM"],
                                "locations": [],
                            }
                        }
                    }
                }
            },
        }
    )
    session = StubSession(config=config)
    config_provider = provider_class()
    cfg = config_provider.get_cfg(session, "apis.streaming.pricing.endpoints.main")

    assert cfg.num_infos == expected_num_infos


@pytest.mark.parametrize(
    "session_cxn_type, will_warn",
    [
        (SessionCxnType.DEPLOYED, False),
        (SessionCxnType.REFINITIV_DATA, False),
        (SessionCxnType.REFINITIV_DATA_AND_DEPLOYED, False),
        (SessionCxnType.DESKTOP, True),
    ],
)
def test_direct_url_cannot_used_with_desktop_session(session_cxn_type, will_warn):
    # given
    api_cfg_key = "apis.streaming.pricing.endpoints.main"
    config = ext_config.config_from_dict(
        {
            "sessions": {
                "platform": {
                    "default": {
                        "realtime-distribution-system": {"url": "10.3.177.158:15000"}
                    }
                }
            },
            "apis": {
                "streaming": {
                    "pricing": {
                        "url": "/streaming/pricing/v1",
                        "endpoints": {
                            "main": {
                                "direct-url": "wss://beta.streaming-pricing.com:443",
                                "path": "/",
                                "protocols": ["OMM"],
                                "locations": [],
                            }
                        },
                    }
                }
            },
        }
    )
    session = StubSession(
        config=config,
        response=StubResponse(
            {
                "services": [
                    {
                        "dataFormat": ["tr_json2"],
                        "endpoint": "localhost/api/rdp/streaming/pricing/v1/WebSocket",
                        "location": ["local"],
                        "port": 9001,
                        "provider": "local",
                        "transport": "websocket",
                    }
                ]
            }
        ),
    )
    session._session_cxn_type = session_cxn_type

    if will_warn:
        with warnings.catch_warnings(record=True) as w:
            # when
            cfg = get_cxn_config(api_cfg_key, session)

            # then
            assert len(w) == 1
            assert issubclass(w[0].category, UserWarning)
            assert (
                "direct-url config parameter cannot be used with desktop session, "
                f"the '{api_cfg_key}.direct-url' "
                "parameter will be discarded."
            ) == str(w[0].message)

            assert (
                cfg.url == "ws://localhost:9001/api/rdp/streaming/pricing/v1/WebSocket"
            )

    else:
        with warnings.catch_warnings(record=True) as w:
            # when
            get_cxn_config(api_cfg_key, session)

            # then
            assert len(w) == 0, w[0].message
