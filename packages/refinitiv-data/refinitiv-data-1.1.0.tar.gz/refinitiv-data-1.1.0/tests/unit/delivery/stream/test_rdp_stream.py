from refinitiv.data.delivery import rdp_stream
from refinitiv.data.delivery._stream import _RDPStream, StreamState
from tests.unit.conftest import StubSession


def test_rdp_stream_does_not_blocking_by_alarm_event():
    # given
    session = StubSession()
    rdp_stream = _RDPStream(1, session, "name", None, None, None, None)
    rdp_stream._state = StreamState.Opening

    # when
    args = {"state": {}}
    rdp_stream._do_on_stream_alarm({}, args)

    # then
    assert rdp_stream._opened.is_set()


def test_rdp_stream_doesnot_change_universe_as_dict():
    # given
    input_universe = {
        "instrumentType": "FxCross",
        "instrumentDefinition": {
            "instrumentTag": "USDAUD",
            "fxCrossType": "FxSpot",
            "fxCrossCode": "USDAUD",
        },
    }
    expected_universe = input_universe.copy()

    session = StubSession()

    # when
    definition = rdp_stream.Definition(
        service=None,
        api="streaming.quantitative-analytics.endpoints.financial-contracts",
        universe=input_universe,
        parameters=None,
        view=[
            "InstrumentTag",
            "FxSpot_BidMidAsk",
            "ErrorCode",
            "Ccy1SpotDate",
            "Ccy2SpotDate",
        ],
    )
    stream = definition.get_stream(session)

    # then
    assert definition._universe == expected_universe
    assert stream._universe == expected_universe
