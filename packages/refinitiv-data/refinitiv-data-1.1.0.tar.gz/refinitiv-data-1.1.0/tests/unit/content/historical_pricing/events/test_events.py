import copy

import pytest

from refinitiv.data.content import historical_pricing
from refinitiv.data.content.historical_pricing import events
from refinitiv.data.errors import RDError
from tests.unit.conftest import StubSession, error_user_has_no_permissions
from tests.unit.content.historical_pricing.data_for_tests import (
    DF_REQUIREMENT_TWO_INSTS_ONE_IS_BAD_WITHOUT_FIELDS,
    DF_WITH_EXTENDED_PARAMS,
)


def test_get_data_when_user_has_no_permissions():
    session = StubSession(is_open=True)
    session.http_responses = error_user_has_no_permissions()
    session.async_mode = True
    with pytest.raises(RDError):
        events.Definition("boo").get_data(session)


@pytest.mark.asyncio
async def test_get_data_async_no_exception_when_user_has_no_permissions():
    try:
        session = StubSession(is_open=True)
        session.http_responses = error_user_has_no_permissions()
        session.async_mode = True
        await events.Definition("boo").get_data_async(session)
    except Exception as e:
        assert False, str(e)
    else:
        assert True


def test_df_requirement_two_insts_one_is_bad_without_fields():
    # given
    session = StubSession(
        is_open=True, response=DF_REQUIREMENT_TWO_INSTS_ONE_IS_BAD_WITHOUT_FIELDS
    )
    expected_str = (
        "                              GBP=                                                                                                   G234BP=                                                                                      \n"
        "                        EVENT_TYPE   RTL     BID     ASK MID_PRICE DSPLY_NAME SRC_REF1 DLG_CODE1      CTBTR_1 CTB_LOC1 QUALIFIERS EVENT_TYPE   RTL   BID   ASK MID_PRICE DSPLY_NAME SRC_REF1 DLG_CODE1 CTBTR_1 CTB_LOC1 QUALIFIERS\n"
        "Timestamp                                                                                                                                                                                                                         \n"
        "2022-06-23 11:54:12.169      quote  8462  1.2219  1.2223    1.2221       <NA>     BCFX      <NA>     BARCLAYS      LON       <NA>       <NA>  <NA>  <NA>  <NA>      <NA>       <NA>     <NA>      <NA>    <NA>     <NA>       <NA>\n"
        "2022-06-23 11:54:12.619      quote  8526   1.222  1.2225   1.22225       <NA>     RAB1      RABX  RABOBANKGFM      LON       <NA>       <NA>  <NA>  <NA>  <NA>      <NA>       <NA>     <NA>      <NA>    <NA>     <NA>       <NA>\n"
        "2022-06-23 11:54:12.757      quote  8590  1.2219  1.2224   1.22215       <NA>     NBJX      NBJJ  NEDBANK LTD      JHB       <NA>       <NA>  <NA>  <NA>  <NA>      <NA>       <NA>     <NA>      <NA>    <NA>     <NA>       <NA>"
    )
    definition = historical_pricing.events.Definition(
        universe=["GBP=", "G234BP="], count=3
    )
    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


def test_df_with_expected_params():
    # given
    session = StubSession(is_open=True, response=DF_WITH_EXTENDED_PARAMS)
    expected_str = (
        "                             VOD.L                                                                                          GOOG.O                                                                                                                                                    \n"
        "                        EVENT_TYPE    RTL   SEQNUM     BID BIDSIZE   ASK  ASKSIZE MID_PRICE IMB_SH IMB_SIDE  QUALIFIERS EVENT_TYPE    RTL     BID BIDSIZE BID_MMID1     ASK ASKSIZE ASK_MMID1 MID_PRICE UPLIMIT LOLIMIT LIMIT_INDQ SH_SAL_RES                               QUALIFIERS\n"
        "Timestamp                                                                                                                                                                                                                                                                             \n"
        "2022-07-19 15:39:01.320      quote  50480  9075524  130.94   80476   131  2453541    130.97   <NA>     <NA>  [ASK_TONE]       <NA>   <NA>    <NA>    <NA>      <NA>    <NA>    <NA>      <NA>      <NA>    <NA>    <NA>       <NA>       <NA>                                     <NA>\n"
        "2022-07-19 15:39:38.390      quote  50496  9075694  130.94   80476   131  2503541    130.97   <NA>     <NA>  [ASK_TONE]       <NA>   <NA>    <NA>    <NA>      <NA>    <NA>    <NA>      <NA>      <NA>    <NA>    <NA>       <NA>       <NA>                                     <NA>\n"
        "2022-07-19 15:40:00.112      quote  50528  9075850  130.94   80476   131  2203541    130.97   <NA>     <NA>  [ASK_TONE]       <NA>   <NA>    <NA>    <NA>      <NA>    <NA>    <NA>      <NA>      <NA>    <NA>    <NA>       <NA>       <NA>                                     <NA>\n"
        "2022-07-19 15:40:07.641      quote  50544  9075948  130.94   80476   131  2153541    130.97   <NA>     <NA>  [ASK_TONE]       <NA>   <NA>    <NA>    <NA>      <NA>    <NA>    <NA>      <NA>      <NA>    <NA>    <NA>       <NA>       <NA>                                     <NA>\n"
        "2022-07-19 15:52:52.900      quote  50624  9076320  130.82   12365   131  2153541    130.91   <NA>     <NA>  [BID_TONE]       <NA>   <NA>    <NA>    <NA>      <NA>    <NA>    <NA>      <NA>      <NA>    <NA>    <NA>       <NA>       <NA>                                     <NA>\n"
        "2022-07-19 15:59:58.409       <NA>   <NA>     <NA>    <NA>    <NA>  <NA>     <NA>      <NA>   <NA>     <NA>        <NA>      quote  60320  113.33     200       DEX  113.35     100       MMX      <NA>  118.44  107.16        BOE          N     [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]\n"
        "2022-07-19 15:59:58.409       <NA>   <NA>     <NA>    <NA>    <NA>  <NA>     <NA>      <NA>   <NA>     <NA>        <NA>      quote  60272  113.33     200       DEX  113.36     200       NAS      <NA>  118.44  107.16        BOE          N     [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]\n"
        "2022-07-19 15:59:58.410       <NA>   <NA>     <NA>    <NA>    <NA>  <NA>     <NA>      <NA>   <NA>     <NA>        <NA>      quote  60336  113.33     200       DEX  113.35     200       NAS      <NA>  118.44  107.16        BOE          N     [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]\n"
        "2022-07-19 15:59:58.424       <NA>   <NA>     <NA>    <NA>    <NA>  <NA>     <NA>      <NA>   <NA>     <NA>        <NA>      quote  60352  113.33     200       DEX  113.35     100       MMX      <NA>  118.44  107.16        BOE          N     [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]\n"
        "2022-07-19 15:59:58.425       <NA>   <NA>     <NA>    <NA>    <NA>  <NA>     <NA>      <NA>   <NA>     <NA>        <NA>      quote  60400  113.33     200       DEX  113.35     100       NAS      <NA>  118.44  107.16        BOE          N     [PRC_QL_CD];   [PRC_QL3];A[GV1_TEXT]"
    )
    definition = historical_pricing.events.Definition(
        universe=["VOD.L", "GOOG.O"],
        eventTypes="quote",
        extended_params={
            "count": 5,
            "start": "2022-07-18T10:00:00",
            "end": "2022-07-19T16:00:00",
        },
    )
    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


def test_fields_is_not_change():
    expected_fields = ["BID"]
    testing_fields = ["BID"]
    session = StubSession(is_open=True, response=DF_WITH_EXTENDED_PARAMS)
    definition = historical_pricing.events.Definition(
        universe=["GBP=", "G234BP="], count=10, fields=testing_fields
    )
    definition.get_data(session=session)
    assert testing_fields == expected_fields
