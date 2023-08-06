from refinitiv.data.eikon import StreamingPrices
from tests.unit.conftest import StubSession


def test_stream_class_name():
    # given
    expected_class_name = "PricingStream"

    session = StubSession(is_open=True)
    stream = StreamingPrices(universe=["EUR=", "GBP="], session=session)

    # when
    class_name = str(type(stream["EUR="]))
    class_name = class_name.rsplit(".", 1)[-1][:-2]

    # then
    assert class_name == expected_class_name
