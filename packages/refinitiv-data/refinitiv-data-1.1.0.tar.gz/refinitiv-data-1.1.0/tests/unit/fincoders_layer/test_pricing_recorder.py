from datetime import datetime
from unittest.mock import patch, MagicMock

import pandas as pd
import pytest

from refinitiv.data._fin_coder_layer._ohlc_builder import (
    merge_dataframes,
    create_df,
    replace_values_by_nan,
    Ticks_OHLCBuilder,
    OHLCBuilder,
)
from refinitiv.data._fin_coder_layer._pricing_recorder import PricingRecorder
from refinitiv.data._fin_coder_layer._stream_update_handler import (
    BuildDF_StreamUpdateHandler,
    CollectUpdates_StreamUpdateHandler,
)
from refinitiv.data._content_type import ContentType
from refinitiv.data.content._universe_streams import _UniverseStreams
from refinitiv.data.session import set_default
from tests.unit.conftest import StubSession

MOCKED_RECORDED_UPDATES = {
    "GBP=": [
        {
            "Type": "Update",
            "Key": {"Service": "ELEKTRON_DD", "Name": "GBP="},
            "Fields": {"BID": 1.3317, "ASK": 1.3318},
            "Timestamp": datetime(2021, 12, 16, 18, 28, 33, 109421),
        },
        {
            "Type": "Update",
            "Key": {"Service": "ELEKTRON_DD", "Name": "GBP="},
            "Fields": {"BID": 1.3317, "ASK": 1.3318},
            "Timestamp": datetime(2021, 12, 16, 18, 28, 34, 412376),
        },
    ],
    "EUR=": [
        {
            "Type": "Update",
            "Key": {"Service": "ELEKTRON_DD", "Name": "EUR="},
            "Fields": {"BID": 1.1305, "ASK": 1.1309},
            "Timestamp": datetime(2021, 12, 16, 18, 28, 34, 412376),
        },
        {
            "Type": "Update",
            "Key": {"Service": "ELEKTRON_DD", "Name": "EUR="},
            "Fields": {"BID": 1.1307, "ASK": 1.1308, "VALUE_TS3": "2010-01-01"},
            "Timestamp": datetime(2021, 12, 16, 18, 28, 34, 428335),
        },
    ],
}


@pytest.fixture(
    scope="function",
)
def recorder(request):
    session = StubSession(is_open=True)
    set_default(session)

    stream = _UniverseStreams(
        content_type=ContentType.NONE,
        session=session,
        universe=["EUR=", "GBP="],
        fields=["BID", "ASK", "OPEN_PRC"],
    )
    recorder = PricingRecorder(stream)
    yield recorder
    set_default(None)


@patch(
    "refinitiv.data.delivery._stream.StreamStateManager.is_closed",
    False,
)
def test_record_ohlc_data(recorder):
    df = pd.DataFrame()
    recorder.record(frequency="tick", ticks_per_bar="2")

    assert recorder._ohlc_builder.ohlc_df is None
    recorder._ohlc_builder.save_ohlc_data(df)
    assert recorder._ohlc_builder.ohlc_df is df


@patch("refinitiv.data.delivery._stream.StreamStateManager.is_closed", False)
@patch(
    "refinitiv.data._fin_coder_layer._pricing_recorder.NoBlocking_RecordingControl",
    return_value=MagicMock(),
)
def test_record_with_ticks(recording_control, recorder):
    recorder.record("tick")

    assert isinstance(recorder._update_handler, CollectUpdates_StreamUpdateHandler)
    recording_control.assert_called_once_with(recorder._update_handler)
    recorder._recording_control.start_recording.assert_called_once()


@patch("refinitiv.data.delivery._stream.StreamStateManager.is_closed", False)
@patch(
    "refinitiv.data._fin_coder_layer._pricing_recorder.NoBlocking_RecordingControl",
    return_value=MagicMock(),
)
def test_record_with_ticks_and_ticks_per_bar(recording_control, recorder):
    recorder.record(frequency="tick", ticks_per_bar="10")

    assert isinstance(recorder._ohlc_builder, Ticks_OHLCBuilder)
    assert isinstance(recorder._update_handler, BuildDF_StreamUpdateHandler)
    recording_control.assert_called_once_with(recorder._update_handler)
    recorder._recording_control.start_recording.assert_called_once()


@patch("refinitiv.data.delivery._stream.StreamStateManager.is_closed", False)
@patch(
    "refinitiv.data._fin_coder_layer._pricing_recorder.NoBlocking_RecordingControl",
    return_value=MagicMock(),
)
def test_record_with_ticks_and_ticks_per_bar(recording_control, recorder):
    recorder.record(frequency="tick", ticks_per_bar="10")

    assert isinstance(recorder._ohlc_builder, Ticks_OHLCBuilder)
    assert isinstance(recorder._update_handler, BuildDF_StreamUpdateHandler)
    recording_control.assert_called_once_with(recorder._update_handler)
    recorder._recording_control.start_recording.assert_called_once()


@patch("refinitiv.data.delivery._stream.StreamStateManager.is_closed", False)
@patch(
    "refinitiv.data._fin_coder_layer._pricing_recorder.Blocking_RecordingControl",
    return_value=MagicMock(),
)
def test_record_with_ticks_and_duration(recording_control, recorder):
    recorder.record(frequency="tick", duration="10s")

    assert isinstance(recorder._update_handler, CollectUpdates_StreamUpdateHandler)
    recording_control.assert_called_once_with(recorder._update_handler)
    recorder._recording_control.start_recording.assert_called_once_with(10)


@patch("refinitiv.data.delivery._stream.StreamStateManager.is_closed", False)
@patch(
    "refinitiv.data._fin_coder_layer._pricing_recorder.Blocking_RecordingControl",
    return_value=MagicMock(),
)
def test_record_with_ticks_and_duration_and_ticks_per_bar(recording_control, recorder):
    recorder.record(frequency="tick", ticks_per_bar="10", duration="15s")

    assert isinstance(recorder._update_handler, BuildDF_StreamUpdateHandler)
    recording_control.assert_called_once_with(recorder._update_handler)
    recorder._recording_control.start_recording.assert_called_once()


@patch("refinitiv.data.delivery._stream.StreamStateManager.is_closed", False)
@patch(
    "refinitiv.data._fin_coder_layer._pricing_recorder.RepeatBlocking_RecordingControl",
    return_value=MagicMock(),
)
def test_record_with_frequency_and_duration(recording_control, recorder):
    recorder.record(frequency="5s", duration="10s")

    assert isinstance(recorder._ohlc_builder, OHLCBuilder)
    assert isinstance(recorder._update_handler, CollectUpdates_StreamUpdateHandler)
    recording_control.assert_called_once_with(
        10,
        None,
        recorder._update_handler,
        recorder._ohlc_builder,
        recorder._logger,
        recorder,
    )
    recorder._recording_control.start_recording.assert_called_once()


@patch("refinitiv.data.delivery._stream.StreamStateManager.is_closed", False)
@patch(
    "refinitiv.data._fin_coder_layer._pricing_recorder.RepeatNonBlocking_RecordingControl",
    return_value=MagicMock(),
)
def test_record_with_frequency(recording_control, recorder):
    recorder.record(frequency="5s")

    assert isinstance(recorder._ohlc_builder, OHLCBuilder)
    assert isinstance(recorder._update_handler, CollectUpdates_StreamUpdateHandler)
    recording_control.assert_called_once_with(
        None,
        recorder._update_handler,
        recorder._ohlc_builder,
        recorder._logger,
        recorder,
    )
    recorder._recording_control.start_recording.assert_called_once()


@patch("refinitiv.data.delivery._stream.StreamStateManager.is_closed", False)
@patch(
    "refinitiv.data._fin_coder_layer._pricing_recorder.NoBlocking_RecordingControl",
    return_value=MagicMock(),
)
def test_stop(recording_control, recorder):
    recorder.record(frequency="tick", ticks_per_bar="10")

    recorder.stop()
    recording_control.assert_called_once()

    recorder._recording_control.stop_recording.assert_called_once()


@pytest.mark.parametrize(
    "input, parsed_value",
    [
        ("20s", 20),
        ("2m", 120),
        ("1h", 3600),
    ],
)
def test_parse_input_frequency_and_duration(recorder, input, parsed_value):
    result = recorder._parse_input_frequency_and_duration("20s")
    assert result == 20

    result = recorder._parse_input_frequency_and_duration("2min")
    assert result == 120

    result = recorder._parse_input_frequency_and_duration("1h")
    assert result == 3600


def test_parse_input_frequency_and_duration_error(recorder):
    with pytest.raises(
        ValueError,
        match="Please provide 'duration' or 'frequency' value "
        "in valid format. For example: '10s', '2min', '1h'",
    ):
        recorder._parse_input_frequency_and_duration("invalid data")


def test_merge_dataframes(recorder):
    df = merge_dataframes([pd.DataFrame(), pd.DataFrame()])

    assert "ohlc" in dir(df)
    assert df.index.name == "Timestamp"


@patch(
    "refinitiv.data.delivery._stream.StreamStateManager.is_closed",
    False,
)
def test_create_df(recorder):
    mocked_data = [[1.3319, 1.332], [1.3317, 1.3321]]
    mocked_fields = ["BID", "ASK"]
    mocked_timestamps = [
        datetime(2021, 12, 16, 18, 9, 41, 56778),
        datetime(2021, 12, 16, 18, 9, 35, 585482),
    ]
    mocked_stream_name = "EUR="
    recorder.record(frequency="tick", ticks_per_bar="2")

    df = create_df(mocked_data, mocked_timestamps, mocked_fields, mocked_stream_name)
    assert not df.empty

    df = create_df([], [], [], mocked_stream_name)
    assert df.empty


@patch(
    "refinitiv.data.delivery._stream.StreamStateManager.is_closed",
    False,
)
def test_on_update_handler(recorder):
    mocked_update = MagicMock()
    recorder.record(frequency="tick", ticks_per_bar="5")

    streaming_price_instance = recorder._stream._stream_by_name["EUR="]
    recorder._update_handler._on_update_handler(streaming_price_instance, mocked_update)

    assert mocked_update in recorder._update_handler.updates_by_stream_name["EUR="]

    recorder._update_handler._on_update_handler(streaming_price_instance, mocked_update)

    assert len(recorder._update_handler.updates_by_stream_name["EUR="]) == 2


@patch(
    "refinitiv.data.delivery._stream.StreamStateManager.is_closed",
    False,
)
def test_on_update_handler_with_ticks(recorder):
    streaming_price_eur = recorder._stream._stream_by_name["EUR="]
    streaming_price_gbp = recorder._stream._stream_by_name["GBP="]
    recorder.record(frequency="tick", ticks_per_bar="3")

    assert recorder._update_handler.counter == 0

    recorder._update_handler._on_update_handler(
        stream=streaming_price_eur, message={"Fields": {"BID": 1.3559, "ASK": 1.3561}}
    )

    assert recorder._update_handler.counter == 1

    recorder._update_handler._on_update_handler(
        streaming_price_gbp, {"Fields": {"BID": 1.3559, "ASK": 1.3561}}
    )
    assert recorder._update_handler.counter == 2


def test_validate_arguments_invalid_frequency(recorder):
    with pytest.raises(
        ValueError,
        match="Please provide 'tick' value as frequency when you are using 'ticks_per_bar' argument.",
    ):
        recorder._validate_arguments(
            frequency="2min", duration="1min", ticks_per_bar="100"
        )


def test_validate_arguments_(recorder):
    with pytest.raises(
        ValueError,
        match="Please check your arguments, 'duration' should be higher that 'frequency'.",
    ):
        recorder._validate_arguments(
            frequency="2min", duration="1min", ticks_per_bar="1"
        )


@patch(
    "refinitiv.data.delivery._stream.StreamStateManager.is_closed",
    False,
)
def test_get_history(recorder):
    recorder.record(frequency="tick", ticks_per_bar="1")

    recorder._update_handler.updates_by_stream_name = MOCKED_RECORDED_UPDATES
    df = recorder.get_history()

    assert not df.empty
    assert "ohlc" in dir(df)
    assert df.index.name == "Timestamp"


@patch(
    "refinitiv.data.delivery._stream.StreamStateManager.is_closed",
    False,
)
def test_get_ohlc_history_no_data(recorder):
    recorder.record(frequency="tick", ticks_per_bar="1")

    df = recorder.get_history()
    assert df.empty


@patch(
    "refinitiv.data.delivery._stream.StreamStateManager.is_closed",
    False,
)
def test_check_recorded_ohlc_df(recorder):
    recorder.record(frequency="tick", ticks_per_bar="3")

    recorder._ohlc_builder.ohlc_df = pd.DataFrame()

    df = recorder._check_df(recorder._ohlc_builder.ohlc_df)
    assert df is recorder._ohlc_builder.ohlc_df


def test_validate_count_argument_invalid_value(recorder):
    with pytest.raises(
        ValueError,
        match="Invalid argument. Please provide 'ticks_per_bar'"
        " in the following format: '10', '100', '500'",
    ):
        recorder._validate_count_argument("invalid value")


def test_validate_count_argument_invalid_count(recorder):
    with pytest.raises(
        ValueError, match="Invalid argument. 'ticks_per_bar' should be more then 0"
    ):
        recorder._validate_count_argument("0")


@patch(
    "refinitiv.data.delivery._stream.StreamStateManager.is_closed",
    False,
)
def test_record_with_invalid_freqency_and_valid_count(recorder):
    with pytest.raises(
        ValueError,
        match="Please provide 'tick' value as frequency when you are using 'ticks_per_bar' argument.",
    ):
        recorder.record(frequency="3s", ticks_per_bar="100")


def test_replace_values_by_nan(recorder):
    data = [[17.0, "18.9", "2010-01-01"]]
    replace_values_by_nan(data)
    assert data == [[17.0, "18.9", None]]
