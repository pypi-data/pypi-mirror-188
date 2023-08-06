import time

from refinitiv.data.content.pricing.chain._stream import StreamingChain
from tests.unit.conftest import StubSession
from ....conftest import TIMEOUT


def test_on_complete_called_once():
    on_complete_called = 0

    def called_once(*args):
        nonlocal on_complete_called
        on_complete_called += 1

    session = StubSession(is_open=True)
    streaming_chain = StreamingChain("test", session=session)
    streaming_chain.on_complete(called_once)

    streaming_chain._chain_records._on_stream_complete("")
    streaming_chain._chain_records._on_stream_complete("")
    streaming_chain._chain_records._on_stream_complete("")
    streaming_chain._on_stream_complete(streaming_chain)

    time.sleep(TIMEOUT)
    assert on_complete_called == 1


def test_streaming_chain_custom_service():
    # given
    custom_service = "TEST_SERVICE"
    session = StubSession(is_open=True)

    # when
    streaming_chain = StreamingChain("test", session=session, service=custom_service)

    # then
    assert streaming_chain._service == custom_service
    assert streaming_chain._chain_records.service == custom_service
