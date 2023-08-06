from unittest.mock import patch

import pytest
from pandas import Timestamp

from refinitiv.data._core.session import set_default
from refinitiv.data._fin_coder_layer.get_data import (
    convert_types,
    get_data,
    update_universe,
)
from refinitiv.data.delivery._data._request import Request
from refinitiv.data.discovery import Peers
from tests.unit.conftest import StubResponse, StubSession, send_ws_messages
from tests.unit.delivery.stream.conftest import StubWebSocketApp
from . import data_for_tests as td

args_names = (
    f"adc_df, pricing_df, data, expected_result,"
    f" adc_stub, pricing_stub, is_datetime_dtype, exception_expected"
)


def test_session_is_close():
    # given
    error_message = "Session is not opened. Can't send any request"

    session = StubSession()
    set_default(session)

    # when
    with pytest.raises(ValueError, match=error_message):
        get_data(...)


@pytest.mark.parametrize(
    ("raw", "_universe", "expected_result"),
    [
        (
            {
                "data": [
                    ["GOOG.O", "USD"],
                    ["GOOG.O", "USD"],
                    ["GOOG.O", "USD"],
                    ["GOOG.O", "USD"],
                    ["VOD.L", "USD"],
                    ["VOD.L", "USD"],
                    ["VOD.L", "USD"],
                    ["VOD.L", "USD"],
                    ["EUR=", None],
                ]
            },
            ["GOOG.O", "VOD.L", "EUR="],
            [
                "GOOG.O",
                "GOOG.O",
                "GOOG.O",
                "GOOG.O",
                "VOD.L",
                "VOD.L",
                "VOD.L",
                "VOD.L",
                "EUR=",
            ],
        )
    ],
)
def test_update_universe(raw, _universe, expected_result):
    # given
    # when
    result = update_universe(raw, _universe)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("column", "column_names", "expected_result"),
    [
        (
            ["GOOG.O", "USD", 297242.64071, 297242.64071, "2022-07-05T00:00:00"],
            ["Instrument", "Currency", "Revenue - Mean", "Revenue - Mean", "Date"],
            [
                "GOOG.O",
                "USD",
                297242.64071,
                297242.64071,
                Timestamp("2022-07-05 00:00:00"),
            ],
        ),
    ],
)
def test_convert_types(column, column_names, expected_result):
    # given
    # when
    result = convert_types(column, column_names)

    # then
    assert result == expected_result


infos = {
    "services": [
        {
            "port": 443,
            "location": ["ap-northeast-1a"],
            "transport": "websocket",
            "provider": "aws",
            "endpoint": "ap-northeast-1-aws-1-sm.optimized-pricing-api.refinitiv.net",
            "dataFormat": ["tr_json2"],
        },
    ]
}


def make_http_request(content_data):
    def _http_request(request: Request):
        url = request.url or ""
        if url.endswith("streaming/pricing/v1/"):
            return StubResponse(content_data=infos)
        return StubResponse(content_data=content_data)

    return _http_request


@pytest.mark.parametrize(
    (
        "params",
        "http_responses",
        "stream_data",
        "expected_result",
        "underlying_platform",
    ),
    [
        (
            td.GET_DATA_PARAMS_1,
            td.GET_DATA_RAW_RESPONSE_1,
            td.GET_DATA_STREAM_MESSAGES_1,
            td.GET_DATA_RESULT_1,
            "rdp",
        ),
        (
            td.GET_DATA_PARAMS_2,
            td.GET_DATA_RAW_RESPONSE_2,
            td.GET_DATA_STREAM_MESSAGES_2,
            td.GET_DATA_RESULT_2,
            "rdp",
        ),
        (
            td.GET_DATA_PARAMS_3,
            td.GET_DATA_RAW_RESPONSE_3,
            td.GET_DATA_STREAM_MESSAGES_3,
            td.GET_DATA_RESULT_3,
            "rdp",
        ),
        (
            td.GET_DATA_PARAMS_4,
            td.GET_DATA_RAW_RESPONSE_4,
            td.GET_DATA_STREAM_MESSAGES_4,
            td.GET_DATA_RESULT_4,
            "rdp",
        ),
        (
            td.GET_DATA_PARAMS_5,
            td.GET_DATA_RAW_RESPONSE_5,
            td.GET_DATA_STREAM_MESSAGES_5,
            td.GET_DATA_RESULT_5,
            "rdp",
        ),
        (
            td.GET_DATA_PARAMS_6,
            td.GET_DATA_RAW_RESPONSE_6,
            td.GET_DATA_STREAM_MESSAGES_6,
            td.GET_DATA_RESULT_6,
            "udf",
        ),
        (
            td.GET_DATA_PARAMS_7,
            td.GET_DATA_RAW_RESPONSE_7,
            td.GET_DATA_STREAM_MESSAGES_7,
            td.GET_DATA_RESULT_7,
            "udf",
        ),
        (
            td.GET_DATA_PARAMS_8,
            td.GET_DATA_RAW_RESPONSE_8,
            td.GET_DATA_STREAM_MESSAGES_8,
            td.GET_DATA_RESULT_8,
            "udf",
        ),
    ],
)
@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_get_data(
    http_responses, stream_data, expected_result, params, underlying_platform
):
    session = StubSession(is_open=True, stream_auto_reconnection=True)
    session.config.set_param(
        "apis.data.datagrid.underlying-platform", underlying_platform
    )
    session.http_request = make_http_request(http_responses)
    send_ws_messages(session, stream_data)

    result = get_data(**params)

    assert result.to_string() == expected_result

    session.close()


def test_get_data_session_is_not_opened():
    session = StubSession(is_open=False)
    set_default(session)
    with pytest.raises(ValueError):
        get_data(...)


@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_no_request_to_adc_if_universe_expander_and_pricing_fields():
    no_request_to_udc = True

    def check_if_no_adc_request(request: Request):
        nonlocal no_request_to_udc
        url = request.url or ""
        if url.endswith("streaming/pricing/v1/"):
            return StubResponse(content_data=infos)
        if url == "test_get_udf_url_root":
            no_request_to_udc = False
        return StubResponse()

    session = StubSession(is_open=True, stream_auto_reconnection=True)
    session.config.set_param("apis.data.datagrid.underlying-platform", "udf")
    session.http_request = check_if_no_adc_request
    send_ws_messages(session, td.GET_DATA_STREAM_MESSAGES_1)
    set_default(session)
    peers = Peers("VOD.L")
    peers._universe = ["EUR="]

    get_data(universe=peers, fields=["bid", "ask"])
    assert no_request_to_udc

    session.close()


@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_get_data_duplicate_date():
    expected_str = (
        "  Instrument  Total Revenue per Share       Date  Total Revenue per Share       Date  Revenue from Business Activities - Total     BID     ASK\n"
        "0      IBM.N                63.395314 2021-12-31                63.395314 2020-12-31                               57350000000    <NA>    <NA>\n"
        "1      IBM.N                     <NA> 2020-12-31                61.544967 2019-12-31                                      <NA>    <NA>    <NA>\n"
        "2      IBM.N                     <NA> 2019-12-31                64.642849 2018-12-31                                      <NA>    <NA>    <NA>\n"
        "3      VOD.L                 1.565839 2022-03-31                 1.565839 2021-03-31                               45580000000  106.36  106.38\n"
        "4      VOD.L                     <NA> 2021-03-31                 1.475895 2020-03-31                                      <NA>  106.36  106.38\n"
        "5      VOD.L                     <NA> 2020-03-31                 1.528584 2019-03-31                                      <NA>  106.36  106.38"
    )

    session = StubSession(is_open=True, stream_auto_reconnection=True)
    session.config.set_param("apis.data.datagrid.underlying-platform", "udf")

    session.http_request = make_http_request(td.GET_DATA_DUPLICATE_DATE_HTTP)
    set_default(session)

    send_ws_messages(session, td.GET_DATA_DUPLICATE_DATE_STREAM)

    result_df = get_data(
        universe=["IBM.N", "VOD.L"],
        fields=[
            "BID",
            "ASK",
            "TR.F.TotRevenue",
            "TR.F.TotRevPerShr",
            "TR.F.TotRevenue(SDate=-1,EDate=-3,Period=FY0,Frq=FY).date",
            "TR.F.TotRevPerShr(SDate=0,EDate=-2,Period=FY0,Frq=FY)",
            "TR.F.TotRevPerShr(SDate=0,EDate=-2,Period=FY0,Frq=FY).date",
        ],
        use_field_names_in_headers=False,
    )
    session.close()
    set_default(None)

    assert result_df.to_string() == expected_str
