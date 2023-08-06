from unittest.mock import patch

import refinitiv.data as rd
from refinitiv.data.delivery._stream.contrib import ContribType
from tests.unit.conftest import StubSession
from tests.unit.delivery.stream.conftest import (
    make_mock_create_offstream_contrib,
)


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_offstream_contrib",
    new=make_mock_create_offstream_contrib(),
)
def test_omm_stream_contribute_sent():
    session = StubSession(is_open=True)
    rd.session.set_default(session)

    response = rd.delivery.omm_stream.contribute(
        name="TEST",
        fields={"BID": 40.83},
        service="ATS_GLOBAL_1",
        contrib_type=ContribType.UPDATE,
    )

    assert response.is_success is True

    rd.session.set_default(None)


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_offstream_contrib",
    new=make_mock_create_offstream_contrib(),
)
async def test_omm_stream_contribute_async_sent():
    session = StubSession(is_open=True)
    rd.session.set_default(session)

    response = await rd.delivery.omm_stream.contribute_async(
        name="TEST",
        fields={"BID": 40.83},
        service="ATS_GLOBAL_1",
        contrib_type=ContribType.UPDATE,
    )

    assert response.is_success is True

    rd.session.set_default(None)


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_offstream_contrib",
    new=make_mock_create_offstream_contrib(was_send=False),
)
def test_omm_stream_contribute_not_sent():
    session = StubSession(is_open=True)
    rd.session.set_default(session)

    def on_ack_callback(ack_msg, stream):
        pass

    def on_error_callback(error_msg, stream):
        pass

    response = rd.delivery.omm_stream.contribute(
        name="TEST",
        fields={"BID": 40.83},
        service="ATS_GLOBAL_1",
        contrib_type=ContribType.UPDATE,
        on_ack=on_ack_callback,
        on_error=on_error_callback,
    )

    assert response.is_success is False

    rd.session.set_default(None)


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_offstream_contrib",
    new=make_mock_create_offstream_contrib(was_send=False),
)
async def test_omm_stream_contribute_async_not_sent():
    session = StubSession(is_open=True)
    rd.session.set_default(session)

    def on_ack_callback(ack_msg, stream):
        pass

    def on_error_callback(error_msg, stream):
        pass

    response = await rd.delivery.omm_stream.contribute_async(
        name="TEST",
        fields={"BID": 40.83},
        service="ATS_GLOBAL_1",
        contrib_type=ContribType.UPDATE,
        on_ack=on_ack_callback,
        on_error=on_error_callback,
    )

    assert response.is_success is False

    rd.session.set_default(None)


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_offstream_contrib",
    new=make_mock_create_offstream_contrib(raise_err=True),
)
def test_omm_stream_contribute_raise_error():
    session = StubSession(is_open=True)
    rd.session.set_default(session)

    def on_ack_callback(ack_msg, stream):
        pass

    def on_error_callback(error_msg, stream):
        pass

    response = rd.delivery.omm_stream.contribute(
        name="TEST",
        fields={"BID": 40.83},
        service="ATS_GLOBAL_1",
        contrib_type=ContribType.UPDATE,
        on_ack=on_ack_callback,
        on_error=on_error_callback,
    )

    assert response.is_success is False

    rd.session.set_default(None)


@patch(
    "refinitiv.data.delivery._stream._stream_factory.create_offstream_contrib",
    new=make_mock_create_offstream_contrib(raise_err=True),
)
async def test_omm_stream_contribute_async_raise_error():
    session = StubSession(is_open=True)
    rd.session.set_default(session)

    def on_ack_callback(ack_msg, stream):
        pass

    def on_error_callback(error_msg, stream):
        pass

    response = await rd.delivery.omm_stream.contribute_async(
        name="TEST",
        fields={"BID": 40.83},
        service="ATS_GLOBAL_1",
        contrib_type=ContribType.UPDATE,
        on_ack=on_ack_callback,
        on_error=on_error_callback,
    )

    assert response.is_success is False

    rd.session.set_default(None)
