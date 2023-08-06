from types import SimpleNamespace

import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data.content._df_build_type import DFBuildType
from refinitiv.data.content._universe_stream import _UniverseStream
from refinitiv.data.content._universe_streams import _UniverseStreams
from tests.unit.conftest import is_dunder_method, StubSession


@pytest.fixture(
    scope="function",
    params=[
        ContentType.FORWARD_CURVE,
        ContentType.ZC_CURVES,
        ContentType.ZC_CURVE_DEFINITIONS,
        ContentType.SURFACES,
        ContentType.CONTRACTS,
    ],
)
def content_type(request):
    return request.param


@pytest.fixture(
    scope="function",
    params=[
        DFBuildType.INDEX,
        DFBuildType.DATE_AS_INDEX,
    ],
)
def dfbuild_type(request):
    return request.param


@pytest.fixture(scope="function")
def session_mock():
    from refinitiv.data import _configure as configure

    session_mock_ = StubSession(config=configure.get_config())
    return session_mock_


def remove_dunder_methods(iterable):
    return [item for item in iterable if not is_dunder_method(item)]


def remove_private_attributes(iterable):
    return [item for item in iterable if not item.startswith("_")]


@pytest.fixture(scope="function")
def stream():
    session = StubSession(is_open=True, fail_if_error=True)
    streaming_price = _UniverseStream(
        content_type=ContentType.NONE, name="name", session=session
    )
    return streaming_price


@pytest.fixture(scope="function")
def streams():
    session = StubSession(is_open=True, fail_if_error=True)
    _stream = _UniverseStreams(
        content_type=ContentType.NONE, universe="name", session=session
    )
    return _stream


TIMEOUT = 0.0001


class StubDefinition:
    def __init__(self) -> None:
        ns = SimpleNamespace()
        ns._get_enum_parameter = lambda *args: []
        self.surface_parameters = ns

    def get_dict(self):
        return {}

    def get_instrument_type(self):
        return ""
