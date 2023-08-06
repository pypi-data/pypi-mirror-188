from unittest import mock

from refinitiv.data._content_type import ContentType
from refinitiv.data.content.pricing._stream_facade import Stream, PricingStream
from tests.unit.conftest import StubSession


def test_input_attributes():
    # given
    excepted_attributes = [
        "_session",
        "_always_use_default_session",
        "_universe",
        "_fields",
        "_service",
        "_api",
        "_extended_params",
    ]

    # when
    session = StubSession(is_open=True)
    stream_ = Stream(session)
    attributes = list(stream_.__dict__.keys())

    # then
    assert attributes == excepted_attributes


def test_smoke_stream_into_stream():
    # given
    session = StubSession(is_open=True)

    with mock.patch(
        "refinitiv.data.content.pricing._stream_facade._UniverseStreams.__init__",
        return_value=None,
    ) as mock_stream:
        # when
        s = Stream(session, universe="universe")
        s._stream

        # then
        mock_stream.assert_called_once_with(
            content_type=ContentType.STREAMING_PRICING,
            item_facade_class=PricingStream,
            universe="universe",
            session=session,
            fields=None,
            service=None,
            api=None,
            extended_params=None,
        )
