from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from refinitiv.data.content import trade_data_service
from tests.unit.conftest import StubSession
import refinitiv.data as rd
from refinitiv.data._core.session import GrantPassword, EventCode
from refinitiv.data.session import platform, desktop


@pytest.mark.parametrize(
    "defn_with_stream",
    [
        rd.content.pricing.Definition("universe"),
        rd.delivery.rdp_stream.Definition("", [], [], {}, "test.api"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.custom_instruments.Definition("universe"),
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
        rd.content.ipa.financial_contracts.cap_floor.Definition("universe"),
        rd.content.ipa.financial_contracts.cds.Definition("universe"),
        rd.content.ipa.financial_contracts.cross.Definition("universe"),
        rd.content.ipa.financial_contracts.swap.Definition("universe"),
        rd.content.ipa.financial_contracts.option.Definition(),
        rd.content.ipa.financial_contracts.repo.Definition(),
        rd.content.ipa.financial_contracts.swaption.Definition(),
        rd.content.ipa.financial_contracts.term_deposit.Definition(),
    ],
    ids=[
        "pricing",
        "rdp_stream",
        "omm_stream",
        "custom_instruments",
        "financial_contracts.bond",
        "financial_contracts.cap_floor",
        "financial_contracts.cds",
        "financial_contracts.cross",
        "financial_contracts.swap",
        "financial_contracts.option",
        "financial_contracts.repo",
        "financial_contracts.swaption",
        "financial_contracts.term_deposit",
    ],
)
def test_on_update(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_update_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_update(on_update_callback)
    stream._stream._on_stream_update(MagicMock(), {"Fields": {}})

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "defn_with_stream",
    [
        rd.content.pricing.Definition("universe"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=[
        "pricing",
        "omm_stream",
        "custom_instruments",
    ],
)
def test_on_refresh(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_refresh_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_refresh(on_refresh_callback)
    stream._stream._on_stream_refresh(MagicMock(), {"Fields": {}})

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "defn_with_stream",
    [
        rd.content.pricing.Definition("universe"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=[
        "pricing",
        "omm_stream",
        "custom_instruments",
    ],
)
def test_on_status(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_status_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_status(on_status_callback)
    stream._stream._on_stream_status(MagicMock(), {"Fields": {}})

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "mock_name, obj_definition",
    [
        ("universe", rd.content.pricing.Definition("universe")),
        ("name", rd.delivery.omm_stream.Definition("name")),
        ("S)name.", rd.content.custom_instruments.Definition("name")),
    ],
    ids=[
        "pricing",
        "omm_stream",
        "custom_instruments",
    ],
)
def test_on_complete(mock_name, obj_definition):
    # given
    session = StubSession(is_open=True)
    stream = obj_definition.get_stream(session)

    mock_stream = SimpleNamespace()
    mock_stream.name = mock_name

    callback_called = False

    def on_complete_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_complete(on_complete_callback)
    stream._stream._on_stream_complete(mock_stream)

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "defn_with_stream",
    [
        rd.content.pricing.Definition("universe"),
        rd.delivery.omm_stream.Definition(""),
        rd.content.custom_instruments.Definition("universe"),
    ],
    ids=[
        "pricing",
        "omm_stream",
        "custom_instruments",
    ],
)
def test_on_error(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_error_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_error(on_error_callback)
    stream._stream._on_stream_error(MagicMock(), {"Fields": {}})

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "defn_with_stream",
    [
        rd.delivery.rdp_stream.Definition("", [], [], {}, "test.api"),
        rd.delivery.omm_stream.Definition(""),
    ],
    ids=[
        "rdp_stream",
        "omm_stream",
    ],
)
def test_on_ack(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_ack_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_ack(on_ack_callback)
    stream._stream._on_stream_ack(MagicMock(), {"Fields": {}})

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "defn_with_stream",
    [
        rd.delivery.rdp_stream.Definition("", [], [], {}, "test.api"),
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
        rd.content.ipa.financial_contracts.cap_floor.Definition("universe"),
        rd.content.ipa.financial_contracts.cds.Definition("universe"),
        rd.content.ipa.financial_contracts.cross.Definition("universe"),
        rd.content.ipa.financial_contracts.swap.Definition("universe"),
        rd.content.ipa.financial_contracts.option.Definition(),
        rd.content.ipa.financial_contracts.repo.Definition(),
        rd.content.ipa.financial_contracts.swaption.Definition(),
        rd.content.ipa.financial_contracts.term_deposit.Definition(),
    ],
    ids=[
        "rdp_stream",
        "financial_contracts.bond",
        "financial_contracts.cap_floor",
        "financial_contracts.cds",
        "financial_contracts.cross",
        "financial_contracts.swap",
        "financial_contracts.option",
        "financial_contracts.repo",
        "financial_contracts.swaption",
        "financial_contracts.term_deposit",
    ],
)
def test_on_response(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_response_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_response(on_response_callback)
    stream._stream._on_stream_response(MagicMock(), {"Fields": {}})

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "defn_with_stream",
    [
        rd.delivery.rdp_stream.Definition("", [], [], {}, "test.api"),
    ],
    ids=[
        "rdp_stream",
    ],
)
def test_on_alarm(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_alarm_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_alarm(on_alarm_callback)
    stream._stream._on_stream_alarm(MagicMock(), {"Fields": {}})

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "defn_with_stream",
    [
        rd.content.ipa.financial_contracts.bond.Definition("universe"),
        rd.content.ipa.financial_contracts.cap_floor.Definition("universe"),
        rd.content.ipa.financial_contracts.cds.Definition("universe"),
        rd.content.ipa.financial_contracts.cross.Definition("universe"),
        rd.content.ipa.financial_contracts.swap.Definition("universe"),
        rd.content.ipa.financial_contracts.option.Definition(),
        rd.content.ipa.financial_contracts.repo.Definition(),
        rd.content.ipa.financial_contracts.swaption.Definition(),
        rd.content.ipa.financial_contracts.term_deposit.Definition(),
    ],
    ids=[
        "financial_contracts.bond",
        "financial_contracts.cap_floor",
        "financial_contracts.cds",
        "financial_contracts.cross",
        "financial_contracts.swap",
        "financial_contracts.option",
        "financial_contracts.repo",
        "financial_contracts.swaption",
        "financial_contracts.term_deposit",
    ],
)
def test_on_state(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_state_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_state(on_state_callback)
    stream._stream._on_stream_alarm(MagicMock(), {"state": {}})

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "obj_session",
    [
        desktop.Definition(app_key="foo"),
        platform.Definition(
            app_key="foo", grant=GrantPassword(username="username", password="password")
        ),
    ],
    ids=[
        "session.desktop",
        "session.platform",
    ],
)
def test_on_state_for_session(obj_session):
    # given
    session = obj_session.get_session()

    callback_called = False

    def on_state_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    session.on_state(on_state_callback)
    session._call_on_state("")

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "obj_session",
    [
        desktop.Definition(app_key="foo"),
        platform.Definition(
            app_key="foo", grant=GrantPassword(username="username", password="password")
        ),
    ],
    ids=[
        "session.desktop",
        "session.platform",
    ],
)
def test_on_event_for_session(obj_session):
    # given
    session = obj_session.get_session()

    callback_called = False

    def on_event_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    session.on_event(on_event_callback)
    session._call_on_event(EventCode.SessionConnected, "")

    # then
    assert callback_called is True


@pytest.mark.parametrize(
    "callback, input_message",
    [
        ("on_update", {"update": [{}]}),
        ("on_complete", {"state": {"message": "queueSize=0"}}),
        ("on_add", {"data": [{}]}),
        ("on_remove", {"remove": [{}]}),
        ("on_event", {"messages": [{}]}),
        ("on_state", {"state": {"test": None}}),
    ],
    ids=[
        "trade_data_service.on_update",
        "trade_data_service.on_complete",
        "trade_data_service.on_add",
        "trade_data_service.on_remove",
        "trade_data_service.on_event",
        "trade_data_service.on_state",
    ],
)
def test_callbacks_for_trade_data_service(callback, input_message):
    # given
    session = StubSession(is_open=True)
    defn_with_stream = trade_data_service.Definition()
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def _callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    getattr(stream, callback)(_callback)
    stream._stream._do_on_update(MagicMock(), input_message)

    # then
    assert callback_called is True


def test_on_update_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_update(on_callback)
    stream._stream.dispatch_update(...)

    # then
    assert callback_called is True


def test_on_add_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_add(on_callback)
    stream._stream.dispatch_add(..., ...)

    # then
    assert callback_called is True


def test_on_complete_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_complete(on_callback)
    stream._stream.dispatch_complete(...)

    # then
    assert callback_called is True


def test_on_remove_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_remove(on_callback)
    stream._stream.dispatch_remove(..., ...)

    # then
    assert callback_called is True


def test_on_error_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    callback_called = False

    def on_callback(*args, **kwargs):
        nonlocal callback_called
        callback_called = True

    # when
    stream.on_error(on_callback)
    stream._stream.dispatch_error(...)

    # then
    assert callback_called is True
