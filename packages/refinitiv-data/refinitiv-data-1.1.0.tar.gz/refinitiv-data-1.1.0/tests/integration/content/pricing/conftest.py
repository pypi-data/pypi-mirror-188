from datetime import datetime

import pandas as pd
import pytest

from refinitiv.data import get_config
from refinitiv.data.delivery._data._data_provider import Response
from tests.integration.helpers import compare_list


def get_column_names_from_list(data_frame):
    df = pd.DataFrame(data_frame)
    df_list = []
    for col in df.columns:
        if col != "Instrument":
            df_list.append(col)
    return df_list


def check_df_column_contains_value(df, column_name, expected_value):
    column_values = df[column_name].tolist()

    if isinstance(expected_value, list):
        assert column_values == expected_value, f"{column_values} != {expected_value}"

    if isinstance(expected_value, str):
        for item in column_values:
            assert item == expected_value, f"{item} != {expected_value}"


def check_pricing_data(pricing_definition, expected_universe, expected_fields=None):
    df = None

    if isinstance(pricing_definition, Response):
        df = pricing_definition.data.df

    elif isinstance(pricing_definition, pd.DataFrame):
        df = pricing_definition

    actual_fields = get_column_names_from_list(df)

    if expected_fields is None:
        assert not df.empty

    elif isinstance(expected_fields, str):
        actual_fields = actual_fields[0]
        assert expected_fields == actual_fields, f"{expected_fields} != {actual_fields}"

    elif isinstance(expected_fields, list):
        compare_list(actual_fields, expected_fields)

    check_df_column_contains_value(df, "Instrument", expected_universe)


def check_item_message_and_status(universe, expected_message, pricing_stream):
    actual_message = None
    actual_item_status = None

    if isinstance(universe, str):
        actual_message = pricing_stream._stream._stream_by_name[
            universe
        ].message.replace("**", "")
        actual_item_status = str(pricing_stream._stream._stream_by_name[universe].state)

    if isinstance(universe, list):
        actual_message = pricing_stream._stream._stream_by_name[
            universe[1]
        ].message.replace("**", "")
        actual_item_status = str(
            pricing_stream._stream._stream_by_name[universe[1]].state
        )

    assert actual_message == expected_message, f"{actual_message}"
    assert (
        actual_item_status == "StreamState.Opened"
    ), f"Stream state is not closed, {actual_item_status}"


def on_event(msg, instrument_name, stream, triggered_events_list=None):
    current_time = datetime.now().time()
    if triggered_events_list is not None:
        triggered_events_list.append(msg)
    print(
        f"{current_time} - Stream {stream} - Received event : {msg} for RIC: {instrument_name}"
    )


def add_callback_for_contribution(stream, event_list):
    stream.on_ack(
        lambda status, instrument_name, stream_item: on_event(
            status, instrument_name, stream_item, event_list
        )
    )
    stream.on_error(
        lambda status, instrument_name, stream_item: on_event(
            status, instrument_name, stream_item, event_list
        )
    )

    return stream


@pytest.fixture(scope="function")
def setup_direct_url():
    config = get_config()
    config.set_param(
        "apis.streaming.pricing.endpoints.main",
        {"direct-url": "ws://10.184.8.188:15000"},
        auto_create=True,
    )
