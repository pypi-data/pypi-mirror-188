from datetime import datetime
from tests.integration.conftest import (
    get_dict_values_as_list,
)


def on_refresh(data, instrument_name, stream, triggered_events_list=None):
    current_time = datetime.now().time()
    if triggered_events_list is not None:
        triggered_events_list.append("Refresh")
    print(f"{current_time} - Refresh received for {instrument_name} : {data}")


def on_updated(data, instrument_name, stream, triggered_events_list=None):
    current_time = datetime.now().time()
    if triggered_events_list is not None:
        triggered_events_list.append("Update")
    print(f"{current_time} - Update received for {instrument_name} : {data}")


def on_status(status, instrument_name, stream, triggered_events_list=None):
    current_time = datetime.now().time()
    if triggered_events_list is not None:
        triggered_events_list.append("Status")
    print(f"{current_time} - Status received for {instrument_name} : {status}")


def on_complete(stream, triggered_events_list=None):
    current_time = datetime.now().time()
    if triggered_events_list is not None:
        triggered_events_list.append("Complete")
    print(f"{current_time} - Stream is complete. Full snapshot:")
    print(stream.get_snapshot())


def on_error(status, instrument_name, stream, triggered_events_list=None):
    current_time = datetime.now().time()
    if triggered_events_list is not None:
        triggered_events_list.append("Error")
    print(f"{current_time} - Stream {stream} - Received error : {status}")


def add_callbacks_for_universe_stream(
    stream,
    triggered_events=None,
):
    stream.on_refresh(
        lambda data, instrument_name, stream_item: on_refresh(
            data, instrument_name, stream_item, triggered_events
        )
    )
    stream.on_update(
        lambda data, instrument_name, stream_item: on_updated(
            data, instrument_name, stream_item, triggered_events
        )
    )
    stream.on_complete(lambda stream_item: on_complete(stream_item, triggered_events))
    stream.on_status(
        lambda status, instrument_name, stream_item: on_status(
            status, instrument_name, stream_item, triggered_events
        )
    )
    stream.on_error(
        lambda status, instrument_name, stream_item: on_error(
            status, instrument_name, stream_item, triggered_events
        )
    )

    return stream


def check_triggered_events(triggered_events, expected_events):
    for i, event_type in enumerate(expected_events):
        assert (
            triggered_events[i] == event_type
        ), f"Event {triggered_events[i]} is not expected in order"


def assert_stream_error(stream, expected_msg, universe):
    actual_message = stream._stream._stream_by_name[universe].status["State"]["Text"]
    assert expected_msg in actual_message, f"{actual_message}"


def check_stream_data(stream, expected_universe, expected_fields=None):
    stream.open()

    try:
        if isinstance(expected_universe, str):
            expected_universe = [expected_universe]

        if isinstance(expected_universe, list):
            stream_item = stream._stream._stream_by_name
            for universe in expected_universe:
                content_value = get_dict_values_as_list(stream_item[universe])[0]
                assert content_value is not None, f"Stream object data in None"

        if isinstance(expected_fields, list):
            if isinstance(expected_universe, str):
                expected_universe = [expected_universe]
            for universe in expected_universe:
                actual_fields = set(
                    stream.get_snapshot(
                        universe=universe, fields=expected_fields
                    ).columns
                )
                actual_fields.remove("Instrument")
                assert (
                    set(expected_fields) == actual_fields
                ), f"{expected_fields} != {actual_fields}"

        if isinstance(expected_fields, str):
            actual_fields = stream.get_snapshot(universe=expected_universe).columns
            assert (
                expected_fields in actual_fields
            ), f"{expected_fields} not in {actual_fields}"

        if expected_fields is None:
            actual_fields = stream.get_snapshot(universe=expected_universe).columns
            assert (
                "PROD_PERM" in actual_fields or "TRDPRC_1" in actual_fields
            ), f"Fields does not exist in {actual_fields}"

    except KeyError as err:
        raise AssertionError(
            f"The instrument with universe {expected_universe} does not exist",
            f" \n The error appeared: {str(err)}",
        )

    stream.close()
