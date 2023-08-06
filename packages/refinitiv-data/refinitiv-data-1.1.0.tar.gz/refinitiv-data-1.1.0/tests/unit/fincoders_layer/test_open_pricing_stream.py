from unittest.mock import patch, MagicMock

import pytest

from refinitiv.data import open_pricing_stream
from refinitiv.data._core.session import set_default
from refinitiv.data._fin_coder_layer._mixed_streams import MixedStreams
from tests.unit.conftest import StubSession


def test_session_is_close():
    # given
    error_message = "Session is not opened. Can't send any request"

    session = StubSession()
    set_default(session)

    # when
    with pytest.raises(ValueError, match=error_message):
        open_pricing_stream(...)


@patch("refinitiv.data._fin_coder_layer.get_stream.Stream")
def test_open_pricing_stream(mock_stream):
    session = StubSession(is_open=True)
    set_default(session)

    callback = lambda *args, **kwargs: print(args, kwargs)

    stream = open_pricing_stream(
        universe=["EUR=", "USD="], fields=["BID", "ASK", "OPEN_PRC"], on_data=callback
    )

    mock_stream.assert_called_once()
    attr_list = ["get_snapshot", "open", "close", "recorder"]
    for attr in attr_list:
        assert hasattr(stream, attr)


def test_mixed_streams():
    def add_to_list(_list: list, elem):
        _list.append(elem)
        return MagicMock()

    pricing = []
    custom_insts = []
    mixed_streams = MixedStreams(
        universe=["S)Test1", "Test2", "S)Test3", "S)Test4", "Test5"],
        session=StubSession(),
    )
    mixed_streams._get_pricing_stream = lambda a: add_to_list(pricing, a)
    mixed_streams._get_custom_instruments_stream = lambda a: add_to_list(
        custom_insts, a
    )
    mixed_streams._stream_by_name

    assert pricing == ["Test2", "Test5"]
    assert custom_insts == ["S)Test1", "S)Test3", "S)Test4"]
