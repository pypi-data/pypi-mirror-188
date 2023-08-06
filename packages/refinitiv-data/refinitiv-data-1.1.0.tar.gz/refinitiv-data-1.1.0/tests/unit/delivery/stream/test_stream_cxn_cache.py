import threading
import time
from unittest.mock import patch

import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery._data._api_type import APIType
from refinitiv.data.delivery._stream._protocol_type import ProtocolType
from refinitiv.data.delivery._stream._stream_cxn_cache import (
    StreamCxnCache,
)
from refinitiv.data.delivery._stream._stream_factory import (
    StreamDetails,
)
from refinitiv.data.delivery._stream.event import StreamCxnEvent
from tests.unit.conftest import StubSession, StubResponse
from tests.unit.content.conftest import TIMEOUT
from tests.unit.delivery.stream.conftest import StubStreamConnection


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_stream_cxn_cache_doesnt_close_cxn_when_it_released():
    # given
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    session = StubSession(fail_if_error=True, response=response)
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )
    cache.get_cxn(session, details)

    # when
    cache.release(session, details)

    # then
    has_cxn = cache.has_cxn(session, details)
    assert has_cxn is True

    # teardown
    cache.close_cxns(session)


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_stream_cxn_cache_close_cxn_correct_and_thread_is_down():
    # given
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    session = StubSession(fail_if_error=True, response=response)
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )
    cxn = cache.get_cxn(session, details)

    # when
    cache.close_cxns(session)

    time.sleep(TIMEOUT)

    # then
    names = [thread.name for thread in threading.enumerate()]
    assert cxn.name not in names


def test_stream_cxn_cache_not_has_cxn():
    # given
    session = StubSession()
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )

    # when
    has_cxn = cache.has_cxn(session, details)

    # then
    assert not has_cxn


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_stream_cxn_cache_has_cxn():
    # given
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    session = StubSession(fail_if_error=True, response=response)
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )

    # when
    cache.get_cxn(session, details)

    # then
    has_cxn = cache.has_cxn(session, details)
    assert has_cxn is True

    # teardown
    cache.close_cxns(session)


def test_stream_cxn_cache_returns_empty_list_if_no_cxns():
    # given
    session = StubSession(fail_if_error=True)
    cache = StreamCxnCache()

    # when
    cxns = cache.get_cxns(session)

    # then
    assert len(cxns) == 0


def test_stream_cxn_cache_cannot_release_cxn_if_it_does_not_exists():
    # given
    session = StubSession(fail_if_error=True)
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )

    # then
    with pytest.raises(ValueError, match="because it’s not in the cache"):
        # when
        cache.release(session, details)


def test_stream_cxn_cache_cannot_delete_cxn_if_it_is_none():
    # given
    session = StubSession(fail_if_error=True)
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )

    # then
    with pytest.raises(ValueError, match="because it is empty"):
        # when
        cache.del_cxn(None, session, details)


def test_stream_cxn_cache_cannot_delete_cxn_if_it_does_not_exists():
    # given
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    session = StubSession(fail_if_error=True, response=response)
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )

    # then
    with pytest.raises(ValueError, match="because already deleted"):
        # when
        cache.del_cxn(StubStreamConnection(), session, details)


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_stream_cxn_cache_cannot_delete_cxn_if_it_is_using():
    # given
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    session = StubSession(fail_if_error=True, response=response)
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )
    cxn = cache.get_cxn(session, details)

    # then
    with pytest.raises(AssertionError, match="because it is using"):
        # when
        cache.del_cxn(cxn, session, details)

    # teardown
    cache.close_cxns(session)


def test_stream_cxn_cache_has_cxns_is_false():
    # given
    session = StubSession(fail_if_error=True)
    cache = StreamCxnCache()

    # when
    has_cxn = cache.has_cxns(session)

    # then
    assert has_cxn is False


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_stream_cxn_cache_get_cxns():
    # given
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    session = StubSession(fail_if_error=True, response=response)
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_TRADING
    )
    cache.get_cxn(session, details)
    details = StreamDetails(
        ContentType.STREAMING_CHAINS, ProtocolType.OMM, APIType.STREAMING_PRICING
    )
    cache.get_cxn(session, details)

    # when
    cxns = cache.get_cxns(session)

    # then
    assert len(cxns) == 2

    # teardown
    cache.close_cxns(session)


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_stream_cxn_cache_close_cxns():
    def on_contracts(*args):
        details = StreamDetails(
            ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
        )
        cache.release(session, details)

    def on_chains(*args):
        details = StreamDetails(
            ContentType.STREAMING_CHAINS, ProtocolType.OMM, APIType.STREAMING_PRICING
        )
        cache.release(session, details)

    # given
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    session = StubSession(fail_if_error=True, response=response)
    cache = StreamCxnCache()
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )
    cxn = cache.get_cxn(session, details)
    cxn.on(StreamCxnEvent.DISCONNECTING, on_contracts)
    details = StreamDetails(
        ContentType.STREAMING_CHAINS, ProtocolType.OMM, APIType.STREAMING_PRICING
    )
    cxn = cache.get_cxn(session, details)
    cxn.on(StreamCxnEvent.DISCONNECTING, on_chains)

    # when
    cache.close_cxns(session)

    # then
    has_cxn = cache.has_cxns(session)
    assert has_cxn is False


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_stream_cxn",
    new=StubStreamConnection,
)
def test_stream_cxn_cache_get_cxn_async_can_work_asynchronously():
    # given
    from tests.unit.delivery.stream.raw_infos import data

    response = StubResponse(data)
    session = StubSession(response=response)
    details = StreamDetails(
        ContentType.STREAMING_PRICING, ProtocolType.OMM, APIType.STREAMING_PRICING
    )
    cache = StreamCxnCache()

    # when
    try:
        for _ in range(10):
            cache.get_cxn(session, details)
    except Exception as e:
        assert False, str(e)
    else:
        assert True
    finally:
        cache.close_cxns(session)
