from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

from refinitiv.data.content import trade_data_service
from tests.unit.conftest import StubSession
import refinitiv.data as rd
from refinitiv.data._core.session import GrantPassword, EventCode
from refinitiv.data.session import platform, desktop


TEST_INPUT_ARGS = [None, "str", "", {}, 100500, {"key": "value"}, [], [1, 2, 3]]

EXPECTED_EXCEPTION = TypeError


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
def test_on_update_raise_error(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_update(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._on_stream_update(MagicMock(), {"Fields": {}})


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
def test_on_refresh_raise_error(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_refresh(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._on_stream_refresh(MagicMock(), {"Fields": {}})


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
def test_on_status_raise_error(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_status(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._on_stream_status(MagicMock(), {"Fields": {}})


@pytest.mark.skip(reason="different exception")
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
def test_on_complete_raise_error(mock_name, obj_definition):
    # given
    session = StubSession(is_open=True)
    stream = obj_definition.get_stream(session)

    mock_stream = SimpleNamespace()
    mock_stream.name = mock_name

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_complete(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._on_stream_complete(mock_stream)


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
def test_on_error_raise_error(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_error(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._on_stream_error(MagicMock(), {"Fields": {}})


@pytest.mark.skip(reason="different exception")
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
def test_on_ack_raise_error(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        print(input_arg)
        stream.on_ack(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._on_stream_ack(MagicMock(), {"Fields": {}})


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
def test_on_response_raise_error(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_response(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._on_stream_response(MagicMock(), {"Fields": {}})


@pytest.mark.parametrize(
    "defn_with_stream",
    [
        rd.delivery.rdp_stream.Definition("", [], [], {}, "test.api"),
    ],
    ids=[
        "rdp_stream",
    ],
)
def test_on_alarm_raise_error(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_alarm(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._on_stream_alarm(MagicMock(), {"Fields": {}})


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
def test_on_state_raise_error(defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_state(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._on_stream_alarm(MagicMock(), {"state": {}})


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
def test_on_state_raise_error_for_session(obj_session):
    # given
    session = obj_session.get_session()

    # when
    for input_arg in TEST_INPUT_ARGS:
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            session.on_state(input_arg)


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
def test_on_event_raise_error_for_session(obj_session):
    # given
    session = obj_session.get_session()

    # when
    for input_arg in TEST_INPUT_ARGS:
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            session.on_event(EventCode.SessionConnected, input_arg)


@pytest.mark.skip(reason="this test does not work as a general workflow")
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
def test_callbacks_raise_error_for_trade_data_service(callback, input_message):
    # given
    session = StubSession(is_open=True)
    defn_with_stream = trade_data_service.Definition()
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        getattr(stream, callback)(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream._do_on_update(MagicMock(), input_message)


def test_on_update_raise_error_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_update(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream.dispatch_update(...)


def test_on_add_raise_error_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_add(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream.dispatch_add(..., ...)


def test_on_complete_raise_error_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_complete(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream.dispatch_complete(..., ...)


def test_on_remove_raise_error_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_remove(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream.dispatch_remove(..., ...)


def test_on_error_raise_error_for_price_chain():
    # given
    session = StubSession(is_open=True)
    defn_with_stream = rd.content.pricing.chain.Definition("universe")
    stream = defn_with_stream.get_stream(session)

    # when
    for input_arg in TEST_INPUT_ARGS:
        stream.on_error(input_arg)
        # then
        with pytest.raises(expected_exception=EXPECTED_EXCEPTION):
            stream._stream.dispatch_error(...)
