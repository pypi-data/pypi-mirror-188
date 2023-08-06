from refinitiv.data import OpenState


def test_stream_open_state_mixin(stream):
    # when
    state = stream.open_state

    # then
    assert state == OpenState.Closed
