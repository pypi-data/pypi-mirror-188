import sys
from concurrent.futures import Future
import pytest

from refinitiv.data.delivery import omm_stream
from refinitiv.data.delivery._stream import _OMMStream, StreamState
from tests.unit.conftest import StubSession


def test_omm_stream_definition_fields_is_list_of_strings():
    # given
    fields = "BID"

    # when
    definition = omm_stream.Definition(name="GBP=", fields=fields)

    # then
    assert isinstance(definition._fields, list)


def test_opened_future_set_true_after_get_status_event():
    # given
    session = StubSession()
    stream = _OMMStream(1, session, "BB.TO", None, "MarketByPrice", "ELEKTRON_DD")

    stream._state = StreamState.Opening

    # when
    stream._on_stream_status({}, {})

    # then
    assert stream._opened.is_set()


def test_opened_future_does_not_set_true_after_get_refresh_event():
    # given
    session = StubSession()
    stream = _OMMStream(1, session, "BB.TO", None, "MarketByPrice", "ELEKTRON_DD")

    stream._state = StreamState.Opening

    # when
    stream._on_stream_refresh({}, {})

    # then
    assert not stream._opened.is_set()


def test_opened_future_does_not_raise_invalid_state_error():
    # given
    session = StubSession(is_open=True)
    stream = _OMMStream(1, session, "BB.TO", None, "MarketByPrice", "ELEKTRON_DD")

    # when
    # open()
    stream._state = StreamState.Opening
    stream._on_stream_status({}, {})
    stream._state = StreamState.Opened

    try:
        stream._on_stream_complete({}, {})
    except Exception as e:
        assert False, str(e)
    else:
        # then
        assert True


def test_opened_future_does_not_raise_invalid_state_error_if_stream_got_close_message():
    # given
    session = StubSession(is_open=True)
    stream = _OMMStream(1, session, "BB.TO", None, "MarketByPrice", "ELEKTRON_DD")

    # when
    # open()
    stream._state = StreamState.Opening
    close_message = {
        "ID": 6,
        "Type": "Status",
        "Key": {"Service": "IDN_RDFNTS_CF", "Name": "INVALID"},
        "State": {
            "Stream": "Closed",
            "Data": "Suspect",
            "Code": "NotFound",
            "Text": "The record could not be found",
        },
    }
    stream._on_stream_status({}, close_message)
    stream._state = StreamState.Opened

    try:
        stream._on_stream_complete({}, {})
    except Exception as e:
        assert False, str(e)
    else:
        # then
        assert True
