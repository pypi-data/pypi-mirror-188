import datetime

import pytest

from refinitiv.data._errors import RDError
from refinitiv.data.content.historical_pricing import (
    EventTypes,
    summaries,
    events,
    Intervals,
)
from tests.unit.conftest import StubSession, args
from . import data_for_bypassing_tests as td


@pytest.mark.parametrize(
    "count",
    [
        None,
        6,
        100,
    ],
)
def test_df_intra_bypassing_requests_with_dates_0(count):
    # get all data elements from server

    # given
    session = StubSession(is_open=True, response=td.INTRA_WITH_DATES_0_1)
    expected_str = (
        "AMD.O                OPEN_PRC  HIGH_1  LOW_1  TRDPRC_1  NUM_MOVES  ACVOL_UNS\n"
        "Timestamp                                                                   \n"
        "2022-05-25 23:54:00      90.7   90.77  90.68     90.74         22       4193\n"
        "2022-05-25 23:55:00     90.74   90.74  90.68      90.7         16       1525\n"
        "2022-05-25 23:56:00      90.7    90.8  90.66     90.73         19       2721\n"
        "2022-05-25 23:57:00     90.72   90.75   90.7     90.74         22       3790\n"
        "2022-05-25 23:58:00     90.74   90.75   90.7     90.72         20       1778\n"
        "2022-05-25 23:59:00     90.75   90.75   90.7      90.7         17       2289"
    )
    definition = summaries.Definition(
        universe=["AMD.O"],
        interval=Intervals.MINUTE,
        start="2022-05-25T23:54:00",
        end="2022-05-25T23:59:10",
        count=count,
        fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "NUM_MOVES", "ACVOL_UNS"],
    )
    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


def test_df_intra_bypassing_requests_with_dates_1():
    # get only 5 elements from server

    # given
    session = StubSession(is_open=True, response=td.INTRA_WITH_DATES_0_1)
    expected_str = (
        "AMD.O                OPEN_PRC  HIGH_1  LOW_1  TRDPRC_1  NUM_MOVES  ACVOL_UNS\n"
        "Timestamp                                                                   \n"
        "2022-05-25 23:55:00     90.74   90.74  90.68      90.7         16       1525\n"
        "2022-05-25 23:56:00      90.7    90.8  90.66     90.73         19       2721\n"
        "2022-05-25 23:57:00     90.72   90.75   90.7     90.74         22       3790\n"
        "2022-05-25 23:58:00     90.74   90.75   90.7     90.72         20       1778\n"
        "2022-05-25 23:59:00     90.75   90.75   90.7      90.7         17       2289"
    )
    definition = summaries.Definition(
        universe=["AMD.O"],
        interval=Intervals.MINUTE,
        start="2022-05-25T23:54:00",
        end="2022-05-25T23:59:10",
        count=5,
        fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "NUM_MOVES", "ACVOL_UNS"],
    )
    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


@pytest.mark.parametrize(
    "finished_datetime",
    [
        datetime.datetime(2022, 5, 25, 23, 56, 59),
        datetime.datetime(2022, 5, 25, 23, 57, 0),
    ],
)
def test_df_bypassing_requests_with_dates_3(finished_datetime):
    # given
    session = StubSession(is_open=True, response=td.INTRA_WITH_DATES_3)
    expected_str = (
        "AMD.O                OPEN_PRC  HIGH_1  LOW_1  TRDPRC_1  NUM_MOVES  ACVOL_UNS\n"
        "Timestamp                                                                   \n"
        "2022-05-25 23:57:00     90.72   90.75   90.7     90.74         22       3790\n"
        "2022-05-25 23:58:00     90.74   90.75   90.7     90.72         20       1778\n"
        "2022-05-25 23:59:00     90.75   90.75   90.7      90.7         17       2289"
    )

    definition = summaries.Definition(
        universe=["AMD.O"],
        interval=Intervals.MINUTE,
        start=finished_datetime,
        end="2022-05-25T23:59:10",
        fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "NUM_MOVES", "ACVOL_UNS"],
    )

    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


def test_df_bypassing_requests_with_dates_4():
    # server returns two requests first request > second request

    # given
    session = StubSession(is_open=True, response=td.INTRA_WITH_DATES_4)
    expected_str = (
        "AMD.O                OPEN_PRC  HIGH_1  LOW_1  TRDPRC_1  NUM_MOVES  ACVOL_UNS\n"
        "Timestamp                                                                   \n"
        "2022-05-25 23:54:00      90.7   90.77  90.68     90.74         22       4193\n"
        "2022-05-25 23:55:00     90.74   90.74  90.68      90.7         16       1525\n"
        "2022-05-25 23:56:00      90.7    90.8  90.66     90.73         19       2721\n"
        "2022-05-25 23:57:00     90.72   90.75   90.7     90.74         22       3790"
    )

    definition = summaries.Definition(
        universe=["AMD.O"],
        interval=Intervals.MINUTE,
        start="2022-05-25T23:54:00",
        end="2022-05-25T23:59:10",
        fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "NUM_MOVES", "ACVOL_UNS"],
    )

    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


def test_df_intra_bypassing_requests_with_count_0():
    # given
    session = StubSession(is_open=True, response=td.INTRA_WITH_COUNT_0)
    expected_str = (
        "LSEG.L                BID   ASK\n"
        "Timestamp                      \n"
        "2022-10-17 15:34:00  8312  6664\n"
        "2022-10-17 15:35:00  7312  7324\n"
        "2022-10-17 15:40:00  7312  7328\n"
        "2022-10-17 16:30:00  6872  9000\n"
        "2022-10-18 04:00:00  6872  9000"
    )

    definition = summaries.Definition(
        universe=["LSEG.L"],
        interval=Intervals.MINUTE,
        start="10-17-2022T14:30:50",
        count=5,
        fields=["BID", "ASK"],
    )

    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


async def test_df_intra_bypassing_requests_async_with_count():
    # given
    session = StubSession(is_open=True, response=td.INTRA_WITH_COUNT_0)
    expected_str = (
        "LSEG.L                BID   ASK\n"
        "Timestamp                      \n"
        "2022-10-17 15:34:00  8312  6664\n"
        "2022-10-17 15:35:00  7312  7324\n"
        "2022-10-17 15:40:00  7312  7328\n"
        "2022-10-17 16:30:00  6872  9000\n"
        "2022-10-18 04:00:00  6872  9000"
    )

    definition = summaries.Definition(
        universe=["LSEG.L"],
        interval=Intervals.MINUTE,
        start="10-17-2022T14:30:50",
        count=5,
        fields=["BID", "ASK"],
    )

    # when
    response = await definition.get_data_async(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


async def test_df_intra_bypassing_requests_async_with_dates():
    # get only 5 elements from server

    # given
    session = StubSession(is_open=True, response=td.INTRA_WITH_DATES_0_1)
    expected_str = (
        "AMD.O                OPEN_PRC  HIGH_1  LOW_1  TRDPRC_1  NUM_MOVES  ACVOL_UNS\n"
        "Timestamp                                                                   \n"
        "2022-05-25 23:55:00     90.74   90.74  90.68      90.7         16       1525\n"
        "2022-05-25 23:56:00      90.7    90.8  90.66     90.73         19       2721\n"
        "2022-05-25 23:57:00     90.72   90.75   90.7     90.74         22       3790\n"
        "2022-05-25 23:58:00     90.74   90.75   90.7     90.72         20       1778\n"
        "2022-05-25 23:59:00     90.75   90.75   90.7      90.7         17       2289"
    )
    definition = summaries.Definition(
        universe=["AMD.O"],
        interval=Intervals.MINUTE,
        start="2022-05-25T23:54:00",
        end="2022-05-25T23:59:10",
        count=5,
        fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "NUM_MOVES", "ACVOL_UNS"],
    )
    # when
    response = await definition.get_data_async(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


@pytest.mark.parametrize(
    "object_definition, input_kwargs, response",
    [
        # Summaries
        # one universe
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "9022-05-25T00:00:00",
                "end": "9022-05-25T23:59:10",
                "universe": ["AMD.O"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "1022-05-25T00:00:00",
                "end": "1022-05-25T23:59:10",
                "universe": ["AMD.O"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "9022-05-25T00:00:00",
                "end": "9022-05-25T23:59:10",
                "count": 1,
                "universe": ["AMD.O"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "1022-05-25T00:00:00",
                "end": "1022-05-25T23:59:10",
                "count": 1,
                "universe": ["AMD.O"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "end": "1022-05-25T23:59:10",
                "count": 1,
                "universe": ["AMD.O"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "end": "1022-05-25T23:59:10",
                "count": 1,
                "universe": ["AMD.O"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        # two universes
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "9022-05-25T00:00:00",
                "end": "9022-05-25T23:59:10",
                "universe": ["AMD.O", "VOD.L"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_TWO_UNIVERSES_EMPTY_DATA,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "1022-05-25T00:00:00",
                "end": "1022-05-25T23:59:10",
                "universe": ["AMD.O", "VOD.L"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_TWO_UNIVERSES_EMPTY_DATA,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "9022-05-25T00:00:00",
                "end": "9022-05-25T23:59:10",
                "count": 1,
                "universe": ["AMD.O", "VOD.L"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_TWO_UNIVERSES_EMPTY_DATA,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "1022-05-25T00:00:00",
                "end": "1022-05-25T23:59:10",
                "count": 1,
                "universe": ["AMD.O", "VOD.L"],
                "interval": Intervals.MINUTE,
            },
            response=td.INTRA_TWO_UNIVERSES_EMPTY_DATA,
        ),
        # Events
        # one universe
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "9022-05-25T00:00:00",
                "end": "9022-05-25T23:59:10",
                "universe": ["AMD.O"],
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "1022-05-25T00:00:00",
                "end": "1022-05-25T23:59:10",
                "universe": ["AMD.O"],
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "9022-05-25T00:00:00",
                "end": "9022-05-25T23:59:10",
                "count": 10001,
                "universe": ["AMD.O"],
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "1022-05-25T00:00:00",
                "end": "1022-05-25T23:59:10",
                "count": 10001,
                "universe": ["AMD.O"],
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "end": "1022-05-25T23:59:10",
                "count": 10001,
                "universe": ["AMD.O"],
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "end": "1022-05-25T23:59:10",
                "count": 10001,
                "universe": ["AMD.O"],
            },
            response=td.INTRA_EMPTY_DATA,
        ),
        # two universes
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "9022-05-25T00:00:00",
                "end": "9022-05-25T23:59:10",
                "universe": ["AMD.O", "VOD.L"],
            },
            response=td.INTRA_TWO_UNIVERSES_EMPTY_DATA,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "1022-05-25T00:00:00",
                "end": "1022-05-25T23:59:10",
                "universe": ["AMD.O", "VOD.L"],
            },
            response=td.INTRA_TWO_UNIVERSES_EMPTY_DATA,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "9022-05-25T00:00:00",
                "end": "9022-05-25T23:59:10",
                "count": 10001,
                "universe": ["AMD.O", "VOD.L"],
            },
            response=td.INTRA_TWO_UNIVERSES_EMPTY_DATA,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "1022-05-25T00:00:00",
                "end": "1022-05-25T23:59:10",
                "count": 10001,
                "universe": ["AMD.O", "VOD.L"],
            },
            response=td.INTRA_TWO_UNIVERSES_EMPTY_DATA,
        ),
    ],
)
def test_df_intra_server_returns_empty_data(object_definition, input_kwargs, response):
    # given
    session = StubSession(is_open=True, response=response)
    expected_str = "Empty DataFrame\n" "Columns: []\n" "Index: []"

    definition = object_definition(**input_kwargs)
    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


@pytest.mark.parametrize(
    "object_definition, input_kwargs, response",
    [
        # Summaries
        # one universe
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "2022-05-25T23:54:00",
                "end": "2022-05-25T23:59:10",
                "universe": ["LSEG.L.ffff"],
                "interval": Intervals.MINUTE,
            },
            response=td.INST_IS_BAD,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "2022-05-25T23:54:00",
                "count": 1,
                "universe": ["LSEG.L.ffff"],
                "interval": Intervals.MINUTE,
            },
            response=td.INST_IS_BAD,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "end": "2022-05-25T23:59:10",
                "count": 1,
                "universe": ["LSEG.L.ffff"],
                "interval": Intervals.MINUTE,
            },
            response=td.INST_IS_BAD,
        ),
        # two universes
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "2022-05-25T23:54:00",
                "end": "2022-05-25T23:59:10",
                "universe": ["LSEG.L.ffff", "VOD.Lffff"],
                "interval": Intervals.MINUTE,
            },
            response=td.INSTS_ARE_BAD,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "start": "2022-05-25T23:54:00",
                "count": 1,
                "universe": ["LSEG.L.ffff", "VOD.Lffff"],
                "interval": Intervals.MINUTE,
            },
            response=td.INSTS_ARE_BAD,
        ),
        args(
            object_definition=summaries.Definition,
            input_kwargs={
                "end": "2022-05-25T23:59:10",
                "count": 1,
                "universe": ["LSEG.L.ffff", "VOD.Lffff"],
                "interval": Intervals.MINUTE,
            },
            response=td.INSTS_ARE_BAD,
        ),
        # Events
        # one universe
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "2022-05-25T23:54:00",
                "end": "2022-05-25T23:59:10",
                "universe": ["LSEG.L.ffff"],
            },
            response=td.INST_IS_BAD,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "2022-05-25T23:54:00",
                "count": 10001,
                "universe": ["LSEG.L.ffff"],
            },
            response=td.INST_IS_BAD,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "end": "2022-05-25T23:59:10",
                "count": 10001,
                "universe": ["LSEG.L.ffff"],
            },
            response=td.INST_IS_BAD,
        ),
        # two universes
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "2022-05-25T23:54:00",
                "end": "2022-05-25T23:59:10",
                "universe": ["LSEG.L.ffff", "VOD.Lffff"],
            },
            response=td.INSTS_ARE_BAD,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "start": "2022-05-25T23:54:00",
                "count": 10001,
                "universe": ["LSEG.L.ffff", "VOD.Lffff"],
            },
            response=td.INSTS_ARE_BAD,
        ),
        args(
            object_definition=events.Definition,
            input_kwargs={
                "end": "2022-05-25T23:59:10",
                "count": 10001,
                "universe": ["LSEG.L.ffff", "VOD.Lffff"],
            },
            response=td.INSTS_ARE_BAD,
        ),
    ],
)
def test_df_intra_server_returns_error_data(object_definition, input_kwargs, response):
    # given
    session = StubSession(is_open=True, response=response)
    error_msg = "Error code 1 | No data to return, please check errors: ERROR: No successful response."

    definition = object_definition(**input_kwargs)

    # when
    with pytest.raises(RDError, match=error_msg):
        definition.get_data(session=session)


@pytest.mark.parametrize(
    "count",
    [
        None,
        6,
        100,
    ],
)
def test_df_events_bypassing_requests_with_dates_0(count):
    # get all data elements from server

    # given
    session = StubSession(is_open=True, response=td.EVENT_WITH_DATES_0_1)
    expected_str = (
        "GBP=                    EVENT_TYPE    RTL     BID     ASK  MID_PRICE  DSPLY_NAME SRC_REF1 DLG_CODE1       CTBTR_1 CTB_LOC1  QUALIFIERS\n"
        "Timestamp                                                                                                                             \n"
        "2022-10-18 09:17:03.269      quote  25886  1.1318  1.1321    1.13195        <NA>     COB1      CBKF   Commerzbank      FFT        <NA>\n"
        "2022-10-18 09:17:04.118      quote  25950  1.1318  1.1322      1.132        <NA>     BCFX      <NA>      BARCLAYS      LON        <NA>\n"
        "2022-10-18 09:17:04.310      quote  26014  1.1318   1.132     1.1319        <NA>     <NA>      ZKBZ   ZUERCHER KB      ZUR        <NA>\n"
        "2022-10-18 09:17:04.416      quote  26078  1.1315   1.132    1.13175        <NA>     CKLU      CKLU  StoneX Finan      LUX        <NA>\n"
        "2022-10-18 09:17:04.466      quote  26142  1.1319   1.132    1.13195        <NA>     SAHK      SAHK     SANTANDER      HKG        <NA>"
    )

    definition = events.Definition(
        universe=["GBP="],
        eventTypes=[EventTypes.TRADE, EventTypes.QUOTE],
        start="10-17-2022T00:00:00",
        end="10-18-2022T10:00:00",
        count=count,
    )

    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


def test_df_events_bypassing_requests_with_dates_1():
    # get only 3 elements

    # given
    session = StubSession(is_open=True, response=td.EVENT_WITH_DATES_0_1)
    expected_str = (
        "GBP=                    EVENT_TYPE    RTL     BID    ASK  MID_PRICE  DSPLY_NAME SRC_REF1 DLG_CODE1       CTBTR_1 CTB_LOC1  QUALIFIERS\n"
        "Timestamp                                                                                                                            \n"
        "2022-10-18 09:17:04.310      quote  26014  1.1318  1.132     1.1319        <NA>     <NA>      ZKBZ   ZUERCHER KB      ZUR        <NA>\n"
        "2022-10-18 09:17:04.416      quote  26078  1.1315  1.132    1.13175        <NA>     CKLU      CKLU  StoneX Finan      LUX        <NA>\n"
        "2022-10-18 09:17:04.466      quote  26142  1.1319  1.132    1.13195        <NA>     SAHK      SAHK     SANTANDER      HKG        <NA>"
    )

    definition = events.Definition(
        universe=["GBP="],
        eventTypes=[EventTypes.TRADE, EventTypes.QUOTE],
        start="10-17-2022T00:00:00",
        end="10-18-2022T10:00:00",
        count=3,
    )

    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


@pytest.mark.asyncio
async def test_df_events_bypassing_requests_async_with_dates():
    # get only 3 elements

    # given
    session = StubSession(is_open=True, response=td.EVENT_WITH_DATES_0_1)
    expected_str = (
        "GBP=                    EVENT_TYPE    RTL     BID    ASK  MID_PRICE  DSPLY_NAME SRC_REF1 DLG_CODE1       CTBTR_1 CTB_LOC1  QUALIFIERS\n"
        "Timestamp                                                                                                                            \n"
        "2022-10-18 09:17:04.310      quote  26014  1.1318  1.132     1.1319        <NA>     <NA>      ZKBZ   ZUERCHER KB      ZUR        <NA>\n"
        "2022-10-18 09:17:04.416      quote  26078  1.1315  1.132    1.13175        <NA>     CKLU      CKLU  StoneX Finan      LUX        <NA>\n"
        "2022-10-18 09:17:04.466      quote  26142  1.1319  1.132    1.13195        <NA>     SAHK      SAHK     SANTANDER      HKG        <NA>"
    )

    definition = events.Definition(
        universe=["GBP="],
        eventTypes=[EventTypes.TRADE, EventTypes.QUOTE],
        start="10-17-2022T00:00:00",
        end="10-18-2022T10:00:00",
        count=3,
    )

    # when
    response = await definition.get_data_async(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str
