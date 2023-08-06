import math
import numpy as np

import refinitiv.data as rd
from refinitiv.data import OpenState
from refinitiv.data._fin_coder_layer._intervals_consts import NON_INTRA_DAY_INTERVALS
from tests.integration.helpers import compare_list


OHLC_COLUMNS_NAMES = ["close", "high", "low", "open"]


def check_session_state(session):
    assert session.open_state == rd.OpenState.Opened, f"Session is not open"

    rd.close_session()
    assert session.open_state == rd.OpenState.Closed, f"Session is open"


def check_column_names_is_exist_in_response_and_df_not_empty(
    response, expected_fields=None
):
    assert response is not None
    assert not response.empty, f"DataFrame is empty: {response}"

    if expected_fields != [] and expected_fields is not None:
        if isinstance(expected_fields, str):
            expected_fields = [expected_fields]
        actual_fields = [col for col in response.columns]
        compare_list(list(set(actual_fields)), expected_fields)


def check_rics_fields_order_respects_and_df_not_empty(
    response, expected_universes, expected_fields
):
    actual_rics, actual_fields = [], []
    for ric, field in response.columns:
        if ric not in actual_rics:
            actual_rics.append(ric)
        if field not in actual_fields:
            actual_fields.append(field)

    assert response is not None
    assert not response.empty, f"DataFrame is empty: {response}"
    if not expected_universes == [] or not None:
        assert actual_rics == expected_universes, f"Inconsistency in the ric's order"
    if not expected_fields == [] or not None:
        assert actual_fields == expected_fields, f"Inconsistency in the field's order"


def check_stream_opened(stream):
    assert (
        stream._stream.open_state == OpenState.Opened
    ), "Stream is not in opened state."


def check_stream_closed(stream):
    assert (
        stream._stream.open_state == OpenState.Closed
    ), "Stream is not in closed state."


def check_stream_universe(stream, expected_universe):
    if isinstance(expected_universe, str):
        expected_universe = [expected_universe]

    universe_streams = stream._stream._stream._stream_by_name
    for universe in expected_universe:
        assert universe in universe_streams, f"Universe {universe} is not in stream"
        content = universe_streams[universe]
        assert content is not None, f"Data for universe {universe} is None"


def check_stream_fields(stream, universe, expected_fields):
    if isinstance(universe, str):
        universe = [universe]
    snapshot_df = stream.get_snapshot(universe, expected_fields)
    actual_fields = set(snapshot_df.columns)
    actual_fields.remove("Instrument")

    if isinstance(expected_fields, str):
        expected_fields = [expected_fields]

    if expected_fields:
        assert actual_fields == set(
            expected_fields
        ), f"{expected_fields} != {actual_fields}"

    else:
        assert actual_fields, f"{actual_fields} is empty list"


def check_stream_snapshot(stream, requested_universe, requested_fields):
    df = stream.get_snapshot(requested_universe, requested_fields)
    actual_universe = list(df["Instrument"])
    assert all(universe in actual_universe for universe in requested_universe)
    assert all(field in df for field in requested_fields)


def is_universe_exist(dataframe, expected_universe):
    universe_list = [
        column[0]
        for column in dataframe.columns.tolist()
        if "ticks count" not in column
    ]
    return list(set(universe_list)) == expected_universe


def check_df_index_names(response, interval=None):
    index_date = response.index

    if interval is not None and interval in NON_INTRA_DAY_INTERVALS:
        assert (
            index_date.name == "Date" or "date"
        ), f"Index column has the {index_date.name} name"
    else:
        assert (
            index_date.name == "Timestamp"
        ), f"Index column has the {index_date.name} name"


def check_df_recording_duration(elapsed_time, expected_duration):
    if isinstance(expected_duration, str):
        duration = expected_duration.rstrip("s")
        expected_duration = int(duration)
    assert (
        round(elapsed_time) == expected_duration
    ), f"Duration parameter {expected_duration} is not equal to actual elapsed time {elapsed_time}"


def check_df_recording_frequency(dataframe, expected_frequency):
    seconds_duration = dataframe.index.floor("S")
    difference = seconds_duration.to_series().diff()[1:]
    assert np.all(
        difference[0] == difference
    ), f"Frequency is not equal between all updates"
    assert difference[0].seconds == int(
        expected_frequency.rstrip("s")
    ), f"Actual frequency {difference[0].seconds} seconds is not equal to expected"


def check_history_for_expected_amount_of_bars(
    stream, history, frequency, duration, recorders_amount=1
):
    assert (
        history is stream.recorder._ohlc_builder.ohlc_df
    ), "There is inconsistency in recorded data with history"
    if isinstance(duration, str):
        duration = duration.rstrip("s")
        duration = int(duration)
    frequency = frequency.rstrip("s")
    frequency = int(frequency)
    count = math.ceil(duration / frequency)
    expected_amount = count * recorders_amount
    actual_amount = len(history)
    assert (
        actual_amount == expected_amount
    ), f"There is inconsistency with amount of ohlc bars, actual_amount={actual_amount}"


def check_triggered_events(callback_history, expected_universes):
    assert callback_history is not None, f"List of callbacks is empty"

    for df in callback_history:
        assert df is not None, f"Empty df is received"
        assert not df.empty, f"Empty df is received"

        universe = df.axes[0].values[0]
        assert universe in expected_universes, f"Universe is not expected in DataFrame"


def check_df_contains_ohlc_columns_and_universes(
    dataframe, expected_fields, expected_universe
):
    universe, fields, column_names = dataframe.axes[1].levels
    compare_list(column_names, OHLC_COLUMNS_NAMES)
    compare_list(fields, expected_fields)
    compare_list(universe, expected_universe)
