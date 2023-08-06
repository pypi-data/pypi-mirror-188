import pytest

from refinitiv.data import OpenState
from refinitiv.data._core.session.event_code import EventCode
from ..conftest import create_platform_session, create_desktop_session

PLATFORM_SEQUENCE = [
    ("state", OpenState.Pending),
    ("event", EventCode.SessionAuthenticationSuccess),
    ("state", OpenState.Opened),
    ("state", OpenState.Closed),
]

DESKTOP_SEQUENCE = [
    ("state", OpenState.Pending),
    ("state", OpenState.Opened),
    ("state", OpenState.Closed),
]


@pytest.mark.parametrize(
    "session_provider, expected_sequence",
    [
        (create_platform_session, PLATFORM_SEQUENCE),
        (create_desktop_session, DESKTOP_SEQUENCE),
    ],
    ids=["platform_session", "desktop_session"],
)
def test_sessions_callbacks_sequence(session_provider, expected_sequence):
    session = session_provider()
    callbacks = []

    session.on_event(lambda *a: callbacks.append(("event", a[0])))
    session.on_state(lambda *a: callbacks.append(("state", a[0])))

    session.open()
    session.close()

    assert callbacks == expected_sequence, "Unexpected callbacks sequence"
