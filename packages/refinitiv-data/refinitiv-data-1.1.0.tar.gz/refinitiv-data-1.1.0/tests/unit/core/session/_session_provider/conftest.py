import pytest

from refinitiv.data._core.session._session_type import SessionType


@pytest.fixture(scope="function", params=[SessionType.DESKTOP, SessionType.PLATFORM])
def session_type(request):
    return request.param
