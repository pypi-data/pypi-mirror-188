import refinitiv.data as rd
import tests.integration.conftest as global_conftest
from tests.integration.helpers import compare_list


def open_platform_session_for_omm_stream():
    return rd.open_session(config_name=global_conftest.conf, name="platform.my-session")


def open_deployed_session_for_omm_stream():
    return rd.open_session(
        config_name=global_conftest.conf, name="platform.deployed-cipsnylab2"
    )


def on_ack(ack_msg, stream, event_list: list = None):
    if event_list is not None:
        event_list.append(ack_msg)
    print(ack_msg)


def on_error(error_msg, stream, event_list: list = None):
    if event_list is not None:
        event_list.append(error_msg)
    print(error_msg)


def check_triggered_events(triggered_events, expected_events):
    for i, event_type in enumerate(expected_events):
        event_list = list(triggered_events[i].keys())
        assert event_list[0] == event_type

    actual_event = []
    for event in triggered_events:
        for event_name, event_body in event.items():
            actual_event.append(event_name)
            if event_name == "Error":
                assert (
                    False
                ), f"Error {event_body['State']['Text']} is found in the stream"

    for event_type in expected_events:
        assert event_type in actual_event, f"Not found '{event_type}' in the stream"


def get_error_event_text_msg(triggered_events):
    for event in triggered_events:
        for event_name, event_body in event.items():
            if event_name == "Status":
                return event_body["State"]["Text"]


def check_stream_view(expected_view, triggered_events):
    if expected_view is not None:
        if isinstance(expected_view, str):
            expected_view = [expected_view]
        if expected_view != []:
            for events in triggered_events:
                for _, event in events.items():
                    received_view = list(event.get("Fields").keys())
                    compare_list(received_view, expected_view)


def check_stream_universe(expected_universe, triggered_events_list):
    for events in triggered_events_list:
        for _, event in events.items():
            assert expected_universe == event.get("Key").get("Name")


def check_extended_params(stream, extended_params, triggered_events):
    for events in triggered_events:
        for _, event in events.items():
            assert extended_params["View"] == stream._extended_params["View"]
            received_view = list(event.get("Fields").keys())
            compare_list(received_view, extended_params["View"])
