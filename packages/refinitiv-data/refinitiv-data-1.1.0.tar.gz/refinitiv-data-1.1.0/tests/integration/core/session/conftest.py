from datetime import datetime

from refinitiv.data import OpenState


def assert_session_open_state(session):
    assert session.open_state == OpenState.Opened
    session.close()
    assert session.open_state == OpenState.Closed


def on_state(state, message, session, event_list=None):
    current_time = datetime.now().time()
    print("----------------------------------------------------------")
    print(
        ">>> {} received at {} session state is {}".format(
            message, current_time, state
        )
    )
    if event_list is not None:
        event_list.append((state, message))


def on_event(event_code, message, session, event_list=None):
    current_time = datetime.now().time()
    print("----------------------------------------------------------")
    print(
        ">>> {} received at {} event code is {}".format(
            message, current_time, event_code
        )
    )
    if event_list is not None:
        event_list.append((event_code, message))
