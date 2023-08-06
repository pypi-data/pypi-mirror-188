from unittest.mock import patch

import mock
import pytest

from refinitiv.data._core.session import set_default
from refinitiv.data._errors import RDError, ScopeError
from refinitiv.data.discovery import Peers, Screener, Chain
from tests.unit.conftest import StubSession, StubResponse, send_ws_messages
from tests.unit.delivery.stream.conftest import StubWebSocketApp
from .data_for_tests import (
    BUNCH_CONSTITUENTS,
    EXPECTED_CONSTITUENTS_LIST,
    EXPECTED_SUMMARY_LIST,
)

universe = ["BT.L", "DTEGn.DE", "TEF.MC", "ORAN.PA"]
valid_adc_response = StubResponse(
    {
        "responses": [
            {
                "columnHeadersCount": 1,
                "data": [
                    ["BT.L", "BT.L"],
                    ["DTEGn.DE", "DTEGn.DE"],
                    ["TEF.MC", "TEF.MC"],
                    ["ORAN.PA", "ORAN.PA"],
                ],
                "headerOrientation": "horizontal",
                "headers": [
                    [
                        {"displayName": "Instrument"},
                        {"displayName": "RIC", "field": "TR.RIC"},
                    ]
                ],
                "rowHeadersCount": 1,
                "totalColumnsCount": 2,
                "totalRowsCount": 4,
            }
        ]
    }
)
adc_response_with_error_screen = StubResponse(
    {
        "responses": [
            {
                "columnHeadersCount": 1,
                "data": [["screen(IBM.NNN)", None]],
                "error": [
                    {
                        "code": 800,
                        "col": 1,
                        "message": "SCREEN(IBM.NNN) processing failed.",
                        "row": 0,
                    }
                ],
                "headerOrientation": "horizontal",
                "headers": [
                    [
                        {"displayName": None},
                        {"displayName": "TR.RIC", "field": "TR.RIC"},
                    ]
                ],
                "rowHeadersCount": 1,
                "totalColumnsCount": 2,
                "totalRowsCount": 2,
            }
        ]
    }
)

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

stream_data = [
    {
        "ID": 5,
        "Type": "Refresh",
        "Key": {"Service": "ELEKTRON_DD", "Name": "0#.DJI"},
        "State": {"Stream": "Open", "Data": "Ok"},
        "Qos": {"Timeliness": "Realtime", "Rate": "JitConflated"},
        "PermData": "AwEBlWnA",
        "SeqNumber": 3216,
        "Fields": {
            "PROD_PERM": 9569,
            "RDNDISPLAY": 187,
            "DSPLY_NAME": "DJ INDU AVERAGE",
            "RDN_EXCHID": "   ",
            "CURRENCY": "USD",
            "REF_COUNT": 14,
            "RECORDTYPE": 120,
            "LONGLINK1": ".DJI",
            "LONGLINK2": "AAPL.OQ",
            "LONGLINK3": "AMGN.OQ",
            "LONGLINK4": "AXP.N",
            "LONGLINK5": "BA.N",
            "LONGLINK6": "CAT.N",
            "LONGLINK7": "CRM.N",
            "LONGLINK8": "CSCO.OQ",
            "LONGLINK9": "CVX.N",
            "LONGLINK10": "DIS.N",
            "LONGLINK11": "DOW.N",
            "LONGLINK12": "GS.N",
            "LONGLINK13": "HD.N",
            "LONGLINK14": "HON.OQ",
            "LONGPREVLR": None,
            "LONGNEXTLR": None,
            "PREF_LINK": None,
            "RDN_EXCHD2": "DJI",
            "CONTEXT_ID": 2883,
            "DDS_DSO_ID": 8292,
            "SPS_SP_RIC": ".[SPSCMEIVAE1",
        },
    }
]
adc_response_with_error_peers = StubResponse(
    {
        "responses": [
            {
                "columnHeadersCount": 1,
                "data": [["peers(IBM.NNN)", None]],
                "error": [
                    {
                        "code": 413,
                        "col": 1,
                        "message": "Unable to resolve some identifier(s).",
                        "row": 0,
                    }
                ],
                "headerOrientation": "horizontal",
                "headers": [
                    [
                        {"displayName": "Instrument"},
                        {"displayName": "RIC", "field": "TR.RIC"},
                    ]
                ],
                "rowHeadersCount": 1,
                "totalColumnsCount": 2,
                "totalRowsCount": 2,
            }
        ]
    }
)
chains_response = {
    "meta": {
        "nodesLimit": "1",
        "nextLink": "",
        "prevLink": "",
        "cacheStatus": "",
    },
    "universe": {
        "ric": "0#.DJI",
        "displayName": "DJ INDU AVERAGE",
        "serviceName": "ELEKTRON_DD",
    },
    "data": {
        "constituents": [
            ".DJI",
            "AAPL.OQ",
            "AMGN.OQ",
            "AXP.N",
            "BA.N",
            "CAT.N",
            "CRM.N",
            "CSCO.OQ",
            "CVX.N",
            "DIS.N",
            "DOW.N",
            "GS.N",
            "HD.N",
            "HON.OQ",
        ]
    },
}

stream_data_with_error = [
    {
        "ID": 5,
        "Type": "Status",
        "Key": {"Service": "IDN_RDFNTS_CF", "Name": "IBM.NNN"},
        "State": {
            "Stream": "Closed",
            "Data": "Suspect",
            "Code": "NotFound",
            "Text": "The record could not be found",
        },
    }
]
constituents = [
    "AAPL.OQ",
    "AMGN.OQ",
    "AXP.N",
    "BA.N",
    "CAT.N",
    "CRM.N",
    "CSCO.OQ",
    "CVX.N",
    "DIS.N",
    "DOW.N",
    "GS.N",
    "HD.N",
    "HON.OQ",
]

summary_links = [".DJI"]


def make_http_request(adc_response=None, chain_response=None):
    def _http_request(request, *args, **kwargs):
        if request.url.endswith("streaming/pricing/v1/"):
            return StubResponse(content_data=infos)
        elif request.url == "test_get_rdp_url_root/data/datagrid/beta1/":
            return StubResponse(content_data=adc_response)
        elif request.url.startswith(
            "test_get_rdp_url_root/data/pricing/chains/v1/?universe="
        ):
            return StubResponse(content_data=chain_response)
        return StubResponse()

    return _http_request


def test_peers():
    session = StubSession(is_open=True, response=valid_adc_response)
    set_default(session)
    test_expression = "test_expr"
    peers = Peers(test_expression)
    assert peers.expression == f"peers({test_expression})"
    assert list(peers) == universe


def test_peers_exception():
    session = StubSession(is_open=True, response=adc_response_with_error_peers)
    set_default(session)
    test_expression = "test_expr"
    with pytest.raises(
        RDError,
        match="Error code 413 | Unable to resolve some identifier(s). Requested universes: peers(test_expr). Requested fields: TR.RIC",
    ):
        list(Peers(test_expression))


def test_screener():
    session = StubSession(is_open=True, response=valid_adc_response)
    set_default(session)
    test_expression = "test_expr"
    screener = Screener(test_expression)
    assert screener.expression == f"screen({test_expression})"
    assert list(screener) == universe


def test_screener_exception():
    session = StubSession(is_open=True, response=adc_response_with_error_screen)
    set_default(session)
    test_expression = "test_expr"
    with pytest.raises(
        RDError,
        match="Error code 800 | SCREEN(IBM.NNN) processing failed. Requested universes: screen(IBM.NNN). Requested fields: TR.RIC",
    ):
        list(Screener(test_expression))


@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_chain():
    session = StubSession(is_open=True, stream_auto_reconnection=True)

    session.http_request = make_http_request()
    send_ws_messages(session, stream_data)

    test_name = "Test_chain"
    result = Chain(test_name)

    assert result.constituents == constituents
    assert result.summary_links == summary_links
    assert result.name == test_name
    assert list(result) == constituents

    session.close()


adc_response = {
    "columnHeadersCount": 1,
    "data": [
        ["GS.N", "GS.N"],
        ["NKE.N", "NKE.N"],
        ["CSCO.OQ", "CSCO.OQ"],
        ["JPM.N", "JPM.N"],
        ["DIS.N", "DIS.N"],
        ["INTC.OQ", "INTC.OQ"],
        ["DOW.N", "DOW.N"],
        ["MRK.N", "MRK.N"],
        ["CVX.N", "CVX.N"],
        ["AXP.N", "AXP.N"],
        ["VZ.N", "VZ.N"],
        ["HD.N", "HD.N"],
        ["WBA.OQ", "WBA.OQ"],
        ["MCD.N", "MCD.N"],
        ["UNH.N", "UNH.N"],
        ["KO.N", "KO.N"],
        ["JNJ.N", "JNJ.N"],
        ["MSFT.OQ", "MSFT.OQ"],
        ["HON.OQ", "HON.OQ"],
        ["CRM.N", "CRM.N"],
        ["PG.N", "PG.N"],
        ["IBM.N", "IBM.N"],
        ["MMM.N", "MMM.N"],
        ["AAPL.OQ", "AAPL.OQ"],
        ["WMT.N", "WMT.N"],
        ["CAT.N", "CAT.N"],
        ["AMGN.OQ", "AMGN.OQ"],
        ["V.N", "V.N"],
        ["TRV.N", "TRV.N"],
        ["BA.N", "BA.N"],
    ],
    "headerOrientation": "horizontal",
    "headers": [
        [{"displayName": "Instrument"}, {"displayName": "RIC", "field": "TR.RIC"}]
    ],
    "rowHeadersCount": 1,
    "totalColumnsCount": 2,
    "totalRowsCount": 31,
}


@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_chain_exception():
    session = StubSession(is_open=True, stream_auto_reconnection=True)

    session.http_request = make_http_request()
    send_ws_messages(session, stream_data_with_error)

    test_name = "IBM.NNN"
    with pytest.raises(RDError, match="Error code -1 | The record could not be found"):
        list(Chain(test_name))

    session.close()


def scope_error(*args, **kwargs):
    raise ScopeError([{""}], {""}, "", "")


@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_chain_adc():
    session = StubSession(is_open=True, stream_auto_reconnection=True)
    session.config.set_param("apis.data.datagrid.underlying-platform", "rdp")

    session.http_request = make_http_request(adc_response)
    send_ws_messages(session, stream_data_with_error)

    test_name = "IBM.NNN"
    with mock.patch(
        "refinitiv.data.discovery._universe_expanders._chain.get_chain_data_from_stream",
        new=scope_error,
    ):
        assert list(Chain(test_name))

    session.close()


@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_chain_endpoint():
    session = StubSession(is_open=True, stream_auto_reconnection=True)
    session.config.set_param("apis.data.datagrid.underlying-platform", "rdp")

    session.http_request = make_http_request([], chains_response)
    send_ws_messages(session, stream_data_with_error)

    test_name = "IBM.NNN"
    with mock.patch(
        "refinitiv.data.discovery._universe_expanders._chain.get_chain_data_from_stream",
        new=scope_error,
    ):
        with mock.patch(
            "refinitiv.data.discovery._universe_expanders._chain.get_chain_data_from_adc",
            new=scope_error,
        ):
            assert list(Chain(test_name))

    session.close()


@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_chain_endpoint_with_bunch_constituents():
    session = StubSession(
        is_open=True, stream_auto_reconnection=True, response=BUNCH_CONSTITUENTS
    )
    session.config.set_param("apis.data.datagrid.underlying-platform", "rdp")

    send_ws_messages(session, stream_data_with_error)

    test_name = "0#.FCHI"
    with mock.patch(
        "refinitiv.data.discovery._universe_expanders._chain.get_chain_data_from_stream",
        new=scope_error,
    ):
        with mock.patch(
            "refinitiv.data.discovery._universe_expanders._chain.get_chain_data_from_adc",
            new=scope_error,
        ):
            testing_result = Chain(test_name)
            assert testing_result.constituents == EXPECTED_CONSTITUENTS_LIST
            assert testing_result.summary_links == EXPECTED_SUMMARY_LIST

    session.close()


@patch("websocket.WebSocketApp", new=StubWebSocketApp)
def test_chain_endpoint_error():
    response = StubResponse({}, 401)
    response.errors = [RDError(401, "Not Authorized to Chain Data")]
    session = StubSession(
        is_open=True, stream_auto_reconnection=True, response=response
    )
    session.config.set_param("apis.data.datagrid.underlying-platform", "rdp")

    send_ws_messages(session, stream_data_with_error)

    test_name = "IBM.NNN"
    with mock.patch(
        "refinitiv.data.discovery._universe_expanders._chain.get_chain_data_from_stream",
        new=scope_error,
    ):
        with mock.patch(
            "refinitiv.data.discovery._universe_expanders._chain.get_chain_data_from_adc",
            new=scope_error,
        ):
            with pytest.raises(RDError):
                list(Chain(test_name))

    session.close()
