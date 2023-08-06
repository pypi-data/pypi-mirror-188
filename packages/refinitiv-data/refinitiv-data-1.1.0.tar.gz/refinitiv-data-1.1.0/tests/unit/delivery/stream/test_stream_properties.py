import pytest
import refinitiv.data as rd
from tests.unit.conftest import StubSession


def test_stream_is_open_raise_error(stream):
    # then
    with pytest.raises(AttributeError, match="object has no attribute 'is_open'"):
        # when
        stream.is_open


def test_stream_is_close_raise_error(stream):
    # then
    with pytest.raises(AttributeError, match="object has no attribute 'is_close'"):
        # when
        stream.is_close


def test_stream_is_pause_raise_error(stream):
    # then
    with pytest.raises(AttributeError, match="object has no attribute 'is_pause'"):
        # when
        stream.is_pause


def test_stream_is_paused_raise_error(stream):
    # then
    with pytest.raises(AttributeError, match="object has no attribute 'is_paused'"):
        # when
        stream.is_paused


@pytest.mark.parametrize(
    "method",
    [
        "open",
        "open_async",
        "close",
    ],
)
def test_stream_has_methods(method, stream):
    # when
    has = hasattr(stream, method)
    attr = getattr(stream, method)
    has = has and callable(attr)

    # then
    assert has is True


@pytest.mark.parametrize(
    "method",
    [
        "close_async",
    ],
)
def test_stream_doesnt_have_methods(method, stream):
    # when
    not_has = not hasattr(stream, method)

    # then
    assert not_has is True


@pytest.mark.parametrize(
    "expected_repr, defn_with_stream",
    [
        (
            "<refinitiv.data.content.pricing.Stream object at",
            rd.content.pricing.Definition("universe"),
        ),
        (
            "<refinitiv.data.content.trade_data_service.Stream object at",
            rd.content.trade_data_service.Definition(),
        ),
        (
            "<refinitiv.data.delivery.rdp_stream.RDPStream object at",
            rd.delivery.rdp_stream.Definition("", [], [], {}, ""),
        ),
        (
            "<refinitiv.data.delivery.omm_stream.OMMStream object at",
            rd.delivery.omm_stream.Definition(""),
        ),
        (
            "<refinitiv.data.content.pricing.chain.Stream object at",
            rd.content.pricing.chain.Definition("universe"),
        ),
        (
            "<refinitiv.data.content.ipa.financial_contracts.Stream object at",
            rd.content.ipa.financial_contracts.bond.Definition("universe"),
        ),
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
def test_stream_repr(expected_repr, defn_with_stream):
    # given
    session = StubSession(is_open=True)
    stream = defn_with_stream.get_stream(session)

    # when
    testing_repr = repr(stream)

    # then
    assert expected_repr in testing_repr, testing_repr
