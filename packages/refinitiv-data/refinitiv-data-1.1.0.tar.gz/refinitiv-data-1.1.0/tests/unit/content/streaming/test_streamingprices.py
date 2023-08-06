from refinitiv.data.content import pricing
from tests.unit.conftest import StubSession
from .conftest import streaming_price_record_json
from ...fincoders_layer.conftest import assert_datetime_dtype_for_df


def test_incorrect_work_pricing_stream_get_snapshot_method():
    # given
    session = StubSession(is_open=True)
    definition = pricing.Definition(["GBP=", "EUR="])
    stream = definition.get_stream(session)
    streaming_price = stream._stream._stream_by_name["GBP="]
    streaming_price._record = streaming_price_record_json

    # when
    df = stream.get_snapshot("GBP=", ["BID"])

    # then
    assert not df.empty


def test_pricing_stream_get_snapshot_columns_datetime64():
    # given
    session = StubSession(is_open=True)
    definition = pricing.Definition(["GBP=", "EUR="])
    stream = definition.get_stream(session)
    streaming_price = stream._stream._stream_by_name["GBP="]
    streaming_price._record = streaming_price_record_json

    # when
    df = stream.get_snapshot("GBP=")

    # then
    assert_datetime_dtype_for_df(df)
    assert sum(i == "datetime64[ns]" for i in df.dtypes) == 32, df.select_dtypes(
        include=["datetime64"]
    ).columns


def test_stream_class_name():
    # given
    expected_class_name = "PricingStream"

    session = StubSession(is_open=True)
    definition = pricing.Definition(["GBP=", "EUR="])
    stream = definition.get_stream(session)

    # when
    class_name = str(type(stream["EUR="]))
    class_name = class_name.rsplit(".", 1)[-1][:-2]

    # then
    assert class_name == expected_class_name
