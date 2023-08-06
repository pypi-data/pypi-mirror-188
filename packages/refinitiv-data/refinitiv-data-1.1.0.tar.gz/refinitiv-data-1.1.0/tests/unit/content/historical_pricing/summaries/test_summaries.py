from refinitiv.data.content import historical_pricing
from refinitiv.data.content._intervals import Intervals
from refinitiv.data.content.historical_pricing import MarketSession
from tests.unit.conftest import StubSession
from tests.unit.content.historical_pricing.data_for_tests import (
    DF_WITHOUT_NAN_RESPONSES,
    DF_REQUIREMENT_TWO_INSTS_ONE_FIELD,
)


def test_df_without_nan():
    # given
    session = StubSession(is_open=True, response=DF_WITHOUT_NAN_RESPONSES)
    expected_str = (
        "                       AMD.O                                                  IMNM.O                                          \n"
        "                    OPEN_PRC   HIGH_1    LOW_1 TRDPRC_1 NUM_MOVES ACVOL_UNS OPEN_PRC HIGH_1 LOW_1 TRDPRC_1 NUM_MOVES ACVOL_UNS\n"
        "Timestamp                                                                                                                     \n"
        "2022-05-25 19:54:00     <NA>     <NA>     <NA>     <NA>      <NA>      <NA>        3      3     3        3         1       104\n"
        "2022-05-25 19:56:00     <NA>     <NA>     <NA>     <NA>      <NA>      <NA>        3      3     3        3         2       224\n"
        "2022-05-25 19:57:00    92.55   92.575    92.44    92.54      1186    306126        3      3     3        3         1       100\n"
        "2022-05-25 19:58:00    92.53  92.5714  92.4722  92.5575      1451    339267     <NA>   <NA>  <NA>     <NA>      <NA>       100\n"
        "2022-05-25 19:59:00    92.55    92.71   92.484  92.7099      2483    619187     <NA>   <NA>  <NA>     <NA>      <NA>       231\n"
        "2022-05-25 20:00:00     92.7     92.7    92.65    92.65         2   1750467     <NA>   <NA>  <NA>     <NA>      <NA>      <NA>\n"
        "2022-05-25 20:01:00     <NA>     <NA>     <NA>     <NA>      <NA>     56358     <NA>   <NA>  <NA>     <NA>      <NA>      <NA>"
    )
    definition = historical_pricing.summaries.Definition(
        universe=["AMD.O", "IMNM.O"],
        interval=Intervals.ONE_MINUTE,
        start="2022-05-25T00:00:00",
        end="2022-05-25T23:59:10",
        count=5,
        fields=["OPEN_PRC", "HIGH_1", "LOW_1", "TRDPRC_1", "NUM_MOVES", "ACVOL_UNS"],
        sessions=[
            MarketSession.NORMAL,
        ],
    )
    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


def test_df_requirement_two_insts_one_field():
    # given
    session = StubSession(is_open=True, response=DF_REQUIREMENT_TWO_INSTS_ONE_FIELD)
    expected_str = (
        "BID           GBP=  G234BP=\n"
        "Date                       \n"
        "2022-06-09   1.249     <NA>\n"
        "2022-06-10  1.2314     <NA>\n"
        "2022-06-13  1.2134     <NA>\n"
        "2022-06-14  1.1993     <NA>\n"
        "2022-06-15  1.2178     <NA>\n"
        "2022-06-16  1.2351     <NA>\n"
        "2022-06-17  1.2224     <NA>\n"
        "2022-06-20   1.225     <NA>\n"
        "2022-06-21  1.2272     <NA>\n"
        "2022-06-22  1.2266     <NA>"
    )
    definition = historical_pricing.summaries.Definition(
        universe=["GBP=", "G234BP="], interval=Intervals.DAILY, count=10, fields=["BID"]
    )
    # when
    response = definition.get_data(session=session)
    df = response.data.df

    # then
    assert df.to_string() == expected_str


def test_fields_is_not_change():
    expected_fields = ["BID"]
    testing_fields = ["BID"]
    session = StubSession(is_open=True, response=DF_REQUIREMENT_TWO_INSTS_ONE_FIELD)
    definition = historical_pricing.summaries.Definition(
        universe=["GBP=", "G234BP="],
        interval=Intervals.DAILY,
        count=10,
        fields=testing_fields,
    )
    definition.get_data(session=session)
    assert testing_fields == expected_fields
