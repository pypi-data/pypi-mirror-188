from functools import partial
from unittest import mock

import pytest

import refinitiv.data as rd
from refinitiv.data import OpenState
from refinitiv.data._content_type import ContentType
from refinitiv.data.content._universe_streams import _UniverseStreams
from refinitiv.data.content.custom_instruments._stream_facade import (
    CustomInstsUniverseStreams,
    Stream as CustomInstrumentsStreamFacade,
)
from refinitiv.data.content.ipa.financial_contracts._quantitative_data_stream import (
    QuantitativeDataStream,
)
from refinitiv.data.content.ipa.financial_contracts._stream_facade import (
    Stream as FinancialContractsStreamFacade,
)
from refinitiv.data.content.pricing._stream_facade import Stream as PricingStreamFacade
from refinitiv.data.content.pricing.chain._stream import StreamingChain
from refinitiv.data.content.pricing.chain._stream_facade import (
    Stream as PricingChainStreamFacade,
)
from refinitiv.data.content.trade_data_service._stream import TradeDataStream
from refinitiv.data.content.trade_data_service._stream_facade import (
    Stream as TradeDataStreamFacade,
)
from refinitiv.data.delivery._stream import (
    _RDPStream,
    StreamState,
    _OMMStream,
    RDPStream,
    OMMStream,
)
from tests.unit.conftest import StubSession, StubResponse

ids = [
    "pricing",
    "trade_data_service",
    "rdp_stream",
    "omm_stream",
    "pricing.chain",
    "financial_contracts.bond",
    "custom_instruments",
]


@pytest.mark.parametrize(
    argnames="definition",
    argvalues=[
        rd.content.pricing.Definition("universe"),
        rd.content.trade_data_service.Definition(),
        rd.delivery.rdp_stream.Definition("", [], [], {}, "api/path"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.pricing.chain.Definition("universe"),
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=ids,
)
def test_stream_can_be_opened_via_context_manager(definition):
    session = StubSession(is_open=True)
    stream = definition.get_stream(session)
    try:
        stream._stream._stream._do_open = lambda *_, **__: None
        stream._stream._stream._do_close = lambda *_, **__: None
    except AttributeError:
        stream._stream._do_open = lambda *_, **__: None
        stream._stream._do_close = lambda *_, **__: None

    with stream:
        assert stream.open_state is OpenState.Opened

    assert stream.open_state is OpenState.Closed


def test_rdp_stream_got_alarm_message():
    # given
    def on_error(*args, **kwargs):
        nonlocal error_printed
        error_printed = True

    session = StubSession()
    error_printed = False
    stream = _RDPStream(3, session, "", [], [], {}, {})
    stream._error = on_error
    stream._state = StreamState.Opening
    alarm_message = {
        "data": [],
        "state": {
            "id": "QPSValuation.ERROR_REQUEST_TIMEOUT",
            "code": 408,
            "status": "ERROR",
            "message": "The request could not be executed within the service allocated time",
            "stream": "Open",
        },
        "type": "Alarm",
        "streamID": "3",
    }

    # when
    stream.dispatch_alarm({}, alarm_message)

    # then
    assert error_printed is True
    assert stream._opened.is_set() is True


@pytest.mark.parametrize(
    argnames="definition",
    argvalues=[
        rd.content.pricing.Definition("universe"),
        rd.content.trade_data_service.Definition(),
        rd.delivery.rdp_stream.Definition("", [], [], {}, "api/path"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.pricing.chain.Definition("universe"),
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=ids,
)
def test_stream_open_always_use_default_session_if_not_passed_in_get_stream(definition):
    # given
    session_a = StubSession(is_open=True)
    rd.session.set_default(session_a)
    stream = definition.get_stream()
    if hasattr(stream._stream, "_stream"):
        stream._stream._stream._do_open = lambda *args, **kwargs: None
    else:
        stream._stream._do_open = lambda *args, **kwargs: None

    assert stream._stream.session == session_a

    # when
    session_b = StubSession(is_open=True)
    rd.session.set_default(session_b)
    stream.open()

    # then
    assert stream._stream.session == session_b

    rd.session.set_default(None)


@pytest.mark.parametrize(
    argnames="definition",
    argvalues=[
        rd.content.pricing.Definition("universe"),
        rd.content.trade_data_service.Definition(),
        rd.delivery.rdp_stream.Definition("", [], [], {}, "api/path"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.pricing.chain.Definition("universe"),
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=ids,
)
def test_stream_open_always_use_session_from_get_stream_if_passed(definition):
    # given
    session_a = StubSession(is_open=True)
    rd.session.set_default(session_a)
    stream = definition.get_stream(session_a)
    if hasattr(stream._stream, "_stream"):
        stream._stream._stream._do_open = lambda *args, **kwargs: None
    else:
        stream._stream._do_open = lambda *args, **kwargs: None

    assert stream._stream.session == session_a

    # when
    session_b = StubSession(is_open=True)
    rd.session.set_default(session_b)
    stream.open()

    # then
    assert stream._stream.session == session_a

    rd.session.set_default(None)


@pytest.mark.parametrize(
    argnames="definition",
    argvalues=[
        rd.content.pricing.Definition("universe"),
        rd.content.trade_data_service.Definition(),
        rd.delivery.rdp_stream.Definition("", [], [], {}, "api/path"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.pricing.chain.Definition("universe"),
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=ids,
)
def test_user_cannot_create_stream_without_any_session(definition):
    # then
    with pytest.raises(
        AttributeError,
        match="No default session created yet. Please create a session first!",
    ):
        # given
        definition.get_stream()


@pytest.mark.parametrize(
    argnames="definition",
    argvalues=[
        rd.content.pricing.Definition("universe"),
        rd.content.trade_data_service.Definition(),
        rd.delivery.rdp_stream.Definition("", [], [], {}, "api/path"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.pricing.chain.Definition("universe"),
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=ids,
)
def test_user_can_create_stream_with_opened_default_session(definition):
    # given
    session = StubSession(is_open=True)
    rd.session.set_default(session)

    # when
    try:
        definition.get_stream()
    except Exception as e:
        assert False, str(e)
    else:
        # then
        assert True

    rd.session.set_default(None)


@pytest.mark.parametrize(
    argnames="definition",
    argvalues=[
        rd.content.pricing.Definition("universe"),
        rd.content.trade_data_service.Definition(),
        rd.delivery.rdp_stream.Definition("", [], [], {}, "api/path"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.pricing.chain.Definition("universe"),
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
    ],
    ids=[
        "pricing",
        "trade_data_service",
        "rdp_stream",
        "omm_stream",
        "pricing.chain",
        "financial_contracts.bond",
    ],
)
def test_user_can_create_stream_with_not_opened_default_session(definition):
    # given
    session = StubSession()
    rd.session.set_default(session)

    try:
        # when
        definition.get_stream()
    except Exception as e:
        assert False, str(e)
    else:
        # then
        assert True

    rd.session.set_default(None)


@pytest.mark.parametrize(
    argnames="definition",
    argvalues=[
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=[
        "custom_instruments",
    ],
)
def test_user_cannot_create_stream_with_not_opened_default_session(definition):
    # given
    session = StubSession()
    rd.session.set_default(session)

    # then
    with pytest.raises(
        ValueError, match="Session is not opened. Can't send any request"
    ):
        # when
        definition.get_stream()

    rd.session.set_default(None)


@pytest.mark.parametrize(
    argnames="internal_stream_class",
    argvalues=[
        partial(_UniverseStreams, ContentType.STREAMING_CUSTOM, "universe"),
        TradeDataStream,
        partial(
            _RDPStream,
            **{
                "stream_id": 0,
                "service": "",
                "universe": [],
                "view": [],
                "parameters": {},
                "details": {},
            },
        ),
        partial(_OMMStream, **{"stream_id": 0, "name": "", "details": {}}),
        partial(StreamingChain, **{"name": ""}),
        partial(QuantitativeDataStream, **{"universe": ""}),
        partial(CustomInstsUniverseStreams, **{"content_type": {}, "universe": ""}),
    ],
    ids=ids,
)
def test_internal_stream_cannot_be_created_without_session(internal_stream_class):
    # then
    with pytest.raises(
        AttributeError, match="'NoneType' object has no attribute 'logger'"
    ):
        # when
        internal_stream_class(session=None)


@pytest.mark.parametrize(
    argnames="facade_stream_class",
    argvalues=[
        PricingStreamFacade,
        TradeDataStreamFacade,
        partial(
            RDPStream,
            **{
                "api": "",
                "service": "",
                "universe": [],
                "view": [],
                "parameters": {},
            },
        ),
        partial(OMMStream, **{"name": ""}),
        partial(PricingChainStreamFacade, **{"name": ""}),
        partial(FinancialContractsStreamFacade, **{"universe": ""}),
        partial(CustomInstrumentsStreamFacade, **{"uuid": "uuid"}),
    ],
    ids=ids,
)
def test_facade_stream_can_be_created_with_not_opened_default_session(
    facade_stream_class,
):
    # given
    session = StubSession()
    rd.session.set_default(session)

    try:
        # when
        facade_stream_class()
    except Exception as e:
        assert False, str(e)
    else:
        # then
        assert True

    rd.session.set_default(None)


@pytest.mark.parametrize(
    argnames="facade_stream_class",
    argvalues=[
        CustomInstrumentsStreamFacade,
    ],
    ids=[
        "custom_instruments",
    ],
)
def test_facade_stream_cannot_be_created_with_not_opened_default_session(
    facade_stream_class,
):
    # given
    session = StubSession()
    rd.session.set_default(session)

    # then
    with pytest.raises(
        ValueError, match="Session is not opened. Can't send any request"
    ):
        # when
        facade_stream_class()

    rd.session.set_default(None)


@pytest.mark.parametrize(
    argnames="internal_stream_class",
    argvalues=[
        partial(
            _UniverseStreams,
            **{
                "content_type": ContentType.STREAMING_CUSTOM,
                "universe": "universe",
                "api": "api",
            },
        ),
        TradeDataStream,
        partial(
            _RDPStream,
            **{
                "stream_id": 0,
                "service": "",
                "universe": [],
                "view": [],
                "parameters": {},
                "details": {},
            },
        ),
        partial(_OMMStream, **{"stream_id": 0, "name": "", "details": {}}),
        partial(StreamingChain, **{"name": ""}),
        partial(QuantitativeDataStream, **{"universe": ""}),
        partial(CustomInstsUniverseStreams, **{"content_type": {}, "universe": ""}),
    ],
    ids=ids,
)
def test_internal_stream_cannot_set_new_session_if_stream_already_opened(
    internal_stream_class,
):
    # given
    session_first = StubSession(is_open=True)
    stream = internal_stream_class(session=session_first)
    if hasattr(stream, "_stream"):
        stream._stream._do_open = lambda *args, **kwargs: None
    else:
        stream._do_open = lambda *args, **kwargs: None

    # when
    stream.open()
    session_second = StubSession(is_open=True)
    stream.session = session_second

    # then
    assert stream.session == session_first


class StubOMMStream:
    def __init__(self, service, *args, **kwargs):
        self.classname = ...
        self.on = lambda *args, **kwargs: ...
        self.open = lambda *args, **kwargs: ...
        self.id = ...
        assert service == "test_service"


infos = {
    "services": [
        {
            "port": 443,
            "location": ["ap-northeast-1a"],
            "transport": "websocket",
            "provider": "aws",
            "endpoint": "ap-northeast-1-aws-1-sm.optimized-pricing-api.refinitiv.net",
            "dataFormat": ["tr_json2"],
        },
    ]
}


def http_request(request):
    url = request.url
    if url.startswith("test_get_rdp_url_root/streaming"):
        return StubResponse(content_data=infos)
    return StubResponse({})


@pytest.mark.parametrize(
    ("name_in_config", "definition"),
    [
        ("pricing", rd.content.pricing.Definition("EUR=")),
        ("custom-instruments", rd.content.custom_instruments.Definition("EUR=")),
    ],
)
def test_service_in_config_omm(name_in_config, definition):
    session = StubSession(is_open=True, stream_auto_reconnection=True)
    session.http_request = http_request
    session.config.set_param(
        f"apis.streaming.{name_in_config}.service", "test_service", auto_create=True
    )
    with mock.patch(
        "refinitiv.data.delivery._stream._stream_factory._OMMStream", new=StubOMMStream
    ):
        stream = definition.get_stream(session=session)
        stream.open()


class StubRDPStream:
    def __init__(self, service, *args, **kwargs):
        self.classname = ...
        self.on_response = lambda *args, **kwargs: ...
        self.on_update = lambda *args, **kwargs: ...
        self.on_ack = lambda *args, **kwargs: ...
        self.on_alarm = lambda *args, **kwargs: ...
        self.on = lambda *args, **kwargs: ...
        self.open = lambda *args, **kwargs: ...
        assert service == "test_service"


@pytest.mark.parametrize(
    ("name_in_config", "definition"),
    [
        ("trading-analytics", rd.content.trade_data_service.Definition()),
        (
            "quantitative-analytics",
            rd.content.ipa.financial_contracts.option.Definition(),
        ),
    ],
)
def test_service_in_config_rdp(name_in_config, definition):
    session = StubSession(is_open=True, stream_auto_reconnection=True)
    session.http_request = http_request
    session.config.set_param(
        f"apis.streaming.{name_in_config}.service", "test_service", auto_create=True
    )
    with mock.patch(
        "refinitiv.data.delivery._stream._stream_factory._RDPStream", new=StubRDPStream
    ):
        stream = definition.get_stream(session=session)
        stream.open()


{"apis": {"streaming": {"pricing": {"service": "MY_SERVICE"}}}}
