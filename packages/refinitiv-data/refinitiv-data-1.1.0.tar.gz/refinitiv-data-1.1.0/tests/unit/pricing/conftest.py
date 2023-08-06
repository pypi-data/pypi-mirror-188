import pytest

from refinitiv.data.content.pricing._stream_facade import Stream
from tests.unit.conftest import StubSession


@pytest.fixture(scope="function")
def pricing_stream():
    session = StubSession(is_open=True)
    pricing_stream = Stream(session=session)
    return pricing_stream
