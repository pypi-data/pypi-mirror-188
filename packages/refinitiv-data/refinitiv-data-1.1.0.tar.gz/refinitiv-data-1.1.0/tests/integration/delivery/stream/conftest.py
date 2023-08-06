from time import sleep

from refinitiv.data import OpenState


def check_open_and_close_stream_state(stream, wait_before_close=None):
    stream.open()
    assert stream.open_state == OpenState.Opened, "Stream is not in opened state"
    if wait_before_close is not None:
        sleep(wait_before_close)
    stream.close()
    assert stream.open_state == OpenState.Closed, "Stream is not in closed state"
