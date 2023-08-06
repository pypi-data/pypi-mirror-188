import pytest

from refinitiv.data.content.pricing._stream_facade import Stream
from refinitiv.data import OpenState
from tests.unit.conftest import StubSession


def test_pricing_stream_raise_error_if_no_session():
    # then
    with pytest.raises(AttributeError):
        # when
        stream = Stream()


def test_pricing_stream_raise_error_if_bad_universe():
    # given
    session = StubSession(is_open=True)
    stream = Stream(session=session, universe=[None])

    # then
    with pytest.raises(ValueError):
        # when
        stream.open()


def test_pricing_stream__repr__():
    # given
    session = StubSession(is_open=True)
    stream = Stream(session=session, universe="universe")
    hex_id = hex(id(stream))
    expected_value = f"<refinitiv.data.content.pricing.Stream object at {hex_id} {{name='universe'}}>"

    # when
    testing_value = repr(stream)

    # then
    assert testing_value == expected_value


def test_pricing_stream__iter__(pricing_stream):
    # when
    iterator = iter(pricing_stream)

    # then
    with pytest.raises(StopIteration):
        next(iterator)


def test_pricing_stream__getitem__(pricing_stream):
    # when
    testing_value = pricing_stream["item"]

    # then
    assert testing_value == {}


def test_pricing_stream__len__(pricing_stream):
    # when
    testing_value = len(pricing_stream)

    # then
    assert testing_value == 0


def test_pricing_stream_close(pricing_stream):
    # when
    state = pricing_stream.close()

    # then
    assert state is OpenState.Closed, state


def test_pricing_stream_get_snapshot(pricing_stream):
    # when
    snapshot = pricing_stream.get_snapshot()

    # then
    assert snapshot.empty is True, snapshot


def test_pricing_stream_on_refresh(pricing_stream):
    # when
    testing_value = pricing_stream.on_refresh(lambda: None)

    # then
    assert testing_value is pricing_stream


def test_pricing_stream_on_update(pricing_stream):
    # when
    testing_value = pricing_stream.on_update(lambda: None)

    # then
    assert testing_value is pricing_stream


def test_pricing_stream_on_status(pricing_stream):
    # when
    testing_value = pricing_stream.on_status(lambda: None)

    # then
    assert testing_value is pricing_stream


def test_pricing_stream_on_complete(pricing_stream):
    # when
    testing_value = pricing_stream.on_complete(lambda: None)

    # then
    assert testing_value is pricing_stream


def test_pricing_stream_on_error(pricing_stream):
    # when
    testing_value = pricing_stream.on_error(lambda: None)

    # then
    assert testing_value is pricing_stream
