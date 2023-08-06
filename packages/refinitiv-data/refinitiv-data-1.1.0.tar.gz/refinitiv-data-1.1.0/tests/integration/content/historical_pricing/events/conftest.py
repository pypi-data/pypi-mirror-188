import enum


def check_response_data_fields(response, expected_fields):
    for data_object in response.data.raw:
        actual_fields = {header["name"] for header in data_object["headers"]}
        assert set(expected_fields).issubset(
            actual_fields
        ), f"Not all requested fields are present in universe {data_object['universe']['ric']}"


def check_response_data_event_type(response, event_type):
    if isinstance(event_type, enum.Enum):
        event_type = event_type.value
    assert all(
        s == event_type for s in response.data.df["EVENT_TYPE"]
    ), f"Data contains event types that weren't requested: {list(response.data.df['EVENT_TYPE'])}"
