from datetime import datetime, timedelta

from refinitiv.data.delivery import rdp_stream

today = datetime.utcnow()
yesterday = today - timedelta(days=1)
yesterday = yesterday.isoformat() + "Z"
today = today.isoformat() + "Z"


def get_financial_contracts_stream(extended_params=None):
    stream = rdp_stream.Definition(
        service=None,
        api="streaming.quantitative-analytics.endpoints.financial-contracts",
        universe={
                "instrumentType": "FxCross",
                "instrumentDefinition": {
                    "instrumentTag": "USDAUD",
                    "fxCrossType": "FxSpot",
                    "fxCrossCode": "USDAUD",
                },
            },
        parameters=None,
        extended_params=extended_params,
        view=[
            "InstrumentTag",
            "FxSpot_BidMidAsk",
            "ErrorCode",
            "Ccy1SpotDate",
            "Ccy2SpotDate",
        ],
    ).get_stream()
    return stream


def get_benchmark_stream(extended_params=None):
    stream = rdp_stream.Definition(
        service=None,
        api="streaming.benchmark.endpoints.resource",
        universe=["TSLA.O", "AAPL.O", "AMZN.O"],
        view=None,
        parameters={
            "calculationType": "vwap",
            "responseType": {"type": "streaming", "frequency": "tick"},
            "timeField": "exchange",
            "startTime": {"absoluteTime": yesterday},
            "endTime": {"absoluteTime": today},
        },
        extended_params=extended_params,
    ).get_stream()
    return stream


def get_trading_analytics_stream(extended_params=None):
    stream = rdp_stream.Definition(
        service=None,
        universe=[],
        view=None,
        parameters={"universeType": "RIC"},
        api="streaming.trading-analytics.endpoints.redi",
        extended_params=extended_params,
    ).get_stream()
    return stream


def add_callbacks(stream, stream_log=None):
    if stream_log is None:
        stream_log = []

    stream.on_update(
        lambda update, item_stream: on_stream_update(
            update, item_stream, "update", stream_log
        )
    )
    stream.on_ack(
        lambda ack_msg, item_stream: on_stream_update(
            ack_msg, item_stream, "ack", stream_log
        )
    )
    stream.on_alarm(
        lambda alarm_msg, item_stream: on_stream_update(
            alarm_msg, item_stream, "alarm", stream_log
        )
    )
    stream.on_response(
        lambda response, item_stream: on_stream_update(
            response, item_stream, "response", stream_log
        )
    )


def on_stream_update(event, stream, event_type, stream_log):
    stream_log.append(event_type)
    message = f"{datetime.now()}: {event_type} - {event} received at"
    print(message)


def check_stream_view(stream, expected_view):
    assert stream._view == expected_view


def check_stream_universe(stream, expected_universe):
    assert stream._universe == expected_universe
