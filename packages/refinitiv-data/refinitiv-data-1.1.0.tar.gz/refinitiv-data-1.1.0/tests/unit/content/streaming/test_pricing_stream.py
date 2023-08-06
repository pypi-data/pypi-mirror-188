from unittest.mock import Mock

from refinitiv.data.content._universe_streams import UniverseStreamFacade


def test_stream_available_methods():
    # given
    expected_methods = [
        "close",
        "open",
        "open_async",
        "open_state",
    ]

    # when
    stream = UniverseStreamFacade(stream=Mock())

    # then
    for expected_method in expected_methods:
        assert hasattr(stream, expected_method), expected_method


def test_stream_available_attribute():
    # given
    expected_attribute = ["_stream"]

    # when
    stream = UniverseStreamFacade(...)
    attributes = list(stream.__dict__.keys())

    # then
    assert attributes == expected_attribute
