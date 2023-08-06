import numpy

import refinitiv.data as rd
from tests.unit.conftest import StubSession


def test_snapping_zero_values_to_pd_na_in_the_pricing_stream():
    # given
    session = StubSession(is_open=True)
    field = "EURO_NETCH"
    universe = "UAH="
    stream = rd.content.pricing.Definition(universe=universe, fields=field).get_stream(
        session
    )
    stream._stream._do_open = lambda *_, **__: None
    # fmt: off
    stream._stream._stream_by_name[universe]._record = {
        'ID': 5, 'Type': 'Refresh', 'Key': {'Service': 'ELEKTRON_DD', 'Name': universe},
        'State': {'Stream': 'Open', 'Data': 'Ok'},
        'Qos': {'Timeliness': 'Realtime', 'Rate': 'JitConflated'},
        'PermData': 'AwEBV2w=', 'SeqNumber': 574, 'Fields': {field: 0.0}
    }
    # fmt: on

    # when
    stream.open()
    df = stream.get_snapshot()

    # then
    assert isinstance(df[field][0], numpy.int64)
