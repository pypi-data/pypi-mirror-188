import asyncio
import collections
import json
import os
import sys
from datetime import datetime, timedelta
from itertools import product
from urllib.parse import urlparse, parse_qs

import numpy as np
import pandas as pd
from pandas.core.dtypes.common import is_datetime64tz_dtype, is_datetime64_any_dtype

from refinitiv.data import _configure as configure

PROJECT_CONFIG_PATH = os.path.join(os.getcwd(), configure._default_config_file_name)


def make_write(remove, config_path):
    def write(config, filepath=None, is_remove=True, silent=False):
        is_remove and remove(filepath)
        path = filepath or config_path
        if not is_remove:
            with open(path, "r") as f:
                d = {}
                try:
                    d = json.loads(f.read())
                except Exception as e:
                    if not silent:
                        raise e

            config.update(d)
        with open(path, "w") as f:
            s = json.dumps(config)
            f.write(s)

    return write


def make_remove(config_path):
    def remove(filepath=None):
        path = filepath or config_path
        if os.path.exists(path):
            try:
                os.remove(path)
            except PermissionError:
                pass

    return remove


def create_obj_with_value_by_path(path, value):
    res = root = {}

    if isinstance(path, list):
        *keys, last = path
    elif isinstance(path, str):
        *keys, last = path.split(".")
    else:
        raise Exception(path)

    for key in keys:
        next = {}
        root[key] = next
        root = next
    root[last] = value
    return res


remove_prj_config = make_remove(PROJECT_CONFIG_PATH)
write_prj_config = make_write(remove_prj_config, PROJECT_CONFIG_PATH)


def check_response_status(
    response,
    expected_status_code,
    expected_http_reason=None,
    expected_error_message=None,
    expected_error_code=None,
):
    """
    Parameters
    ----------
    response
    expected_status_code
    expected_http_reason
    expected_error_message
    expected_error_code
    -------

    """
    status_list = response.http_status
    if isinstance(status_list, dict):
        status_list = [status_list]
    for status in status_list:
        if isinstance(status, dict):
            check_status_code_and_reason(
                status, expected_status_code, expected_http_reason
            )
        elif isinstance(status, list):
            for status_item in status:
                check_status_code_and_reason(
                    status_item, expected_status_code, expected_http_reason
                )

    if expected_error_message is not None:
        assert len(response.errors) != 0, f"Error not found"
        for error in response.errors:
            assert (
                error.message == expected_error_message
            ), f"Actual error message {error.message}"
            assert (
                error.code == expected_error_code
            ), f"{error.code} != {expected_error_code}"


def check_status_code_and_reason(status, expected_status_code, expected_http_reason):
    assert (
        status["http_status_code"] == expected_status_code
    ), f"{status['http_status_code']} != {expected_status_code}"
    assert (
        status["http_reason"] == expected_http_reason
    ), f"Actual http reason {status['http_reason']}"


def check_non_empty_response_data(response):
    assert response.data.raw, f"Empty response.data.raw received"
    assert not response.data.df.empty, f"Empty response.data.df received"


def check_empty_response_data(response):
    assert (
        not response.data.raw
    ), f"Non-empty response.data.raw received: {response.data.raw}"
    assert (
        not response.data.df
    ), f"Non-empty response.data.df received: {response.data.df}"


def check_empty_dataframe_in_response(response):
    assert (
        response.data.df.empty
    ), f"Non-empty response.data.df received: {response.data.df}"


def check_extended_params_were_sent_in_request(response, expected_extended_params=None):
    if expected_extended_params:
        if isinstance(response.request_message, list):
            request = response.request_message[0][0]
        else:
            request = response.request_message

        body = json.loads(request.content.decode("utf-8")) if request.content else ""

        if request.method == "POST":
            if isinstance(body, list):
                body = body[0]
            for key in expected_extended_params.keys():
                assert (
                    body[key] == expected_extended_params[key]
                ), f"Body does not contain extended params {expected_extended_params[key]}, actual body:{body[key]}"
        else:
            parse_result = urlparse(str(request.url))
            query_params = parse_qs(parse_result.query)

            for key in expected_extended_params.keys():
                actual_params = query_params[key][0]
                if isinstance(expected_extended_params[key], int):
                    actual_params = int(actual_params)
                assert (
                    actual_params == expected_extended_params[key]
                ), f"Query does not contain extended params {expected_extended_params[key]}, actual query:{actual_params[0]}"

            assert len(body) == 0, f"GET request contain body - {body}"


async def get_async_response_from_definition(definition_object):
    response = await definition_object.get_data_async()
    return response


async def get_async_response_from_definitions(
    definition_object_first, definition_object_second
):
    result = await asyncio.gather(
        definition_object_first.get_data_async(),
        definition_object_second.get_data_async(),
    )

    return result


def check_response_dataframe_contains_columns_names(response, expected_columns_names):
    if hasattr(response, "data"):
        dataframe = response.data.df
    else:
        dataframe = response.df
    retrieved_column_names = dataframe.columns.array
    retrieved_column_names_lowercase = list(
        map(lambda x: x.lower(), retrieved_column_names)
    )
    for column_name in expected_columns_names:
        assert column_name.lower() in retrieved_column_names_lowercase, (
            f"Expected column name '{column_name}' is not found in list of columns retrieved from dataframe: "
            f"{retrieved_column_names} "
        )


def check_response_dataframe_contains_rows_names(response, expected_rows_names):
    dataframe = response.data.df
    retrieved_rows_names = dataframe.index.array
    for row_name in expected_rows_names:
        assert (
            row_name in retrieved_rows_names
        ), f"Expected row name {row_name} is not found in list of rows retrieved from dataframe: {retrieved_rows_names}"


def check_response_dataframe_universe_date_as_index(response, expected_universe):
    if isinstance(expected_universe, list):
        column_names = response.data.df.columns
        actual_universe = {universe for universe, _ in column_names}
        assert actual_universe == set(expected_universe), (
            f"Received columns list is different from expected: "
            f"{list(actual_universe)} != {list(expected_universe)}"
        )
    else:
        assert expected_universe == response.data.df.columns.names[0]


def check_response_dataframe_columns_date_as_index(
    response, requested_universe, requested_fields
):
    if isinstance(requested_fields, str):
        requested_fields = [requested_fields]
    if isinstance(requested_universe, list):
        expected_columns_names = list(product(requested_universe, requested_fields))
    else:
        expected_columns_names = requested_fields
    expected_columns_names_lowercase = column_names_to_lowercase(expected_columns_names)
    actual_columns = response.data.df.columns
    actual_columns_names_lowercase = column_names_to_lowercase(actual_columns)

    assert set(actual_columns_names_lowercase) == set(
        expected_columns_names_lowercase
    ), (
        f"Received columns list is different from expected: "
        f"{list(actual_columns_names_lowercase)} != {list(expected_columns_names_lowercase)}"
    )


def column_names_to_lowercase(column_names):
    if isinstance(column_names[0], str):
        return map(lambda col_name: col_name.lower(), column_names)
    elif isinstance(column_names[0], tuple):
        return map(
            lambda col_name: (col_name[0].lower(), col_name[1].lower()),
            column_names,
        )
    else:
        raise TypeError(
            "column_names must contain either strings, or tuples(string, string)"
        )


def check_index_column_contains_dates(response):
    dataframe = response
    if not isinstance(response, pd.DataFrame):
        dataframe = response.data.df
    index_values = list(dataframe.index.values)
    for date in index_values:
        assert date is not pd.NaT, f"Index column contains {pd.NaT}"
        assert is_datetime64_any_dtype(date)
        assert not is_datetime64tz_dtype(date)
        # assert isinstance(date, np.datetime64)

    headers = dataframe.columns
    if dataframe.columns.nlevels == 2:
        headers = dataframe.columns.levels[1]
    assert not any(
        elem in headers for elem in ("Date", "DATE", "date")
    ), f"Duplicated column with date data in dataframe columns"


def compare_list(received_list, expected_list):
    assert collections.Counter(received_list) == collections.Counter(
        expected_list
    ), f"Received list {received_list} != expected list {expected_list}"


def check_if_dataframe_is_not_none(dataframe):
    assert not dataframe.isnull().values.all(), f"DataFrame is NaN/None"


def display_event(event, stream, event_type, triggered_events=None):
    current_time = datetime.now().time()
    if triggered_events is not None:
        triggered_events.append({event_type: event})
    print(
        ">>> Stream ID {} - {} - {} event {} received at {}".format(
            stream.id, stream.name, event_type, event, current_time
        ),
    )


def add_callbacks(stream, triggered_events=None):
    stream.on_refresh(
        lambda event, stream: display_event(event, stream, "Refresh", triggered_events)
    )
    stream.on_update(
        lambda event, stream: display_event(event, stream, "Update", triggered_events)
    )
    stream.on_status(
        lambda event, stream: display_event(event, stream, "Status", triggered_events)
    )
    stream.on_error(
        lambda event, stream: display_event(event, stream, "Error", triggered_events)
    )
    stream.on_complete(
        lambda event, stream: display_event(event, stream, "Complete", triggered_events)
    )
    return stream


def assert_error(actual_error, argument_name):
    expected_message = (
        f"__init__() missing 1 required positional argument: '{argument_name}'"
    )
    if sys.version_info >= (3, 10):
        expected_message = f"Definition.__init__() missing 1 required positional argument: '{argument_name}'"

    testing_message = str(actual_error.value)
    assert testing_message == expected_message, actual_error


def is_expected_param_in_request_url(response, expected_params):
    requests = response.request_message
    if not isinstance(response.request_message, list):
        requests = [requests]
    for universe_request in requests:
        for request_item in universe_request:
            request_params = request_item.url.params._dict
            for param in expected_params:
                assert (
                    param in request_params.keys()
                ), f"There is no '{param}' param is request url"


def convert_to_datetime(date):
    if isinstance(date, timedelta):
        converted_date = datetime.utcnow() + date
    else:
        converted_date = pd.to_datetime(date)

    return converted_date


def check_response_data_start_end_date(response, start_date, end_date, request=None):
    if not isinstance(response, pd.DataFrame):
        data_datetimes = response.data.df.index
    else:
        data_datetimes = response.index

    start_datetime = convert_to_datetime(start_date)
    end_datetime = convert_to_datetime(end_date)

    if not request.cls.pytestmark[0].args[0] == "datagrid":

        assert (
            data_datetimes[0] >= start_datetime
        ), f"Data starts {start_datetime} earlier than requested: {data_datetimes[0]}"

    assert (
        data_datetimes[-1] <= end_datetime
    ), f"Data ends later than requested: {data_datetimes[-1]}"


def is_universe_empty(dataframe, universe):
    return dataframe[universe].isnull().values.all()


def check_response_is_success(response):
    assert response.is_success


def check_response_data_universe(response, expected_universe):
    actual_universe = {
        data_object["universe"]["ric"] for data_object in response.data.raw
    }
    assert set(expected_universe) == actual_universe


def check_response_values(
    response,
    expected_universe_ric=None,
    expected_interval=None,
    expected_summary_timestamp_label=None,
):
    """

    Parameters
    ----------
    response
    expected_universe_ric
    expected_interval
    expected_summary_timestamp_label
    -------

    """
    data = response.data.raw
    try:
        if expected_universe_ric is not None:
            check_universe_in_response(response, expected_universe_ric)

        if expected_interval is not None:
            assert (
                data["interval"] == expected_interval
            ), f"{data['interval']} != {expected_interval}"

        if expected_summary_timestamp_label is not None:
            assert (
                data["summaryTimestampLabel"] == expected_summary_timestamp_label
            ), f"{data['summaryTimestampLabel']} != {expected_summary_timestamp_label}"
    except KeyError as err:
        raise AssertionError(
            f"The data returned does not have expected property: {data}."
            f" \n The error appeared: {str(err)}"
        )


def check_universe_in_response(response, expected_universe_ric):
    data: dict = response.data.raw
    if isinstance(expected_universe_ric, str):
        assert (
            data["universe"]["ric"] == expected_universe_ric
        ), f"{data['universe']['ric']} != {expected_universe_ric}"

    elif isinstance(expected_universe_ric, list):
        retrieved_universes = list(map(lambda item: item["universe"]["ric"], data))
        assert len(retrieved_universes) == len(expected_universe_ric)
        compare_list(retrieved_universes, expected_universe_ric)
    else:
        raise Exception(
            f"Unexpected type of the expected_universe_ric was provided. "
            f"{type(expected_universe_ric)}, value: {expected_universe_ric}"
        )


def check_dataframe_column_date_for_datetime_type(response):
    if hasattr(response, "data"):
        dataframe = response.data.df
    elif hasattr(response, "df"):
        dataframe = response.df
    else:
        dataframe = response
    actual_column_names = dataframe.columns.array
    for column in actual_column_names:
        if any(
            [
                i
                for i in ["Date", "date", "_DT", "DATE"]
                if i in column
            ]
        ) and all([i if not i in column else False for i in ["DateType", "Dates"]]):

            assert is_datetime64_any_dtype(
                dataframe[column]
            ), f"Column {column} has {type(dataframe[column])} dtype"
            assert not is_datetime64tz_dtype(dataframe[column])


def check_the_number_of_items_in_dataframe(universe, list_of_instruments, count):
    dict_count_of_instruments = {
        item: list_of_instruments.count(item) for item in list_of_instruments
    }
    assert (
        dict_count_of_instruments.get(universe) == count
    ), dict_count_of_instruments.get(universe)


def check_universe_order_in_df(response, expected_universe):
    dataframe = response
    if not isinstance(response, pd.DataFrame):
        dataframe = response.data.df
    if isinstance(expected_universe, list):
        actual_universes = []
        for universe, _ in dataframe.columns:
            if universe not in actual_universes:
                actual_universes.append(universe)
    else:
        actual_universes = dataframe.columns.name
    assert actual_universes == expected_universe


def check_response_value(response, column_name, expected_value):
    if isinstance(expected_value, str):
        expected_value = [expected_value]
    actual_value = []
    for values in response[column_name]:
        actual_value.append(values)

    compare_list(list(set(actual_value)), expected_value)


def check_contrib_response(request, response, event_list, message):
    assert isinstance(event_list[0], dict)
    assert event_list[0]["Text"] == message, f"Actual message: {event_list[0]['Text']}"

    if "negative_case" in request.node.callspec.id:
        assert response.error == message, f"Actual error: {event_list[0]['Text']}"
    else:
        assert (
            response.nak_message == message
        ), f"Actual nak_message: {event_list[0]['Text']}"


def check_event_code(event_list, expected_events):
    event_codes = [event[0] for event in event_list]
    expected_codes = [event[0] for event in expected_events]

    compare_list(event_codes, expected_codes)


def check_event_message(event_list, expected_events):
    event_messages = []
    for event, msg in event_list:
        if isinstance(msg, dict):
            event_messages.append(msg.get("api_cfg"))
        else:
            event_messages.append(msg)

    expected_messages = []
    for event, msg in expected_events:
        if isinstance(msg, dict):
            expected_messages.append(msg.get("api_cfg"))
        else:
            expected_messages.append(msg)

    compare_list(event_messages, expected_messages)
