from unittest.mock import MagicMock

import pytest

from refinitiv.data import OpenState, get_history
from refinitiv.data._config_functions import get_config
from refinitiv.data._core.session import Session, SessionType, set_default
from refinitiv.data._fin_coder_layer._containers import FieldsContainer
from refinitiv.data._fin_coder_layer.get_history import (
    INTERVALS,
    get_adc_params,
)
from refinitiv.data._tools import get_from_path
from refinitiv.data.delivery._data._request import Request
from refinitiv.data.discovery import Peers
from tests.unit.conftest import StubSession, args, StubResponse
from . import data_for_tests as td


def test_session_is_close():
    # given
    error_message = "Session is not opened. Can't send any request"

    session = StubSession()
    set_default(session)

    # when
    with pytest.raises(ValueError, match=error_message):
        get_history(...)


def test_unsupported_interval():
    session = MagicMock(spec=Session)
    session.open_state = OpenState.Opened
    set_default(session)

    with pytest.raises(ValueError):
        get_history(universe="GOOG.O", interval="boo")


@pytest.mark.parametrize(
    "fields, expected_adc, expected_hp",
    [
        args(
            fields=["BID", "ASK", "TRDPRC_1"],
            expected_adc=[],
            expected_hp=["BID", "ASK", "TRDPRC_1"],
        ),
        args(
            fields=["TR.F.NetIncAfterTax", "TR.RevenueMean"],
            expected_adc=["TR.F.NetIncAfterTax", "TR.RevenueMean"],
            expected_hp=[],
        ),
        args(
            fields=["BID", "ASK", "TR.F.NetIncAfterTax", "TR.RevenueMean", "TRDPRC_1"],
            expected_adc=["TR.F.NetIncAfterTax", "TR.RevenueMean"],
            expected_hp=["BID", "ASK", "TRDPRC_1"],
        ),
        args(
            fields=["AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum))", "ASK"],
            expected_adc=["AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum))"],
            expected_hp=["ASK"],
        ),
        args(fields=[], expected_adc=[], expected_hp=[]),
    ],
)
def test_get_adc_and_hp_fields(fields, expected_adc, expected_hp):
    fields = FieldsContainer(fields)
    assert fields.adc == expected_adc
    assert fields.hp == expected_hp


def test_count_intervals():
    assert len(INTERVALS) == 26


@pytest.mark.parametrize(
    "start, end, interval, result",
    [
        args(
            start="2021-01-01",
            end="2021-02-01",
            interval="daily",
            result={"SDate": "2021-01-01", "EDate": "2021-02-01", "FRQ": "D"},
        ),
        args(
            start="2021-05-11",
            end=None,
            interval="tick",
            result={"SDate": "2021-05-11", "FRQ": "D"},
        ),
        args(
            start=None,
            end="2021-02-01",
            interval="daily",
            result={"EDate": "2021-02-01", "FRQ": "D"},
        ),
        args(start=None, end=None, interval="1M", result={"FRQ": "M"}),
        args(
            start=None,
            end=None,
            interval=None,
            result={},
        ),
        args(
            start="2021-01-16",
            end="2021-02-01",
            interval="7D",
            result={"SDate": "2021-01-16", "EDate": "2021-02-01", "FRQ": "W"},
        ),
        args(
            start="2021-01-16",
            end="2021-02-01",
            interval="monthly",
            result={"SDate": "2021-01-16", "EDate": "2021-02-01", "FRQ": "M"},
        ),
        args(
            start="2021-01-16",
            end="2021-02-01",
            interval="3M",
            result={"SDate": "2021-01-16", "EDate": "2021-02-01", "FRQ": "CQ"},
        ),
        args(
            start="2021-01-16",
            end="2021-02-01",
            interval="6M",
            result={"SDate": "2021-01-16", "EDate": "2021-02-01", "FRQ": "CS"},
        ),
        args(
            start="2021-01-16",
            end="2021-02-01",
            interval="yearly",
            result={"SDate": "2021-01-16", "EDate": "2021-02-01", "FRQ": "CY"},
        ),
    ],
)
def test_get_adc_params(start, end, interval, result):
    assert get_adc_params(start, end, interval) == result


def test_udf_get_history_one_instrument_no_fields():
    expected_str = (
        "LSEG.L        TRDPRC_1  MKT_HIGH  MKT_LOW  ACVOL_UNS  MKT_OPEN   BID   ASK          TRNOVR_UNS        VWAP  MID_PRICE  PERATIO  ORDBK_VOL  NUM_MOVES  IND_AUCVOL  OFFBK_VOL  HIGH_1  ORDBK_VWAP  IND_AUC  OPEN_PRC  LOW_1  OFF_CLOSE  CLS_AUCVOL  OPN_AUCVOL  OPN_AUC  CLS_AUC  INT_AUC  INT_AUCVOL  EX_VOL_UNS  ALL_C_MOVE  ELG_NUMMOV  NAVALUE\n"
        "Date                                                                                                                                                                                                                                                                                                                                            \n"
        "2022-08-31      8184.4      8234     8060     648268      8204  8102  8106        5260572719.0   8114.8267       8104  50.7763     618395       5212      398190      27712    8234    8114.731     8102      8204   8060       8102      398190        3770     8204     8102     <NA>        <NA>      816294        5710        5056     <NA>\n"
        "2022-09-01      7922.0      8120     7904     399309      8052  7926  7928       3176528830.76    7955.032       7927  50.3167     378100       5453      121772      21041    8120    7953.505     7928      8052   7904       7928      121772        4371     8052     7928     <NA>        <NA>      464271        5622        5214     <NA>\n"
        "2022-09-02      8000.0      8010     7868     678603      7978  8006  8008       5404213577.17  7963.77182       8007  49.2361     389146       6002      121309     288541    8010    7954.941     8006      7978   7868       8006      121309       10480     7978     8006     <NA>        <NA>      697004        6090        5803     <NA>\n"
        "2022-09-05     7859.75      7962     7778     592614      7930  7954  7956       4683013244.54   7911.6287       7955  49.7205     309648       4132      140236     582572    7962     7917.55     7956      7930   7778       7956      140236        6933     7930     7956     <NA>        <NA>      640688        4289        3995     <NA>\n"
        "2022-09-06      7950.0      7974     7862     362104      7924  7966  7968       2874146953.91  7937.36362       7967    49.41     347868       5115      125206      13993    7974    7938.464     7968      7924   7862       7968      125206        3068     7924     7968     <NA>        <NA>      486599        5274        5019     <NA>\n"
        "2022-09-07  7897.33333      8000     7838    1050642      7918  7944  7946       8288071402.15    7888.567       7945  49.4845     412145       7695      167471     638292    8000     7934.95     7944      7918   7838       7944      167471        5849     7918     7944     <NA>        <NA>     1154149        7753        7199     <NA>\n"
        "2022-09-08      8044.0      8060     7688     611208      7964  8004  8006        4847453609.7     7930.94       8005  49.3355     587774       7217      240248      23394    8060    7932.403     8004      7964   7688       8004      240248        6609     7964     8004     <NA>        <NA>      754372        7318        7011     <NA>\n"
        "2022-09-09      8024.0      8090     7956     479583      7956  8004  8010       3848903522.51   8025.5082       8007  49.7081     381305       5416      182620      98135    8090    8021.854     8004      7956   7956       8004      182620        1606     7956     8004     <NA>        <NA>      602315        5471        5306     <NA>\n"
        "2022-09-12     8028.12      8098     7954     393139      7998  8094  8098       3165188290.65  8051.06695       8096  49.7081     374415       5142      163090      18685    8098    8053.243     8098      7998   7954       8098      163090        7468     7998     8098     <NA>        <NA>      508848        5196        4919     <NA>\n"
        "2022-09-13   8023.8095      8162     7942     534518      8134  8004  8006        4285291504.4   8016.4881       8005  50.2919     454096       6799      199046      76775    8162    8016.292     8004      8134   7942       8004      199046        5863     8134     8004     <NA>        <NA>      683751        6853        6609     <NA>\n"
        "2022-09-14      7972.1      8070     7892     521577      7962  7900  7902       4134076455.03  7925.89236       7901  49.7081     499343       6976      235608      21464    8070    7924.937     7900      7962   7892       7900      235608        3225     7962     7900     <NA>        <NA>      640027        7101        6746     <NA>\n"
        "2022-09-15  7895.55636      7908     7766     422663      7900  7800  7802       3299449612.11   7806.3314       7801  49.0622     399733       5081      232161      22606    7908    7806.016     7802      7900   7766       7802      232161        5668     7900     7802     <NA>        <NA>      507673        5324        4851     <NA>\n"
        "2022-09-16      7760.0      7824     7720    2168875      7760  7770  7786  16851819857.530001    7769.846       7778  48.4536    1015294       7430      619678    1152524    7824    7778.599     7786      7760   7720       7786      619678        3973     7760     7786     7748      103606     2577171        7929        7276     <NA>\n"
        "2022-09-19        <NA>      <NA>     <NA>       <NA>      <NA>  <NA>  <NA>                <NA>        <NA>       7778  48.3542       <NA>       <NA>        <NA>       <NA>    <NA>        <NA>     <NA>      <NA>   <NA>       <NA>        <NA>        <NA>     <NA>     <NA>     <NA>        <NA>        <NA>        <NA>        <NA>     <NA>\n"
        "2022-09-20  7763.06667      7768     7460     513033      7732  7542  7548       3878593615.79   7559.7715       7545  48.3542     473450       6890      186298      36986    7768    7559.729     7548      7732   7460       7548      186298       27764     7732     7548     <NA>        <NA>      663257        6999        6407     <NA>\n"
        "2022-09-21  7663.44985      7730     7518    1001952      7552  7728  7730     7631392654.3177   7616.5246       7729  46.8762     471364       6981      144538     530588    7730     7678.82     7728      7552   7518       7728      144538        4575     7552     7728     <NA>        <NA>     1151781        7092        6807     <NA>\n"
        "2022-09-22     7563.56      7706     7416     759195      7620  7468  7470       5729651816.67  7547.00074       7469   47.994     480791       5866      244543     278361    7706    7508.555     7468      7620   7416       7468      244543        3711     7620     7468     <NA>        <NA>      910761        6009        5666     <NA>\n"
        "2022-09-23  7461.98718      7528     7300     525502      7446  7468  7470       3914411797.42  7449.43887       7469  46.3793     495162       7688      201094      27640    7528    7449.858     7468      7446   7300       7468      201094        4947     7446     7468     <NA>        <NA>      638640        8116        7424     <NA>\n"
        "2022-09-26  7489.15237      7660     7480     627075      7494  7632  7634     4773442156.7861   7612.2345       7633  46.3793     533163       7984      192701      93912    7660    7611.826     7634      7494   7482       7634      192701        4644     7494     7634     <NA>        <NA>      677187        8209        7673     <NA>\n"
        "2022-09-27      7652.0      7694     7548     669293      7606  7622  7624    5102433530.01501   7623.6154       7623  47.4103     569638       6502      282974      99655    7694    7630.916     7622      7606   7548       7622      282974       16892     7606     7622     <NA>        <NA>      789364        6613        6164     <NA>"
    )
    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_ONE_INSTRUMENT_NO_FIELDS
    )

    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_one_adc_field():
    expected_str = (
        "LSEG.L         Revenue\n" "Date                  \n" "2021-12-31  6740000000"
    )
    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["TR.Revenue"])
    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_one_adc_field_use_field_names_in_headers():
    expected_str = (
        "LSEG.L      TR.REVENUE\n" "Date                  \n" "2021-12-31  6740000000"
    )
    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_FIELD_NAMES_IN_HEADERS,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe="LSEG.L", fields=["TR.Revenue"], use_field_names_in_headers=True
    )
    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_one_pricing_field():
    expected_str = (
        "LSEG.L       BID\n"
        "Date            \n"
        "2022-08-30  8176\n"
        "2022-08-31  8102\n"
        "2022-09-01  7926\n"
        "2022-09-02  8006\n"
        "2022-09-05  7954\n"
        "2022-09-06  7966\n"
        "2022-09-07  7944\n"
        "2022-09-08  8004\n"
        "2022-09-09  8004\n"
        "2022-09-12  8094\n"
        "2022-09-13  8004\n"
        "2022-09-14  7900\n"
        "2022-09-15  7800\n"
        "2022-09-16  7770\n"
        "2022-09-20  7542\n"
        "2022-09-21  7728\n"
        "2022-09-22  7468\n"
        "2022-09-23  7468\n"
        "2022-09-26  7632\n"
        "2022-09-27  7622"
    )

    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_PRICING_FIELD
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["BID"])
    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_one_adc_and_one_pricing_field():
    expected_str = (
        "LSEG.L     Currency   BID\n"
        "Date                     \n"
        "2022-08-18      GBP  <NA>\n"
        "2022-08-30     <NA>  8176\n"
        "2022-08-31     <NA>  8102\n"
        "2022-09-01     <NA>  7926\n"
        "2022-09-02     <NA>  8006\n"
        "2022-09-05     <NA>  7954\n"
        "2022-09-06     <NA>  7966\n"
        "2022-09-07     <NA>  7944\n"
        "2022-09-08     <NA>  8004\n"
        "2022-09-09     <NA>  8004\n"
        "2022-09-12     <NA>  8094\n"
        "2022-09-13     <NA>  8004\n"
        "2022-09-14     <NA>  7900\n"
        "2022-09-15     <NA>  7800\n"
        "2022-09-16     <NA>  7770\n"
        "2022-09-20     <NA>  7542\n"
        "2022-09-21     <NA>  7728\n"
        "2022-09-22     <NA>  7468\n"
        "2022-09-23     <NA>  7468\n"
        "2022-09-26     <NA>  7632\n"
        "2022-09-27     <NA>  7622"
    )

    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_AND_ONE_PRICING_FIELD,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe="LSEG.L", fields=["TR.RevenueMean.currency", "BID"]
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_two_specific_adc_fields():
    expected_str = (
        "LSEG.L      Revenue - Mean Currency\n"
        "Date                               \n"
        "2022-08-18      7284197000      GBP"
    )

    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_ONE_INSTRUMENT_TWO_SPECIFIC_ADC_FIELDS
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe="LSEG.L", fields=["TR.RevenueMean", "TR.RevenueMean.currency"]
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_one_adc_field_with_intraday_interval():
    expected_str = (
        "LSEG.L         Revenue\n" "Date                  \n" "2021-12-31  6740000000"
    )

    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_WITH_INTRADAY_INTERVAL,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["TR.Revenue"], interval="10min")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_one_pricing_field_with_intraday_interval():
    expected_str = (
        "LSEG.L                BID\n"
        "Timestamp                \n"
        "2022-09-28 07:00:00  7538\n"
        "2022-09-28 07:10:00  7480\n"
        "2022-09-28 07:20:00  7486\n"
        "2022-09-28 07:30:00  7498\n"
        "2022-09-28 07:40:00  7506\n"
        "2022-09-28 07:50:00  7520\n"
        "2022-09-28 08:00:00  7522\n"
        "2022-09-28 08:10:00  7526\n"
        "2022-09-28 08:20:00  7552\n"
        "2022-09-28 08:30:00  7542\n"
        "2022-09-28 08:40:00  7562\n"
        "2022-09-28 08:50:00  7562\n"
        "2022-09-28 09:00:00  7534\n"
        "2022-09-28 09:10:00  7512\n"
        "2022-09-28 09:20:00  7488\n"
        "2022-09-28 09:30:00  7488\n"
        "2022-09-28 09:40:00  7482\n"
        "2022-09-28 09:50:00  7450\n"
        "2022-09-28 10:00:00  7526\n"
        "2022-09-28 10:10:00  7562"
    )

    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_ONE_INST_ONE_PRICING_FIELD_WITH_INTRADAY_INTERVAL,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["BID"], interval="10min")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_one_adc_field_with_non_intraday_interval():
    expected_str = (
        "LSEG.L      Revenue - Mean\n"
        "Date                      \n"
        "2022-08-18      7284197000"
    )
    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_ONE_INST_ONE_ADC_WITH_NON_INTRADAY_INTERVAL,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["TR.RevenueMean"], interval="1d")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_one_pricing_field_with_non_intraday_interval():
    expected_str = (
        "LSEG.L       BID\n"
        "Date            \n"
        "2022-08-30  8176\n"
        "2022-08-31  8102\n"
        "2022-09-01  7926\n"
        "2022-09-02  8006\n"
        "2022-09-05  7954\n"
        "2022-09-06  7966\n"
        "2022-09-07  7944\n"
        "2022-09-08  8004\n"
        "2022-09-09  8004\n"
        "2022-09-12  8094\n"
        "2022-09-13  8004\n"
        "2022-09-14  7900\n"
        "2022-09-15  7800\n"
        "2022-09-16  7770\n"
        "2022-09-20  7542\n"
        "2022-09-21  7728\n"
        "2022-09-22  7468\n"
        "2022-09-23  7468\n"
        "2022-09-26  7632\n"
        "2022-09-27  7622"
    )

    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_ONE_INST_ONE_PRICING_WITH_NON_INTRADAY_INTERVAL,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["BID"], interval="1d")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_inst_two_adc_two_hp_non_intraday_interval_start_end_date():
    expected_str = (
        "IBM                BID         ASK  Net Income after Tax  Revenue - Mean\n"
        "Date                                                                    \n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2021-01-04  118.449888  118.459439                  <NA>            <NA>\n"
        "2021-01-05  120.513042    120.5608                  <NA>            <NA>\n"
        "2021-01-06  123.493154  123.512257                  <NA>            <NA>\n"
        "2021-01-07  123.206604  123.244811                  <NA>            <NA>\n"
        "2021-01-08  122.767229  122.805435                  <NA>            <NA>\n"
        "2021-01-11  122.824539  122.862745                  <NA>            <NA>\n"
        "2021-01-12  123.397637  123.407189                  <NA>     73959395730\n"
        "2021-01-12        <NA>        <NA>                  <NA>     73959395730\n"
        "2021-01-13  121.219863  121.229415                  <NA>            <NA>\n"
        "2021-01-14        <NA>        <NA>                  <NA>     73965995730\n"
        "2021-01-14  123.177949  123.187501                  <NA>     73965995730\n"
        "2021-01-15  122.623954  122.662161                  <NA>            <NA>\n"
        "2021-01-18        <NA>        <NA>                  <NA>     73987395730\n"
        "2021-01-18        <NA>        <NA>                  <NA>     73987395730\n"
        "2021-01-19  123.206604  123.235259                  <NA>            <NA>\n"
        "2021-01-20  124.190423  124.247733                  <NA>            <NA>\n"
        "2021-01-21  125.909718   125.91927                  <NA>     74726080400\n"
        "2021-01-22   113.28245  113.292002                  <NA>     74238533200\n"
        "2021-01-25        <NA>        <NA>                  <NA>     74191285570\n"
        "2021-01-25  113.253795  113.263347                  <NA>     74191285570\n"
        "2021-01-26  116.969383  116.988487                  <NA>            <NA>\n"
        "2021-01-27        <NA>        <NA>                  <NA>     74195199870\n"
        "2021-01-27        <NA>        <NA>                  <NA>     74195199870\n"
        "2021-01-27        <NA>        <NA>                  <NA>     74195199870\n"
        "2021-01-27  116.978935  117.103106                  <NA>     74195199870\n"
        "2021-01-28  114.686541  114.696093                  <NA>            <NA>\n"
        "2021-01-29  113.693171  113.702723                  <NA>            <NA>\n"
        "2021-02-01  115.078159  115.135469                  <NA>            <NA>"
    )
    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_ONE_INS_TWO_ADC_TWO_HP_NON_INTRADAY_START_END_DATE,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe="IBM",
        fields=["BID", "ASK", "TR.F.NetIncAfterTax", "TR.RevenueMean"],
        interval="daily",
        start="2021-01-01",
        end="2021-02-01",
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_one_instrument_two_specific_pricing_fields():
    expected_str = (
        "LSEG.L       BID   ASK\n"
        "Date                  \n"
        "2022-08-30  8176  8178\n"
        "2022-08-31  8102  8106\n"
        "2022-09-01  7926  7928\n"
        "2022-09-02  8006  8008\n"
        "2022-09-05  7954  7956\n"
        "2022-09-06  7966  7968\n"
        "2022-09-07  7944  7946\n"
        "2022-09-08  8004  8006\n"
        "2022-09-09  8004  8010\n"
        "2022-09-12  8094  8098\n"
        "2022-09-13  8004  8006\n"
        "2022-09-14  7900  7902\n"
        "2022-09-15  7800  7802\n"
        "2022-09-16  7770  7786\n"
        "2022-09-20  7542  7548\n"
        "2022-09-21  7728  7730\n"
        "2022-09-22  7468  7470\n"
        "2022-09-23  7468  7470\n"
        "2022-09-26  7632  7634\n"
        "2022-09-27  7622  7624"
    )
    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_ONE_INSTRUMENT_TWO_SPECIFIC_PRICING_FIELDS,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["BID", "ASK"])

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_two_instruments_without_fields():
    expected_str = (
        "              IBM.N                                                                                                                          EUR=                                                                                                                                                                                                                       \n"
        "           TRDPRC_1  HIGH_1   LOW_1 ACVOL_UNS OPEN_PRC     BID     ASK TRNOVR_UNS      VWAP BLKCOUNT BLKVOLUM NUM_MOVES TRD_STATUS SALTIM     BID     ASK BID_HIGH_1 BID_LOW_1 OPEN_BID MID_PRICE NUM_BIDS ASK_LOW_1 ASK_HIGH_1 ASIAOP_BID ASIAHI_BID ASIALO_BID ASIACL_BID EUROP_BID EURHI_BID EURLO_BID EURCL_BID AMEROP_BID AMERHI_BID AMERLO_BID AMERCL_BID OPEN_ASK\n"
        "Date                                                                                                                                                                                                                                                                                                                                                                    \n"
        "2022-09-21   124.93  127.77  124.92   1096128   126.89  124.94  124.95  137967478   125.868        2   477129      8477          1  72600    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>       <NA>       <NA>       <NA>       <NA>      <NA>      <NA>      <NA>      <NA>       <NA>       <NA>       <NA>       <NA>     <NA>\n"
        "2022-09-22   125.31  126.49  124.45   1152042   124.76  125.31  125.32  144521845  125.4484        2   450245      9169          1  72600  0.9836   0.984     0.9907    0.9807   0.9836    0.9838   103843     0.981     0.9909     0.9836     0.9853     0.9807     0.9843    0.9828    0.9907     0.981    0.9838     0.9874     0.9887      0.981     0.9836   0.9838\n"
        "2022-09-23   122.71  124.57  121.75   1555461   124.53  122.75  122.76  191160601  122.8964        2   684185     11039          1  72600   0.969  0.9694     0.9851    0.9666   0.9835    0.9692    90975    0.9669     0.9854     0.9835     0.9851     0.9765     0.9774    0.9821    0.9838      0.97    0.9716     0.9751     0.9774     0.9666      0.969   0.9839\n"
        "2022-09-26   122.01  124.25  121.76   1287055    122.3   122.0  122.01  157505074  122.3763        2   593148      9160          1  72600  0.9606  0.9609     0.9709    0.9565   0.9678   0.96075   109840    0.9569     0.9712     0.9684     0.9709     0.9565     0.9676    0.9627    0.9701    0.9608    0.9621     0.9641     0.9689     0.9598     0.9606    0.968\n"
        "2022-09-27   121.74  123.95  121.09   1335006    122.6  121.76  121.77  162900375  122.0222        2   559187     10219          1  72600  0.9592  0.9596      0.967    0.9567   0.9609    0.9594   104222     0.957     0.9673     0.9609      0.967     0.9583     0.9645    0.9635     0.967    0.9592    0.9612     0.9627     0.9652     0.9567     0.9592   0.9611\n"
        "2022-09-28     <NA>    <NA>    <NA>      <NA>     <NA>    <NA>    <NA>       <NA>      <NA>     <NA>     <NA>      <NA>       <NA>   <NA>    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>     0.9592       0.96     0.9534     0.9577      <NA>      <NA>      <NA>      <NA>       <NA>       <NA>       <NA>       <NA>     <NA>"
    )

    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_TWO_INSTRUMENTS_WITHOUT_FIELDS
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe=["IBM.N", "EUR="], count=5)

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_two_instruments_one_adc_fields_quarterly_interval_start_date():
    expected_str = (
        "TR.F.NETINCAFTERTAX          IBM       MSFT.O\n"
        "Date                                         \n"
        "2018-12-31           10760000000         <NA>\n"
        "2019-06-30                  <NA>  39397000000"
    )

    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_TWO_INST_ONE_ADC_QUARTERLY_INTERVAL_START_DATE,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe=["IBM", "MSFT.O"],
        fields=["TR.F.NetIncAfterTax"],
        use_field_names_in_headers=True,
        interval="quarterly",
        start="2020-01-01",
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_two_instruments_two_pricing_fields_daily_interval_start_date():
    expected_str = (
        "              EUR=            GBP=        \n"
        "               BID     ASK     BID     ASK\n"
        "Date                                      \n"
        "2022-08-31  1.0057  1.0061  1.1622  1.1625\n"
        "2022-09-01  0.9944  0.9947  1.1542  1.1546\n"
        "2022-09-02  0.9951  0.9955  1.1507  1.1511\n"
        "2022-09-05  0.9926   0.993  1.1513  1.1517\n"
        "2022-09-06  0.9902  0.9906  1.1516  1.1524\n"
        "2022-09-07  0.9999  1.0003  1.1525  1.1529\n"
        "2022-09-08  0.9994  0.9998    1.15  1.1504\n"
        "2022-09-09  1.0039  1.0043  1.1587  1.1591\n"
        "2022-09-12  1.0119  1.0122  1.1679  1.1688\n"
        "2022-09-13   0.997  0.9974  1.1491  1.1495\n"
        "2022-09-14  0.9977  0.9981  1.1535  1.1539\n"
        "2022-09-15  0.9999  1.0003  1.1463  1.1469\n"
        "2022-09-16  1.0015  1.0019  1.1412  1.1416\n"
        "2022-09-19  1.0022  1.0026  1.1429  1.1435\n"
        "2022-09-20   0.997  0.9974  1.1379  1.1383\n"
        "2022-09-21  0.9837  0.9839  1.1266   1.127\n"
        "2022-09-22  0.9836   0.984  1.1257  1.1261\n"
        "2022-09-23   0.969  0.9694  1.0856   1.086\n"
        "2022-09-26  0.9606  0.9609  1.0684  1.0688\n"
        "2022-09-27  0.9592  0.9596  1.0731  1.0734"
    )

    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_TWO_INSTRUMENTS_TWO_HP_DAILY_INTERVAL_START_DATE,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe=["EUR=", "GBP="],
        fields=["BID", "ASK"],
        interval="daily",
        start="2020-10-01",
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_two_instruments_adc_and_pricing_fields_1h_interval_field_names():
    expected_str = (
        "                      VOD.L                                                      MSFT.O                                                    \n"
        "                        BID     ASK TR.F.NETINCAFTERTAX TR.REVENUEMEAN.currency     BID     ASK TR.F.NETINCAFTERTAX TR.REVENUEMEAN.currency\n"
        "Timestamp                                                                                                                                  \n"
        "2022-03-31 00:00:00    <NA>    <NA>          2624000000                            <NA>    <NA>                <NA>                    <NA>\n"
        "2022-06-30 00:00:00    <NA>    <NA>                <NA>                    <NA>    <NA>    <NA>         72738000000                        \n"
        "2022-09-22 00:00:00    <NA>    <NA>                <NA>                     EUR    <NA>    <NA>                <NA>                    <NA>\n"
        "2022-09-26 00:00:00    <NA>    <NA>                <NA>                    <NA>    <NA>    <NA>                <NA>                     USD\n"
        "2022-09-27 04:00:00  105.02   110.0                <NA>                    <NA>  105.02   110.0                <NA>                    <NA>\n"
        "2022-09-27 06:00:00  111.14    92.8                <NA>                    <NA>  111.14    92.8                <NA>                    <NA>\n"
        "2022-09-27 07:00:00  106.72  106.76                <NA>                    <NA>  106.72  106.76                <NA>                    <NA>\n"
        "2022-09-27 08:00:00  106.38  106.44                <NA>                    <NA>  106.38  106.44                <NA>                    <NA>\n"
        "2022-09-27 09:00:00  105.82  105.86                <NA>                    <NA>  105.82  105.86                <NA>                    <NA>\n"
        "2022-09-27 10:00:00  106.06  106.12                <NA>                    <NA>  106.06  106.12                <NA>                    <NA>\n"
        "2022-09-27 11:00:00  106.54  106.58                <NA>                    <NA>  106.54  106.58                <NA>                    <NA>\n"
        "2022-09-27 12:00:00   106.7  106.74                <NA>                    <NA>   106.7  106.74                <NA>                    <NA>\n"
        "2022-09-27 13:00:00  106.66  106.72                <NA>                    <NA>  106.66  106.72                <NA>                    <NA>\n"
        "2022-09-27 14:00:00  106.84  106.88                <NA>                    <NA>  106.84  106.88                <NA>                    <NA>\n"
        "2022-09-27 15:00:00  105.54  105.64                <NA>                    <NA>  105.54  105.64                <NA>                    <NA>\n"
        "2022-09-27 16:00:00  105.02   107.2                <NA>                    <NA>  105.02   107.2                <NA>                    <NA>\n"
        "2022-09-28 04:00:00  105.02   107.2                <NA>                    <NA>  105.02   107.2                <NA>                    <NA>\n"
        "2022-09-28 06:00:00  121.38   89.73                <NA>                    <NA>  121.38   89.73                <NA>                    <NA>\n"
        "2022-09-28 07:00:00  103.58  103.62                <NA>                    <NA>  103.58  103.62                <NA>                    <NA>\n"
        "2022-09-28 08:00:00  103.18  103.22                <NA>                    <NA>  103.18  103.22                <NA>                    <NA>\n"
        "2022-09-28 09:00:00  102.68  102.72                <NA>                    <NA>  102.68  102.72                <NA>                    <NA>\n"
        "2022-09-28 10:00:00   104.5  104.56                <NA>                    <NA>   104.5  104.56                <NA>                    <NA>\n"
        "2022-09-28 11:00:00   104.2  104.24                <NA>                    <NA>   104.2  104.24                <NA>                    <NA>\n"
        "2022-09-28 12:00:00  103.98  104.04                <NA>                    <NA>  103.98  104.04                <NA>                    <NA>"
    )

    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_TWO_INSTRUMENTS_ADC_AND_HP_1H_INTERVAL_FIELD_NAMES,
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=["VOD.L", "MSFT.O"],
        fields=["BID", "ASK", "TR.F.NetIncAfterTax", "TR.RevenueMean.currency"],
        interval="1h",
        use_field_names_in_headers=True,
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_two_instruments_one_adc_two_hp_interval_tick_start_date():
    expected_str = (
        "                          IBM.N                        LSEG.L                     \n"
        "                            BID     ASK Revenue - Mean    BID   ASK Revenue - Mean\n"
        "Timestamp                                                                         \n"
        "2021-04-25 00:00:00.000    <NA>    <NA>    74397055190   <NA>  <NA>           <NA>\n"
        "2021-05-10 00:00:00.000    <NA>    <NA>           <NA>   <NA>  <NA>     6935640740\n"
        "2022-09-27 19:59:59.533  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.608  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.630  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.713  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.784  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.855  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.855  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.855  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.855  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.900  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.901  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.958  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.962  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.982  121.74  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.997  121.76  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.997  121.76  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.998  121.76  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 19:59:59.998  121.76  121.77           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 20:00:00.163     0.0     0.0           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-27 20:00:02.001     0.0     0.0           <NA>   <NA>  <NA>           <NA>\n"
        "2022-09-28 13:34:14.139    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.200    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.563    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.923    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.952    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.952    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.952    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.953    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.953    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.953    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.953    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.953    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.953    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.953    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.953    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.962    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.963    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.963    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:14.963    <NA>    <NA>           <NA>   7616  7620           <NA>\n"
        "2022-09-28 13:34:15.400    <NA>    <NA>           <NA>   7616  7620           <NA>"
    )

    session = StubSession(
        is_open=True,
        response=td.UDF_GET_HISTORY_TWO_INSTS_ONE_ADC_FIELD_TWO_HP_TICK_START_DATE,
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=["IBM.N", "LSEG.L"],
        fields=["BID", "ASK", "TR.RevenueMean"],
        interval="tick",
        start="2021-05-11",
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_three_instruments_without_fields():
    expected_str = (
        "              IBM.N                                                                                                                           EUR=                                                                                                                                                                                                                        S)MyUSD.GESG1-150112\n"
        "           TRDPRC_1   HIGH_1   LOW_1 ACVOL_UNS OPEN_PRC     BID     ASK TRNOVR_UNS      VWAP BLKCOUNT BLKVOLUM NUM_MOVES TRD_STATUS SALTIM     BID     ASK BID_HIGH_1 BID_LOW_1 OPEN_BID MID_PRICE NUM_BIDS ASK_LOW_1 ASK_HIGH_1 ASIAOP_BID ASIAHI_BID ASIALO_BID ASIACL_BID EUROP_BID EURHI_BID EURLO_BID EURCL_BID AMEROP_BID AMERHI_BID AMERLO_BID AMERCL_BID OPEN_ASK             TRDPRC_1\n"
        "Date                                                                                                                                                                                                                                                                                                                                                                                          \n"
        "2022-08-30   129.58   130.77   129.3    735905   130.55  129.58  129.59   95531452  129.8149        2   350014      6041          1  72600    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>       <NA>       <NA>       <NA>       <NA>      <NA>      <NA>      <NA>      <NA>       <NA>       <NA>       <NA>       <NA>     <NA>                 <NA>\n"
        "2022-08-31   128.45    130.0   128.4   1137678   129.92  128.46  128.48  146465933  128.7411        2   709588      6077          1  72600    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>       <NA>       <NA>       <NA>       <NA>      <NA>      <NA>      <NA>      <NA>       <NA>       <NA>       <NA>       <NA>     <NA>                 <NA>\n"
        "2022-09-01   129.66   129.79  127.74   1060391    128.7  129.66  129.67  137059053  129.2533        2   522811      7331          1  72600  0.9944  0.9947     1.0055    0.9909   1.0053   0.99455    85854    0.9912     1.0059     1.0053     1.0055     1.0006     1.0028    1.0012    1.0048    0.9909    0.9947     1.0017     1.0021     0.9909     0.9944   1.0057                    3\n"
        "2022-09-02   127.79   130.56  127.25    886927    130.3  127.83  127.84  113943414  128.4699        2   450566      6472          1  72600  0.9951  0.9955     1.0033    0.9941   0.9944    0.9953    68962    0.9944     1.0036     0.9944     0.9997     0.9941     0.9987    0.9965    1.0033    0.9962    1.0028     0.9996     1.0033     0.9943     0.9951   0.9947                    3\n"
        "2022-09-05     <NA>     <NA>    <NA>      <NA>     <NA>    <NA>    <NA>       <NA>      <NA>     <NA>     <NA>      <NA>       <NA>   <NA>  0.9926   0.993     0.9948    0.9875   0.9948    0.9928    67114    0.9879     0.9952     0.9948     0.9948     0.9875      0.991    0.9904    0.9943    0.9875    0.9927     0.9932     0.9936     0.9911     0.9926   0.9952                    3\n"
        "2022-09-06   126.72    127.9   126.3   1071382    127.8  126.76  126.77  135947360  126.8897        2   447271      8029          1  72600  0.9902  0.9906     0.9986    0.9862   0.9925    0.9904   101494    0.9865     0.9988     0.9925     0.9986     0.9923     0.9975    0.9946    0.9986    0.9862     0.991     0.9924     0.9937     0.9862     0.9902   0.9929                    3\n"
        "2022-09-07   127.71  127.855  126.28    771510   126.69  127.72  127.73   98346699   127.473        2   420909      4878          1  72600  0.9999  1.0003      1.001    0.9874   0.9902    1.0001    82606    0.9876     1.0013     0.9902     0.9928     0.9875     0.9922    0.9891    0.9954    0.9874    0.9937     0.9896      1.001     0.9874     0.9999   0.9906                    3\n"
        "2022-09-08   128.47   128.51  126.59    911647   127.12  128.42  128.43  116797276  128.1168        2   465537      5751          1  72600  0.9994  0.9998     1.0029    0.9929   1.0001    0.9996    86338    0.9932     1.0032     1.0001     1.0014     0.9975      0.998    0.9988    1.0029    0.9929    0.9952     1.0008     1.0029     0.9929     0.9994   1.0003                    3\n"
        "2022-09-09   129.19   129.49  128.07   1069094    128.9  129.21  129.22  138041202  129.1198        2   520062      6216          1  72600  1.0039  1.0043     1.0112    0.9993   0.9993    1.0041    76399    0.9997     1.0115     0.9993      1.011     0.9993     1.0096    1.0071    1.0112     1.003    1.0044     1.0073     1.0075      1.003     1.0039   0.9997                    3\n"
        "2022-09-12   130.66   130.99  129.91   1245309   130.33   130.7  130.71  162528528  130.5126        2   628490      6975          1  72600  1.0119  1.0122     1.0197    1.0058   1.0078   1.01205    62347    1.0061       1.02     1.0078     1.0197     1.0058     1.0174    1.0076    1.0197    1.0076    1.0124     1.0135     1.0162     1.0103     1.0119   1.0082                    3\n"
        "2022-09-13   127.25   129.82   126.8   1603709   129.14  127.23  127.25  205136259  127.9136        2   752373      9835          1  72600   0.997  0.9974     1.0187    0.9964   1.0121    0.9972    77655    0.9968     1.0189     1.0121     1.0155     1.0116     1.0145    1.0126    1.0187    0.9994    0.9996     1.0179     1.0187     0.9964      0.997   1.0125                    3\n"
        "2022-09-14   127.69    129.0  126.85   1286648    127.5  127.66  127.67  164386719  127.7636        3   725522      8149          1  72600  0.9977  0.9981     1.0023    0.9954   0.9967    0.9979    87677    0.9957     1.0026     0.9967     1.0002     0.9954     0.9986    0.9994    1.0023    0.9958    0.9992     1.0006     1.0009     0.9967     0.9977   0.9971                    3\n"
        "2022-09-15   125.49   127.39   124.9   1474804   127.39  125.49   125.5  185269243   125.623        3   705660     10066          1  72600  0.9999  1.0003     1.0017    0.9954   0.9979    1.0001    69080    0.9957      1.002     0.9979     0.9984     0.9954     0.9977    0.9967    1.0017    0.9954     0.999     0.9977     1.0017      0.997     0.9999   0.9982                    3\n"
        "2022-09-16   127.27   127.49  124.01   5408858   124.36  127.23  127.27  685427466  126.7231        2  4463300     10894          1  72600  1.0015  1.0019     1.0036    0.9943   0.9999    1.0017    72842    0.9946     1.0038     0.9999     1.0012     0.9943     0.9956    0.9995    1.0036    0.9943     1.001     0.9983     1.0036     0.9951     1.0015   1.0003                    3\n"
        "2022-09-19   127.73   128.06  126.28   1320203    126.5  127.69  127.73  168291147  127.4737        2   725956      7910          1  72600  1.0022  1.0026     1.0029    0.9964    1.001    1.0024    63178    0.9967     1.0031      1.001     1.0029     0.9964     0.9978    0.9992    1.0017    0.9964    1.0002     0.9992     1.0027     0.9974     1.0022   1.0014                    3\n"
        "2022-09-20    126.3    126.9  125.53    799630    126.9   126.3  126.31  100914959  126.2021        2   357706      7375          1  72600   0.997  0.9974      1.005    0.9953   1.0021    0.9972    72943    0.9956     1.0053     1.0021      1.005     1.0011     1.0034    1.0021    1.0041    0.9953    0.9992     1.0006     1.0013     0.9953      0.997   1.0025                    3\n"
        "2022-09-21   124.93   127.77  124.92   1096128   126.89  124.94  124.95  137967478   125.868        2   477129      8477          1  72600  0.9837  0.9839     0.9976    0.9812    0.997    0.9838    87445    0.9814      0.998      0.997     0.9976     0.9883     0.9909    0.9959    0.9968    0.9865    0.9878     0.9921     0.9925     0.9812     0.9837   0.9974                    3\n"
        "2022-09-22   125.31   126.49  124.45   1152042   124.76  125.31  125.32  144521845  125.4484        2   450245      9169          1  72600  0.9836   0.984     0.9907    0.9807   0.9836    0.9838   103843     0.981     0.9909     0.9836     0.9853     0.9807     0.9843    0.9828    0.9907     0.981    0.9838     0.9874     0.9887      0.981     0.9836   0.9838                    3\n"
        "2022-09-23   122.71   124.57  121.75   1555461   124.53  122.75  122.76  191160601  122.8964        2   684185     11039          1  72600   0.969  0.9694     0.9851    0.9666   0.9835    0.9692    90975    0.9669     0.9854     0.9835     0.9851     0.9765     0.9774    0.9821    0.9838      0.97    0.9716     0.9751     0.9774     0.9666      0.969   0.9839                    3\n"
        "2022-09-26   122.01   124.25  121.76   1287055    122.3   122.0  122.01  157505074  122.3763        2   593148      9160          1  72600  0.9606  0.9609     0.9709    0.9565   0.9678   0.96075   109840    0.9569     0.9712     0.9684     0.9709     0.9565     0.9676    0.9627    0.9701    0.9608    0.9621     0.9641     0.9689     0.9598     0.9606    0.968                    3\n"
        "2022-09-27   121.74   123.95  121.09   1335006    122.6  121.76  121.77  162900375  122.0222        2   559187     10219          1  72600  0.9592  0.9596      0.967    0.9567   0.9609    0.9594   104222     0.957     0.9673     0.9609      0.967     0.9583     0.9645    0.9635     0.967    0.9592    0.9612     0.9627     0.9652     0.9567     0.9592   0.9611                    3\n"
        "2022-09-28     <NA>     <NA>    <NA>      <NA>     <NA>    <NA>    <NA>       <NA>      <NA>     <NA>     <NA>      <NA>       <NA>   <NA>    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>     0.9592       0.96     0.9534     0.9577      <NA>      <NA>      <NA>      <NA>       <NA>       <NA>       <NA>       <NA>     <NA>                    3"
    )

    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_THREE_INSTRUMENTS_WITHOUT_FIELDS
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(universe=["IBM.N", "EUR=", "S)MyUSD.GESG1-150112"])

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_eur_gpb_tick_interval():
    expected_str = (
        "                           EUR=            GBP=        \n"
        "                            BID     ASK     BID     ASK\n"
        "Timestamp                                              \n"
        "2022-09-28 17:00:14.906  0.9701  0.9703    <NA>    <NA>\n"
        "2022-09-28 17:00:15.770    0.97  0.9704    <NA>    <NA>\n"
        "2022-09-28 17:00:16.765    0.97  0.9704    <NA>    <NA>\n"
        "2022-09-28 17:00:18.051    <NA>    <NA>  1.0855  1.0858\n"
        "2022-09-28 17:00:18.790    0.97  0.9704    <NA>    <NA>\n"
        "2022-09-28 17:00:18.794    <NA>    <NA>  1.0853  1.0857\n"
        "2022-09-28 17:00:19.061    <NA>    <NA>  1.0854  1.0857\n"
        "2022-09-28 17:00:19.283    <NA>    <NA>  1.0855  1.0858\n"
        "2022-09-28 17:00:19.785    <NA>    <NA>  1.0854  1.0858\n"
        "2022-09-28 17:00:19.794    0.97  0.9704    <NA>    <NA>"
    )

    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_EUR_GPB_TICK_INTERVAL
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=["EUR=", "GBP="], fields=["BID", "ASK"], interval="tick", count=5
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_chain_one_adc_field_one_hp_field():
    expected_str = (
        "            BMA.BA             BBAR.BA             BHIP.BA        GGAL.BA             BPAT.BA             SUPV.BA        \n"
        "           Revenue         BID Revenue         BID Revenue    BID Revenue         BID Revenue         BID Revenue     BID\n"
        "Date                                                                                                                     \n"
        "2022-08-30    <NA>  430.323194    <NA>   313.05708    <NA>   12.2    <NA>  247.632803    <NA>  108.071291    <NA>   112.4\n"
        "2022-08-31    <NA>  408.459198    <NA>  296.658852    <NA>   11.5    <NA>  236.997355    <NA>  104.344695    <NA>  106.05\n"
        "2022-09-01    <NA>   407.46538    <NA>  289.205112    <NA>  11.65    <NA>  237.343626    <NA>  103.350936    <NA>   106.5\n"
        "2022-09-05    <NA>       418.6    <NA>       302.1    <NA>   12.2    <NA>  241.004198    <NA>  106.829093    <NA>   104.6\n"
        "2022-09-06    <NA>       419.0    <NA>       298.0    <NA>   12.0    <NA>   243.27969    <NA>  105.338454    <NA>   104.0\n"
        "2022-09-07    <NA>       443.5    <NA>       311.0    <NA>   12.7    <NA>  251.293376    <NA>  108.319731    <NA>   107.0\n"
        "2022-09-08    <NA>       441.0    <NA>       311.2    <NA>   12.5    <NA>       252.5    <NA>  108.319731    <NA>   108.0\n"
        "2022-09-09    <NA>       472.2    <NA>       321.0    <NA>  12.55    <NA>       264.3    <NA>  107.822852    <NA>   111.4\n"
        "2022-09-12    <NA>       468.0    <NA>       315.5    <NA>  12.35    <NA>       259.6    <NA>   109.31349    <NA>   110.5\n"
        "2022-09-13    <NA>       455.0    <NA>       306.0    <NA>   12.1    <NA>       250.1    <NA>  104.344695    <NA>   109.5\n"
        "2022-09-14    <NA>       477.0    <NA>       315.0    <NA>   12.2    <NA>       256.1    <NA>   109.31349    <NA>   113.0\n"
        "2022-09-15    <NA>       480.0    <NA>       310.0    <NA>   11.9    <NA>       258.0    <NA>  106.332213    <NA>  113.05\n"
        "2022-09-16    <NA>       489.9    <NA>       315.5    <NA>  11.85    <NA>       259.2    <NA>  108.816611    <NA>   113.0\n"
        "2022-09-19    <NA>       520.9    <NA>       339.2    <NA>   12.0    <NA>       270.7    <NA>       105.0    <NA>   114.0\n"
        "2022-09-20    <NA>       503.0    <NA>       342.6    <NA>  11.75    <NA>       268.3    <NA>       108.5    <NA>   113.5\n"
        "2022-09-21    <NA>       502.0    <NA>      340.45    <NA>   11.6    <NA>       267.6    <NA>       106.0    <NA>   114.0\n"
        "2022-09-22    <NA>       510.0    <NA>       345.5    <NA>  11.65    <NA>       269.5    <NA>      108.25    <NA>   113.1\n"
        "2022-09-23    <NA>       488.6    <NA>       319.2    <NA>   11.0    <NA>       257.3    <NA>      104.25    <NA>   112.0\n"
        "2022-09-26    <NA>       462.0    <NA>      305.15    <NA>  10.65    <NA>      242.35    <NA>       107.0    <NA>   107.6\n"
        "2022-09-27    <NA>       444.3    <NA>       304.5    <NA>  10.45    <NA>       228.9    <NA>       100.5    <NA>  106.55"
    )

    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_CHAIN_ONE_ADC_FIELD_ONE_HP_FIELD
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=[
            'SCREEN(U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010"))'
        ],
        fields=["TR.Revenue", "BID"],
    )
    session.close()

    set_default(None)

    assert result_df.to_string() == expected_str


def test_udf_get_history_chains_adc_pricing_fields(monkeypatch):
    expected_str = (
        "              GS.N                       NKE.N                     CSCO.OQ                       JPM.N                  DIS.N                     INTC.OQ                      DOW.N                       MRK.N                        CVX.N                         AXP.N                         VZ.N                          HD.N                       WBA.OQ                       MCD.N                       UNH.N                    KO.N                        JNJ.N                      MSFT.OQ                       HON.OQ                       CRM.N                         PG.N                        IBM.N                        MMM.N                      AAPL.OQ                         WMT.N                         CAT.N                      AMGN.OQ                          V.N                        TRV.N                    BA.N                     \n"
        "               BID     ASK      Revenue    BID    ASK      Revenue     BID    ASK      Revenue     BID     ASK Revenue    BID    ASK      Revenue     BID    ASK      Revenue    BID    ASK      Revenue     BID     ASK      Revenue     BID     ASK       Revenue     BID     ASK      Revenue     BID     ASK       Revenue     BID     ASK       Revenue    BID    ASK       Revenue    BID    ASK      Revenue     BID     ASK Revenue     BID     ASK      Revenue     BID     ASK      Revenue     BID     ASK       Revenue    BID    ASK      Revenue     BID     ASK      Revenue     BID     ASK      Revenue     BID     ASK      Revenue     BID     ASK      Revenue     BID     ASK       Revenue     BID     ASK       Revenue     BID     ASK      Revenue     BID     ASK      Revenue     BID     ASK      Revenue     BID     ASK Revenue     BID     ASK      Revenue\n"
        "Date                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      \n"
        "2021-08-31    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>  132509000000   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2021-09-25    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>  365817000000    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2021-09-30    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>  24105000000    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2021-10-02    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>  67418000000    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2021-12-25    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>  79024000000   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2021-12-31    <NA>    <NA>  64989000000   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>  54968000000    <NA>    <NA>  48704000000    <NA>    <NA>  155606000000    <NA>    <NA>  42838000000    <NA>    <NA>  133613000000    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>  23222900000    <NA>    <NA>    <NA>    <NA>    <NA>  38655000000    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>  34392000000    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>  57350000000    <NA>    <NA>  35355000000    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>  50971000000    <NA>    <NA>  25979000000    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>  62286000000\n"
        "2022-01-02    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>  93775000000    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2022-01-30    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>  151157000000   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2022-01-31    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>  26492000000    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>  572754000000    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2022-05-31    <NA>    <NA>         <NA>   <NA>   <NA>  46710000000    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2022-06-30    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>  198270000000   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>  80187000000    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2022-07-30    <NA>    <NA>         <NA>   <NA>   <NA>         <NA>    <NA>   <NA>  51557000000    <NA>    <NA>    <NA>   <NA>   <NA>         <NA>    <NA>   <NA>         <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>   <NA>   <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>   <NA>   <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>          <NA>    <NA>    <NA>          <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>         <NA>    <NA>    <NA>    <NA>    <NA>    <NA>         <NA>\n"
        "2022-09-22  312.49  312.73         <NA>  98.54  98.55         <NA>   41.14  41.15         <NA>  111.19   111.2    <NA>  28.06  28.07         <NA>   44.76  44.77         <NA>   87.5  87.51         <NA>  143.01  143.03         <NA>  102.15  102.16          <NA>  154.83  154.84         <NA>  247.91  247.92          <NA>  268.97  269.15          <NA>  39.93  39.94          <NA>  33.29  33.31         <NA>  517.22  517.45    <NA>  173.21  173.25         <NA>  240.78   240.8         <NA>  166.12  166.13          <NA>  59.24  59.25         <NA>   150.1  150.11         <NA>  125.31  125.32         <NA>  136.19   136.2         <NA>   114.1  114.11         <NA>  152.69  152.71          <NA>  133.35  133.37          <NA>   185.7  185.75         <NA>  156.99   157.0         <NA>  227.68  227.75         <NA>  170.49  170.54    <NA>  138.66  138.67         <NA>\n"
        "2022-09-23  302.19  302.26         <NA>  97.04  97.06         <NA>   40.67  40.68         <NA>  109.21  109.22    <NA>  27.52  27.54         <NA>    43.9  43.91         <NA>  86.79   86.8         <NA>  140.34  140.37         <NA>   99.55   99.59          <NA>  144.81  144.82         <NA>  245.95  245.96          <NA>  271.08  271.25          <NA>  39.55  39.56          <NA>  32.83  32.84         <NA>  513.98  514.07    <NA>   171.4  171.49         <NA>  237.96  237.97         <NA>  166.87  166.93          <NA>   58.6  58.61         <NA>  147.08  147.09         <NA>  122.75  122.76         <NA>  135.63  135.64         <NA>  113.11  113.16         <NA>  150.51  150.53          <NA>  130.15  130.16          <NA>   184.1  184.18         <NA>   155.5  155.57         <NA>  226.98   227.0         <NA>  164.24  164.29    <NA>  131.28  131.29         <NA>\n"
        "2022-09-26  294.72  294.86         <NA>  96.16  96.18         <NA>   40.58   40.6         <NA>  106.79   106.8    <NA>  26.94  26.95         <NA>   43.37  43.38         <NA>  86.35  86.36         <NA>   137.5  137.53         <NA>   98.18   98.19          <NA>   141.1  141.11         <NA>  243.69  243.78          <NA>  266.87  266.93          <NA>  38.92  38.94          <NA>   32.7  32.71         <NA>  508.69  508.81    <NA>  170.07  170.12         <NA>  237.46  237.52         <NA>   165.8  165.82          <NA>  57.86  57.87         <NA>  146.32  146.39         <NA>   122.0  122.01         <NA>  135.78  135.79         <NA>  113.04  113.06         <NA>  150.73  150.89          <NA>  131.47  131.48          <NA>  180.61  180.71         <NA>  150.51   150.6         <NA>  226.83  226.87         <NA>  162.65  162.76    <NA>  127.47  127.48         <NA>\n"
        "2022-09-27  291.64  291.66         <NA>  96.29   96.3         <NA>   40.54  40.55         <NA>  105.87  105.88    <NA>  26.88  26.89         <NA>    43.8  43.81         <NA>  85.87  85.88         <NA>  137.53  137.59         <NA>   95.91   95.93          <NA>  141.07  141.12         <NA>  236.71  236.87          <NA>   268.8  268.87          <NA>  38.89   38.9          <NA>  32.43  32.44         <NA>  508.76  508.89    <NA>  170.07   170.1         <NA>  236.41  236.49         <NA>  164.95  164.96          <NA>  56.39   56.4         <NA>  148.86  148.89         <NA>  121.76  121.77         <NA>  132.04  132.05         <NA>  112.46  112.49         <NA>  151.75  151.76          <NA>  130.98  131.04          <NA>  178.03  178.06         <NA>  151.28  151.29         <NA>  225.99  226.07         <NA>  162.47  162.48    <NA>  127.57  127.58         <NA>\n"
        "2022-09-28  300.71  300.72         <NA>  98.66  98.67         <NA>   41.32  41.33         <NA>  108.04  108.05    <NA>  27.11  27.12         <NA>   45.05  45.06         <NA>  86.78  86.79         <NA>  140.46  140.49         <NA>   99.36    99.4          <NA>  145.62  145.63         <NA>  236.89  236.94          <NA>  282.19   282.2          <NA>  39.35  39.36          <NA>  33.18  33.19         <NA>  513.45  513.75    <NA>   173.8  173.83         <NA>  241.02  241.03         <NA>  166.47  166.53          <NA>  56.97  56.98         <NA>  150.17  150.18         <NA>  122.71  122.72         <NA>  131.93  131.98         <NA>  114.25  114.26         <NA>  149.79   149.8          <NA>  133.07  133.11          <NA>   179.1  179.24         <NA>  152.98  152.99         <NA>  230.91  230.98         <NA>  167.69  167.74    <NA>  133.36  133.37         <NA>"
    )
    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_CHAINS_ADC_PRICING_FIELDS
    )

    def mock_validate_responses(responses: list) -> list:
        """Cut first response to ADC."""
        responses = responses[1:]

    monkeypatch.setattr(
        "refinitiv.data.content._historical_data_provider.validate_responses",
        mock_validate_responses,
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=["0#.DJI"], fields=["BID", "ASK", "TR.Revenue"], count=3
    )
    session.close()

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_no_fields():
    expected_str = (
        "LSEG.L        TRDPRC_1    MKT_HIGH  MKT_LOW  ACVOL_UNS  MKT_OPEN   BID   ASK          TRNOVR_UNS        VWAP  MID_PRICE  PERATIO  ORDBK_VOL  NUM_MOVES  IND_AUCVOL  OFFBK_VOL  HIGH_1  ORDBK_VWAP  IND_AUC  OPEN_PRC  LOW_1  OFF_CLOSE  CLS_AUCVOL  OPN_AUCVOL  OPN_AUC  CLS_AUC  INT_AUC  INT_AUCVOL  EX_VOL_UNS  ALL_C_MOVE  ELG_NUMMOV  NAVALUE\n"
        "Date                                                                                                                                                                                                                                                                                                                                              \n"
        "2022-09-07  7897.33333      8000.0     7838    1050642      7918  7944  7946       8288071402.15    7888.567       7945  49.4845     412145       7695      167471     638292    8000     7934.95     7944      7918   7838       7944      167471        5849     7918     7944     <NA>        <NA>     1154149        7753        7199     <NA>\n"
        "2022-09-08      8044.0      8060.0     7688     611208      7964  8004  8006        4847453609.7     7930.94       8005  49.3355     587774       7217      240248      23394    8060    7932.403     8004      7964   7688       8004      240248        6609     7964     8004     <NA>        <NA>      754372        7318        7011     <NA>\n"
        "2022-09-09      8024.0      8090.0     7956     479583      7956  8004  8010       3848903522.51   8025.5082       8007  49.7081     381305       5416      182620      98135    8090    8021.854     8004      7956   7956       8004      182620        1606     7956     8004     <NA>        <NA>      602315        5471        5306     <NA>\n"
        "2022-09-12     8028.12      8098.0     7954     393139      7998  8094  8098       3165188290.65  8051.06695       8096  49.7081     374415       5142      163090      18685    8098    8053.243     8098      7998   7954       8098      163090        7468     7998     8098     <NA>        <NA>      508848        5196        4919     <NA>\n"
        "2022-09-13   8023.8095      8162.0     7942     534518      8134  8004  8006        4285291504.4   8016.4881       8005  50.2919     454096       6799      199046      76775    8162    8016.292     8004      8134   7942       8004      199046        5863     8134     8004     <NA>        <NA>      683751        6853        6609     <NA>\n"
        "2022-09-14      7972.1      8070.0     7892     521577      7962  7900  7902       4134076455.03  7925.89236       7901  49.7081     499343       6976      235608      21464    8070    7924.937     7900      7962   7892       7900      235608        3225     7962     7900     <NA>        <NA>      640027        7101        6746     <NA>\n"
        "2022-09-15  7895.55636      7908.0     7766     422663      7900  7800  7802       3299449612.11   7806.3314       7801  49.0622     399733       5081      232161      22606    7908    7806.016     7802      7900   7766       7802      232161        5668     7900     7802     <NA>        <NA>      507673        5324        4851     <NA>\n"
        "2022-09-16      7760.0      7824.0     7720    2168875      7760  7770  7786  16851819857.530001    7769.846       7778  48.4536    1015294       7430      619678    1152524    7824    7778.599     7786      7760   7720       7786      619678        3973     7760     7786     7748      103606     2577171        7929        7276     <NA>\n"
        "2022-09-19        <NA>        <NA>     <NA>       <NA>      <NA>  <NA>  <NA>                <NA>        <NA>       7778  48.3542       <NA>       <NA>        <NA>       <NA>    <NA>        <NA>     <NA>      <NA>   <NA>       <NA>        <NA>        <NA>     <NA>     <NA>     <NA>        <NA>        <NA>        <NA>        <NA>     <NA>\n"
        "2022-09-20  7763.06667      7768.0     7460     513033      7732  7542  7548       3878593615.79   7559.7715       7545  48.3542     473450       6890      186298      36986    7768    7559.729     7548      7732   7460       7548      186298       27764     7732     7548     <NA>        <NA>      663257        6999        6407     <NA>\n"
        "2022-09-21  7663.44985      7730.0     7518    1001952      7552  7728  7730     7631392654.3177   7616.5246       7729  46.8762     471364       6981      144538     530588    7730     7678.82     7728      7552   7518       7728      144538        4575     7552     7728     <NA>        <NA>     1151781        7092        6807     <NA>\n"
        "2022-09-22     7563.56      7706.0     7416     759195      7620  7468  7470       5729651816.67  7547.00074       7469   47.994     480791       5866      244543     278361    7706    7508.555     7468      7620   7416       7468      244543        3711     7620     7468     <NA>        <NA>      910761        6009        5666     <NA>\n"
        "2022-09-23  7461.98718      7528.0     7300     525502      7446  7468  7470       3914411797.42  7449.43887       7469  46.3793     495162       7688      201094      27640    7528    7449.858     7468      7446   7300       7468      201094        4947     7446     7468     <NA>        <NA>      638640        8116        7424     <NA>\n"
        "2022-09-26  7489.15237      7660.0     7480     627346      7494  7632  7634       4775494706.78   7612.2345       7633  46.3793     533163       7984      192701      93912    7660    7611.826     7634      7494   7482       7634      192701        4644     7494     7634     <NA>        <NA>      677458        8209        7673     <NA>\n"
        "2022-09-27      7652.0      7694.0     7548     669659      7606  7622  7624       5105228152.01   7623.6154       7623  47.4103     569638       6502      282974      99655    7694    7630.916     7622      7606   7548       7622      282974       16892     7606     7622     <NA>        <NA>      789730        6613        6164     <NA>\n"
        "2022-09-28      7564.1      7704.0     7454     601494      7560  7692  7696       4588771149.55   7628.9668       7694  47.3357     528526       8427      190944      72768    7704    7636.925     7696      7560   7454       7696      190944        9332     7560     7696     <NA>        <NA>      657801        8502        8182     <NA>\n"
        "2022-09-29      7594.0  7676.75664     7524     844879      7630  7596  7598       6437374217.61  7619.29235       7597  47.7953     571898       8832      224749     272681    7662     7595.53     7598      7630   7524       7598      224749       10588     7630     7598     <NA>        <NA>     1049100        9064        8646     <NA>\n"
        "2022-09-30  7582.51632      7674.0     7560     551922      7566  7628  7630    4207910038.42096   7624.1024       7629  47.1867     517852       5225      326104      34070    7674     7624.07     7628      7566   7560       7628      326104        6842     7566     7628     <NA>        <NA>      703665        5282        5019     <NA>\n"
        "2022-10-03   7617.6667   7681.7377     7460     427138      7514  7638  7640    3251555544.02803   7612.4188       7639   47.373     410624       5480      174454      16514    7680    7613.227     7640      7514   7460       7640      174454       11143     7514     7640     <NA>        <NA>      526075        5612        5234     <NA>\n"
        "2022-10-04  7574.02425   8023.4566     7378     578779      7658  7716  7718    4443587354.43106   7677.5139       7717  47.4475     519805       6738      207398      58974    7742     7662.27     7718      7658   7378       7718      207398        9203     7658     7718     <NA>        <NA>      666728        6868        6544     <NA>"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_NO_FIELDS
    )

    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_one_adc_field():
    expected_str = (
        "LSEG.L         Revenue\n" "Date                  \n" "2021-12-31  6740000000"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["TR.Revenue"])

    set_default(None)
    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_one_adc_field_use_field_names_in_headers():
    expected_str = (
        "LSEG.L      TR.Revenue\n" "date                  \n" "2021-12-31  6740000000"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_FIELD_NAMES_IN_HEADERS,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe="LSEG.L", fields=["TR.Revenue"], use_field_names_in_headers=True
    )
    set_default(None)
    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_one_pricing_field():
    expected_str = (
        "LSEG.L       BID\n"
        "Date            \n"
        "2022-09-06  7966\n"
        "2022-09-07  7944\n"
        "2022-09-08  8004\n"
        "2022-09-09  8004\n"
        "2022-09-12  8094\n"
        "2022-09-13  8004\n"
        "2022-09-14  7900\n"
        "2022-09-15  7800\n"
        "2022-09-16  7770\n"
        "2022-09-20  7542\n"
        "2022-09-21  7728\n"
        "2022-09-22  7468\n"
        "2022-09-23  7468\n"
        "2022-09-26  7632\n"
        "2022-09-27  7622\n"
        "2022-09-28  7692\n"
        "2022-09-29  7596\n"
        "2022-09-30  7628\n"
        "2022-10-03  7638\n"
        "2022-10-04  7716"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_PRICING_FIELD
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["BID"])
    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_one_adc_and_one_pricing_field():
    expected_str = (
        "LSEG.L     Currency   BID\n"
        "Date                     \n"
        "2022-08-18      GBP  <NA>\n"
        "2022-09-06     <NA>  7966\n"
        "2022-09-07     <NA>  7944\n"
        "2022-09-08     <NA>  8004\n"
        "2022-09-09     <NA>  8004\n"
        "2022-09-12     <NA>  8094\n"
        "2022-09-13     <NA>  8004\n"
        "2022-09-14     <NA>  7900\n"
        "2022-09-15     <NA>  7800\n"
        "2022-09-16     <NA>  7770\n"
        "2022-09-20     <NA>  7542\n"
        "2022-09-21     <NA>  7728\n"
        "2022-09-22     <NA>  7468\n"
        "2022-09-23     <NA>  7468\n"
        "2022-09-26     <NA>  7632\n"
        "2022-09-27     <NA>  7622\n"
        "2022-09-28     <NA>  7692\n"
        "2022-09-29     <NA>  7596\n"
        "2022-09-30     <NA>  7628\n"
        "2022-10-03     <NA>  7638\n"
        "2022-10-04     <NA>  7716"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_AND_ONE_PRICING_FIELD,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe="LSEG.L", fields=["TR.RevenueMean.currency", "BID"]
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_two_specific_adc_fields():
    expected_str = (
        "LSEG.L      Revenue - Mean Currency\n"
        "Date                               \n"
        "2022-08-18      7284197000      GBP"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_TWO_SPECIFIC_ADC_FIELDS
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe="LSEG.L", fields=["TR.RevenueMean", "TR.RevenueMean.currency"]
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_one_adc_field_with_intraday_interval():
    expected_str = (
        "LSEG.L         Revenue\n" "Date                  \n" "2021-12-31  6740000000"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_WITH_INTRADAY_INTERVAL,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["TR.Revenue"], interval="10min")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_one_pricing_field_with_intraday_interval():
    expected_str = (
        "LSEG.L                BID\n"
        "Timestamp                \n"
        "2022-10-05 12:30:00  7706\n"
        "2022-10-05 12:40:00  7710\n"
        "2022-10-05 12:50:00  7704\n"
        "2022-10-05 13:00:00  7690\n"
        "2022-10-05 13:10:00  7688\n"
        "2022-10-05 13:20:00  7714\n"
        "2022-10-05 13:30:00  7714\n"
        "2022-10-05 13:40:00  7710\n"
        "2022-10-05 13:50:00  7708\n"
        "2022-10-05 14:00:00  7710\n"
        "2022-10-05 14:10:00  7712\n"
        "2022-10-05 14:20:00  7720\n"
        "2022-10-05 14:30:00  7718\n"
        "2022-10-05 14:40:00  7728\n"
        "2022-10-05 14:50:00  7722\n"
        "2022-10-05 15:00:00  7734\n"
        "2022-10-05 15:10:00  7758\n"
        "2022-10-05 15:20:00  7764\n"
        "2022-10-05 15:30:00  7790\n"
        "2022-10-05 15:40:00  7790"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_PRICING_FIELD_WITH_INTRADAY_INT,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["BID"], interval="10min")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_one_adc_field_with_non_intraday_interval():
    expected_str = (
        "LSEG.L      Revenue - Mean\n"
        "Date                      \n"
        "2022-08-18      7284197000"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_ONE_ADC_FIELD_WITH_NON_INTRADAY_INT,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["TR.RevenueMean"], interval="1d")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_one_pricing_field_with_non_intraday_interval():
    expected_str = (
        "LSEG.L       BID\n"
        "Date            \n"
        "2022-09-07  7944\n"
        "2022-09-08  8004\n"
        "2022-09-09  8004\n"
        "2022-09-12  8094\n"
        "2022-09-13  8004\n"
        "2022-09-14  7900\n"
        "2022-09-15  7800\n"
        "2022-09-16  7770\n"
        "2022-09-20  7542\n"
        "2022-09-21  7728\n"
        "2022-09-22  7468\n"
        "2022-09-23  7468\n"
        "2022-09-26  7632\n"
        "2022-09-27  7622\n"
        "2022-09-28  7692\n"
        "2022-09-29  7596\n"
        "2022-09-30  7628\n"
        "2022-10-03  7638\n"
        "2022-10-04  7716\n"
        "2022-10-05  7788"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_ONE_INST_ONE_PRICING_FIELD_WITH_NON_INTRADAY_INT,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["BID"], interval="1d")

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_hist_one_inst_two_adc_two_hp_fields_non_intraday_int_start_end_date():
    expected_str = (
        "IBM                BID         ASK  Net Income after Tax  Revenue - Mean\n"
        "Date                                                                    \n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2019-12-31        <NA>        <NA>            7292000000            <NA>\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-16        <NA>        <NA>                  <NA>     73950729070\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2020-12-31        <NA>        <NA>            4042000000            <NA>\n"
        "2021-01-04  118.449888  118.459439                  <NA>            <NA>\n"
        "2021-01-05  120.513042    120.5608                  <NA>            <NA>\n"
        "2021-01-06  123.493154  123.512257                  <NA>            <NA>\n"
        "2021-01-07  123.206604  123.244811                  <NA>            <NA>\n"
        "2021-01-08  122.767229  122.805435                  <NA>            <NA>\n"
        "2021-01-11  122.824539  122.862745                  <NA>            <NA>\n"
        "2021-01-12  123.397637  123.407189                  <NA>     73959395730\n"
        "2021-01-12        <NA>        <NA>                  <NA>     73959395730\n"
        "2021-01-13  121.219863  121.229415                  <NA>            <NA>\n"
        "2021-01-14        <NA>        <NA>                  <NA>     73965995730\n"
        "2021-01-14  123.177949  123.187501                  <NA>     73965995730\n"
        "2021-01-15  122.623954  122.662161                  <NA>            <NA>\n"
        "2021-01-18        <NA>        <NA>                  <NA>     73987395730\n"
        "2021-01-18        <NA>        <NA>                  <NA>     73987395730\n"
        "2021-01-19  123.206604  123.235259                  <NA>            <NA>\n"
        "2021-01-20  124.190423  124.247733                  <NA>            <NA>\n"
        "2021-01-21  125.909718   125.91927                  <NA>     74726080400\n"
        "2021-01-22   113.28245  113.292002                  <NA>     74238533200\n"
        "2021-01-25        <NA>        <NA>                  <NA>     74191285570\n"
        "2021-01-25  113.253795  113.263347                  <NA>     74191285570\n"
        "2021-01-26  116.969383  116.988487                  <NA>            <NA>\n"
        "2021-01-27        <NA>        <NA>                  <NA>     74195199870\n"
        "2021-01-27        <NA>        <NA>                  <NA>     74195199870\n"
        "2021-01-27        <NA>        <NA>                  <NA>     74195199870\n"
        "2021-01-27  116.978935  117.103106                  <NA>     74195199870\n"
        "2021-01-28  114.686541  114.696093                  <NA>            <NA>\n"
        "2021-01-29  113.693171  113.702723                  <NA>            <NA>\n"
        "2021-02-01  115.078159  115.135469                  <NA>            <NA>"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HIST_ONE_INS_TWO_ADC_TWO_HP_NON_INTRADAY_INT_START_END_DATE,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe="IBM",
        fields=["BID", "ASK", "TR.F.NetIncAfterTax", "TR.RevenueMean"],
        interval="daily",
        start="2021-01-01",
        end="2021-02-01",
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_one_instrument_two_specific_pricing_fields():
    expected_str = (
        "LSEG.L       BID   ASK\n"
        "Date                  \n"
        "2022-09-07  7944  7946\n"
        "2022-09-08  8004  8006\n"
        "2022-09-09  8004  8010\n"
        "2022-09-12  8094  8098\n"
        "2022-09-13  8004  8006\n"
        "2022-09-14  7900  7902\n"
        "2022-09-15  7800  7802\n"
        "2022-09-16  7770  7786\n"
        "2022-09-20  7542  7548\n"
        "2022-09-21  7728  7730\n"
        "2022-09-22  7468  7470\n"
        "2022-09-23  7468  7470\n"
        "2022-09-26  7632  7634\n"
        "2022-09-27  7622  7624\n"
        "2022-09-28  7692  7696\n"
        "2022-09-29  7596  7598\n"
        "2022-09-30  7628  7630\n"
        "2022-10-03  7638  7640\n"
        "2022-10-04  7716  7718\n"
        "2022-10-05  7788  7790"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_ONE_INSTRUMENT_TWO_SPECIFIC_PRICING_FIELDS,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe="LSEG.L", fields=["BID", "ASK"])

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_two_instruments_without_fields():
    expected_str = (
        "              IBM.N                                                                                                                          EUR=                                                                                                                                                                                                                       \n"
        "           TRDPRC_1  HIGH_1   LOW_1 ACVOL_UNS OPEN_PRC     BID     ASK TRNOVR_UNS      VWAP BLKCOUNT BLKVOLUM NUM_MOVES TRD_STATUS SALTIM     BID     ASK BID_HIGH_1 BID_LOW_1 OPEN_BID MID_PRICE NUM_BIDS ASK_LOW_1 ASK_HIGH_1 ASIAOP_BID ASIAHI_BID ASIALO_BID ASIACL_BID EUROP_BID EURHI_BID EURLO_BID EURCL_BID AMEROP_BID AMERHI_BID AMERLO_BID AMERCL_BID OPEN_ASK\n"
        "Date                                                                                                                                                                                                                                                                                                                                                                    \n"
        "2022-09-28   122.76  123.22  119.81   1820304   121.65  122.71  122.72  222716495  122.3513        3   998710     10524          1  72600    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>       <NA>       <NA>       <NA>       <NA>      <NA>      <NA>      <NA>      <NA>       <NA>       <NA>       <NA>       <NA>     <NA>\n"
        "2022-09-29   121.63  122.56  120.58   1048410   122.26  121.68  121.71  127412543  121.5293        2   525500      7993          1  72600  0.9814  0.9818     0.9815    0.9634   0.9733    0.9816    96257    0.9636     0.9818     0.9733     0.9738     0.9634     0.9655    0.9684    0.9789    0.9634    0.9771     0.9713     0.9815     0.9682     0.9814   0.9737\n"
        "2022-09-30   118.81  122.43  118.61   2029911   121.66  118.83  118.92  242494240  119.4605        2  1133279     11289          1  72600  0.9799  0.9803     0.9853    0.9733   0.9815    0.9801    94060    0.9736     0.9856     0.9815     0.9844     0.9789     0.9832    0.9798    0.9853    0.9733    0.9781      0.976     0.9817     0.9733     0.9799   0.9818\n"
        "2022-10-03   121.51  122.21  119.63   1396140    120.2  121.51  121.56  169501789  121.4074        3   689575      9004          1  72600  0.9824  0.9827     0.9844    0.9751   0.9798   0.98255    97658    0.9754     0.9847     0.9798     0.9834     0.9782      0.981    0.9783    0.9844    0.9751    0.9806     0.9776     0.9844     0.9752     0.9824   0.9802\n"
        "2022-10-04    125.5  125.62  122.53   1444246    122.8  125.47   125.5  180658926  125.0887        2   681369     10240          1  72600  0.9983  0.9987     0.9999    0.9804   0.9825    0.9985    86112    0.9807     1.0002     0.9825     0.9895     0.9804     0.9873    0.9831    0.9979    0.9824    0.9974      0.989     0.9999     0.9875     0.9983   0.9827\n"
        "2022-10-05     <NA>    <NA>    <NA>      <NA>     <NA>    <NA>    <NA>       <NA>      <NA>     <NA>     <NA>      <NA>       <NA>   <NA>    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>     0.9984     0.9994     0.9934     0.9939      <NA>      <NA>      <NA>      <NA>       <NA>       <NA>       <NA>       <NA>     <NA>"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_TWO_INSTRUMENTS_WITHOUT_FIELDS
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(universe=["IBM.N", "EUR="], count=5)

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_two_instruments_one_adc_fields_quarterly_interval_start_date():
    expected_str = (
        "TR.F.NetIncAfterTax          IBM       MSFT.O\n"
        "date                                         \n"
        "2018-12-31           10760000000         <NA>\n"
        "2019-06-30                  <NA>  39397000000"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_TWO_INST_ONE_ADC_FIELDS_QUARTERLY_INT_START_DATE,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe=["IBM", "MSFT.O"],
        fields=["TR.F.NetIncAfterTax"],
        use_field_names_in_headers=True,
        interval="quarterly",
        start="2020-01-01",
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_two_instruments_two_pricing_fields_daily_interval_start_date():
    expected_str = (
        "              EUR=            GBP=        \n"
        "               BID     ASK     BID     ASK\n"
        "Date                                      \n"
        "2022-09-07  0.9999  1.0003  1.1525  1.1529\n"
        "2022-09-08  0.9994  0.9998    1.15  1.1504\n"
        "2022-09-09  1.0039  1.0043  1.1587  1.1591\n"
        "2022-09-12  1.0119  1.0122  1.1679  1.1688\n"
        "2022-09-13   0.997  0.9974  1.1491  1.1495\n"
        "2022-09-14  0.9977  0.9981  1.1535  1.1539\n"
        "2022-09-15  0.9999  1.0003  1.1463  1.1469\n"
        "2022-09-16  1.0015  1.0019  1.1412  1.1416\n"
        "2022-09-19  1.0022  1.0026  1.1429  1.1435\n"
        "2022-09-20   0.997  0.9974  1.1379  1.1383\n"
        "2022-09-21  0.9837  0.9839  1.1266   1.127\n"
        "2022-09-22  0.9836   0.984  1.1257  1.1261\n"
        "2022-09-23   0.969  0.9694  1.0856   1.086\n"
        "2022-09-26  0.9606  0.9609  1.0684  1.0688\n"
        "2022-09-27  0.9592  0.9596  1.0731  1.0734\n"
        "2022-09-28  0.9734  0.9737  1.0888  1.0892\n"
        "2022-09-29  0.9814  0.9818  1.1115  1.1119\n"
        "2022-09-30  0.9799  0.9803   1.116  1.1164\n"
        "2022-10-03  0.9824  0.9827  1.1322  1.1326\n"
        "2022-10-04  0.9983  0.9987  1.1473  1.1477"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_TWO_INS_TWO_HP_FIELDS_DAILY_INT_START_DATE,
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    result_df = get_history(
        universe=["EUR=", "GBP="],
        fields=["BID", "ASK"],
        interval="daily",
        start="2020-10-01",
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_two_instruments_adc_and_pricing_fields_1h_interval_field_names():
    expected_str = (
        "                      VOD.L                                             MSFT.O                                           \n"
        "                        BID     ASK TR.F.NetIncAfterTax TR.RevenueMean     BID     ASK TR.F.NetIncAfterTax TR.RevenueMean\n"
        "Timestamp                                                                                                                \n"
        "2022-03-31 00:00:00    <NA>    <NA>          2624000000           <NA>    <NA>    <NA>                <NA>           <NA>\n"
        "2022-06-30 00:00:00    <NA>    <NA>                <NA>           <NA>    <NA>    <NA>         72738000000           <NA>\n"
        "2022-10-04 00:00:00    <NA>    <NA>                <NA>            EUR    <NA>    <NA>                <NA>            USD\n"
        "2022-10-04 09:00:00   106.1  106.16                <NA>           <NA>   106.1  106.16                <NA>           <NA>\n"
        "2022-10-04 10:00:00  106.24   106.3                <NA>           <NA>  106.24   106.3                <NA>           <NA>\n"
        "2022-10-04 11:00:00  105.56   105.6                <NA>           <NA>  105.56   105.6                <NA>           <NA>\n"
        "2022-10-04 12:00:00  105.62  105.66                <NA>           <NA>  105.62  105.66                <NA>           <NA>\n"
        "2022-10-04 13:00:00  105.26   105.3                <NA>           <NA>  105.26   105.3                <NA>           <NA>\n"
        "2022-10-04 14:00:00  104.94  104.96                <NA>           <NA>  104.94  104.96                <NA>           <NA>\n"
        "2022-10-04 15:00:00  104.94  105.02                <NA>           <NA>  104.94  105.02                <NA>           <NA>\n"
        "2022-10-04 16:00:00   103.0   110.0                <NA>           <NA>   103.0   110.0                <NA>           <NA>\n"
        "2022-10-05 04:00:00   103.0   110.0                <NA>           <NA>   103.0   110.0                <NA>           <NA>\n"
        "2022-10-05 06:00:00  120.72   89.24                <NA>           <NA>  120.72   89.24                <NA>           <NA>\n"
        "2022-10-05 07:00:00   102.7  102.74                <NA>           <NA>   102.7  102.74                <NA>           <NA>\n"
        "2022-10-05 08:00:00  102.08  102.12                <NA>           <NA>  102.08  102.12                <NA>           <NA>\n"
        "2022-10-05 09:00:00  102.08   102.1                <NA>           <NA>  102.08   102.1                <NA>           <NA>\n"
        "2022-10-05 10:00:00  102.76   102.8                <NA>           <NA>  102.76   102.8                <NA>           <NA>\n"
        "2022-10-05 11:00:00   102.8  102.82                <NA>           <NA>   102.8  102.82                <NA>           <NA>\n"
        "2022-10-05 12:00:00  103.12  103.14                <NA>           <NA>  103.12  103.14                <NA>           <NA>\n"
        "2022-10-05 13:00:00  102.64   102.7                <NA>           <NA>  102.64   102.7                <NA>           <NA>\n"
        "2022-10-05 14:00:00  102.16   102.2                <NA>           <NA>  102.16   102.2                <NA>           <NA>\n"
        "2022-10-05 15:00:00  102.54  102.72                <NA>           <NA>  102.54  102.72                <NA>           <NA>\n"
        "2022-10-05 16:00:00  102.02   105.0                <NA>           <NA>  102.02   105.0                <NA>           <NA>"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_TWO_INST_ADC_AND_PRICING_FIELDS_1H_INT_FIELD_NAMES,
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=["VOD.L", "MSFT.O"],
        fields=["BID", "ASK", "TR.F.NetIncAfterTax", "TR.RevenueMean.currency"],
        interval="1h",
        use_field_names_in_headers=True,
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_two_insts_one_adc_field_two_hp_fields_int_tick_start_date():
    expected_str = (
        "                          IBM.N                        LSEG.L                     \n"
        "                            BID     ASK Revenue - Mean    BID   ASK Revenue - Mean\n"
        "Timestamp                                                                         \n"
        "2021-04-25 00:00:00.000    <NA>    <NA>    74397055190   <NA>  <NA>           <NA>\n"
        "2021-05-10 00:00:00.000    <NA>    <NA>           <NA>   <NA>  <NA>     6935640740\n"
        "2022-10-05 16:30:00.284    <NA>    <NA>           <NA>   7714  7810           <NA>\n"
        "2022-10-05 16:30:00.284    <NA>    <NA>           <NA>   7170  7820           <NA>\n"
        "2022-10-05 16:30:00.284    <NA>    <NA>           <NA>   7720  7810           <NA>\n"
        "2022-10-05 16:30:00.284    <NA>    <NA>           <NA>   7170  7810           <NA>\n"
        "2022-10-05 16:30:00.284    <NA>    <NA>           <NA>   7170  7816           <NA>\n"
        "2022-10-05 16:30:00.284    <NA>    <NA>           <NA>   7704  7810           <NA>\n"
        "2022-10-05 16:30:00.284    <NA>    <NA>           <NA>   7710  7810           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  8634           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  8580           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  8490           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  8470           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  8200           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  7886           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  7998           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  8746           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  7830           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  7824           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  8030           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  7834           <NA>\n"
        "2022-10-05 16:30:00.285    <NA>    <NA>           <NA>   7170  9000           <NA>\n"
        "2022-10-05 17:05:24.257  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.372  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.373  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.397  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.881  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.881  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.881  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.881  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.925  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.925  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.925  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.925  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:24.985  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:25.081  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:25.174  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:25.174  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:25.196  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:25.196  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:25.196  125.35  125.38           <NA>   <NA>  <NA>           <NA>\n"
        "2022-10-05 17:05:25.430  125.35  125.38           <NA>   <NA>  <NA>           <NA>"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True,
        response=td.RDP_GET_HISTORY_TWO_INSTS_ONE_ADC_TWO_HP_FIELDS_INT_TICK_START_DATE,
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=["IBM.N", "LSEG.L"],
        fields=["BID", "ASK", "TR.RevenueMean"],
        interval="tick",
        start="2021-05-11",
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_three_instruments_without_fields():
    expected_str = (
        "              IBM.N                                                                                                                           EUR=                                                                                                                                                                                                                        S)MyUSD.GESG1-150112\n"
        "           TRDPRC_1   HIGH_1   LOW_1 ACVOL_UNS OPEN_PRC     BID     ASK TRNOVR_UNS      VWAP BLKCOUNT BLKVOLUM NUM_MOVES TRD_STATUS SALTIM     BID     ASK BID_HIGH_1 BID_LOW_1 OPEN_BID MID_PRICE NUM_BIDS ASK_LOW_1 ASK_HIGH_1 ASIAOP_BID ASIAHI_BID ASIALO_BID ASIACL_BID EUROP_BID EURHI_BID EURLO_BID EURCL_BID AMEROP_BID AMERHI_BID AMERLO_BID AMERCL_BID OPEN_ASK             TRDPRC_1\n"
        "Date                                                                                                                                                                                                                                                                                                                                                                                          \n"
        "2022-09-07   127.71  127.855  126.28    771510   126.69  127.72  127.73   98346699   127.473        2   420909      4878          1  72600    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>       <NA>       <NA>       <NA>       <NA>      <NA>      <NA>      <NA>      <NA>       <NA>       <NA>       <NA>       <NA>     <NA>                 <NA>\n"
        "2022-09-08   128.47   128.51  126.59    911647   127.12  128.42  128.43  116797276  128.1168        2   465537      5751          1  72600  0.9994  0.9998     1.0029    0.9929   1.0001    0.9996    86338    0.9932     1.0032     1.0001     1.0014     0.9975      0.998    0.9988    1.0029    0.9929    0.9952     1.0008     1.0029     0.9929     0.9994   1.0003                 <NA>\n"
        "2022-09-09   129.19   129.49  128.07   1069094    128.9  129.21  129.22  138041202  129.1198        2   520062      6216          1  72600  1.0039  1.0043     1.0112    0.9993   0.9993    1.0041    76399    0.9997     1.0115     0.9993      1.011     0.9993     1.0096    1.0071    1.0112     1.003    1.0044     1.0073     1.0075      1.003     1.0039   0.9997                    3\n"
        "2022-09-12   130.66   130.99  129.91   1245309   130.33   130.7  130.71  162528528  130.5126        2   628490      6975          1  72600  1.0119  1.0122     1.0197    1.0058   1.0078   1.01205    62347    1.0061       1.02     1.0078     1.0197     1.0058     1.0174    1.0076    1.0197    1.0076    1.0124     1.0135     1.0162     1.0103     1.0119   1.0082                    3\n"
        "2022-09-13   127.25   129.82   126.8   1603709   129.14  127.23  127.25  205136259  127.9136        2   752373      9835          1  72600   0.997  0.9974     1.0187    0.9964   1.0121    0.9972    77655    0.9968     1.0189     1.0121     1.0155     1.0116     1.0145    1.0126    1.0187    0.9994    0.9996     1.0179     1.0187     0.9964      0.997   1.0125                    3\n"
        "2022-09-14   127.69    129.0  126.85   1286648    127.5  127.66  127.67  164386719  127.7636        3   725522      8149          1  72600  0.9977  0.9981     1.0023    0.9954   0.9967    0.9979    87677    0.9957     1.0026     0.9967     1.0002     0.9954     0.9986    0.9994    1.0023    0.9958    0.9992     1.0006     1.0009     0.9967     0.9977   0.9971                    3\n"
        "2022-09-15   125.49   127.39   124.9   1474804   127.39  125.49   125.5  185269243   125.623        3   705660     10066          1  72600  0.9999  1.0003     1.0017    0.9954   0.9979    1.0001    69080    0.9957      1.002     0.9979     0.9984     0.9954     0.9977    0.9967    1.0017    0.9954     0.999     0.9977     1.0017      0.997     0.9999   0.9982                    3\n"
        "2022-09-16   127.27   127.49  124.01   5408858   124.36  127.23  127.27  685427466  126.7231        2  4463300     10894          1  72600  1.0015  1.0019     1.0036    0.9943   0.9999    1.0017    72842    0.9946     1.0038     0.9999     1.0012     0.9943     0.9956    0.9995    1.0036    0.9943     1.001     0.9983     1.0036     0.9951     1.0015   1.0003                    3\n"
        "2022-09-19   127.73   128.06  126.28   1320203    126.5  127.69  127.73  168291147  127.4737        2   725956      7910          1  72600  1.0022  1.0026     1.0029    0.9964    1.001    1.0024    63178    0.9967     1.0031      1.001     1.0029     0.9964     0.9978    0.9992    1.0017    0.9964    1.0002     0.9992     1.0027     0.9974     1.0022   1.0014                    3\n"
        "2022-09-20    126.3    126.9  125.53    799630    126.9   126.3  126.31  100914959  126.2021        2   357706      7375          1  72600   0.997  0.9974      1.005    0.9953   1.0021    0.9972    72943    0.9956     1.0053     1.0021      1.005     1.0011     1.0034    1.0021    1.0041    0.9953    0.9992     1.0006     1.0013     0.9953      0.997   1.0025                    3\n"
        "2022-09-21   124.93   127.77  124.92   1096128   126.89  124.94  124.95  137967478   125.868        2   477129      8477          1  72600  0.9837  0.9839     0.9976    0.9812    0.997    0.9838    87445    0.9814      0.998      0.997     0.9976     0.9883     0.9909    0.9959    0.9968    0.9865    0.9878     0.9921     0.9925     0.9812     0.9837   0.9974                    3\n"
        "2022-09-22   125.31   126.49  124.45   1152042   124.76  125.31  125.32  144521845  125.4484        2   450245      9169          1  72600  0.9836   0.984     0.9907    0.9807   0.9836    0.9838   103843     0.981     0.9909     0.9836     0.9853     0.9807     0.9843    0.9828    0.9907     0.981    0.9838     0.9874     0.9887      0.981     0.9836   0.9838                    3\n"
        "2022-09-23   122.71   124.57  121.75   1555461   124.53  122.75  122.76  191160601  122.8964        2   684185     11039          1  72600   0.969  0.9694     0.9851    0.9666   0.9835    0.9692    90975    0.9669     0.9854     0.9835     0.9851     0.9765     0.9774    0.9821    0.9838      0.97    0.9716     0.9751     0.9774     0.9666      0.969   0.9839                    3\n"
        "2022-09-26   122.01   124.25  121.76   1287055    122.3   122.0  122.01  157505074  122.3763        2   593148      9160          1  72600  0.9606  0.9609     0.9709    0.9565   0.9678   0.96075   109840    0.9569     0.9712     0.9684     0.9709     0.9565     0.9676    0.9627    0.9701    0.9608    0.9621     0.9641     0.9689     0.9598     0.9606    0.968                    3\n"
        "2022-09-27   121.74   123.95  121.09   1335006    122.6  121.76  121.77  162900375  122.0222        2   559187     10219          1  72600  0.9592  0.9596      0.967    0.9567   0.9609    0.9594   104222     0.957     0.9673     0.9609      0.967     0.9583     0.9645    0.9635     0.967    0.9592    0.9612     0.9627     0.9652     0.9567     0.9592   0.9611                    3\n"
        "2022-09-28   122.76   123.22  119.81   1820304   121.65  122.71  122.72  222716495  122.3513        3   998710     10524          1  72600  0.9734  0.9737      0.975    0.9534   0.9592   0.97355   104438    0.9537     0.9753     0.9592       0.96     0.9534     0.9577    0.9549    0.9688    0.9534    0.9678     0.9574      0.975     0.9548     0.9734   0.9596                    3\n"
        "2022-09-29   121.63   122.56  120.58   1048410   122.26  121.68  121.71  127412543  121.5293        2   525500      7993          1  72600  0.9814  0.9818     0.9815    0.9634   0.9733    0.9816    96257    0.9636     0.9818     0.9733     0.9738     0.9634     0.9655    0.9684    0.9789    0.9634    0.9771     0.9713     0.9815     0.9682     0.9814   0.9737                    3\n"
        "2022-09-30   118.81   122.43  118.61   2029911   121.66  118.83  118.92  242494240  119.4605        2  1133279     11289          1  72600  0.9799  0.9803     0.9853    0.9733   0.9815    0.9801    94060    0.9736     0.9856     0.9815     0.9844     0.9789     0.9832    0.9798    0.9853    0.9733    0.9781      0.976     0.9817     0.9733     0.9799   0.9818                    3\n"
        "2022-10-03   121.51   122.21  119.63   1396140    120.2  121.51  121.56  169501789  121.4074        3   689575      9004          1  72600  0.9824  0.9827     0.9844    0.9751   0.9798   0.98255    97658    0.9754     0.9847     0.9798     0.9834     0.9782      0.981    0.9783    0.9844    0.9751    0.9806     0.9776     0.9844     0.9752     0.9824   0.9802                    3\n"
        "2022-10-04    125.5   125.62  122.53   1444246    122.8  125.47   125.5  180658926  125.0887        2   681369     10240          1  72600  0.9983  0.9987     0.9999    0.9804   0.9825    0.9985    86112    0.9807     1.0002     0.9825     0.9895     0.9804     0.9873    0.9831    0.9979    0.9824    0.9974      0.989     0.9999     0.9875     0.9983   0.9827                    3\n"
        "2022-10-05     <NA>     <NA>    <NA>      <NA>     <NA>    <NA>    <NA>       <NA>      <NA>     <NA>     <NA>      <NA>       <NA>   <NA>    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>     0.9984     0.9994     0.9934     0.9939    0.9965    0.9994    0.9833    0.9864       <NA>       <NA>       <NA>       <NA>     <NA>                    3\n"
        "2022-10-06     <NA>     <NA>    <NA>      <NA>     <NA>    <NA>    <NA>       <NA>      <NA>     <NA>     <NA>      <NA>       <NA>   <NA>    <NA>    <NA>       <NA>      <NA>     <NA>      <NA>     <NA>      <NA>       <NA>       <NA>       <NA>       <NA>       <NA>      <NA>      <NA>      <NA>      <NA>       <NA>       <NA>       <NA>       <NA>     <NA>                    3"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_THREE_INSTRUMENTS_WITHOUT_FIELDS
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(universe=["IBM.N", "EUR=", "S)MyUSD.GESG1-150112"])
    session.close()

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_eur_gpb_tick_interval():
    expected_str = (
        "                           EUR=            GBP=        \n"
        "                            BID     ASK     BID     ASK\n"
        "Timestamp                                              \n"
        "2022-10-05 19:22:49.503  0.9894  0.9898    <NA>    <NA>\n"
        "2022-10-05 19:22:51.650  0.9894  0.9898    <NA>    <NA>\n"
        "2022-10-05 19:22:55.501    <NA>    <NA>  1.1347  1.1354\n"
        "2022-10-05 19:22:55.520  0.9892  0.9896    <NA>    <NA>\n"
        "2022-10-05 19:22:55.533    <NA>    <NA>  1.1347  1.1351\n"
        "2022-10-05 19:22:56.204    <NA>    <NA>  1.1348   1.135\n"
        "2022-10-05 19:22:56.215  0.9894  0.9895    <NA>    <NA>\n"
        "2022-10-05 19:22:56.533  0.9892  0.9896    <NA>    <NA>\n"
        "2022-10-05 19:22:56.539    <NA>    <NA>  1.1347  1.1351\n"
        "2022-10-05 19:22:57.138    <NA>    <NA>   1.135  1.1351"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_EUR_GPB_TICK_INTERVAL
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=["EUR=", "GBP="], fields=["BID", "ASK"], interval="tick", count=5
    )

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_chain_one_adc_field_one_hp_field():
    expected_str = (
        "            BMA.BA             BBAR.BA             BHIP.BA        GGAL.BA             BPAT.BA             SUPV.BA        \n"
        "           Revenue         BID Revenue         BID Revenue    BID Revenue         BID Revenue         BID Revenue     BID\n"
        "Date                                                                                                                     \n"
        "2022-09-07    <NA>  440.919274    <NA>  309.236941    <NA>   12.7    <NA>  251.293376    <NA>  108.319731    <NA>   107.0\n"
        "2022-09-08    <NA>  438.433821    <NA>  309.435807    <NA>   12.5    <NA>       252.5    <NA>  108.319731    <NA>   108.0\n"
        "2022-09-09    <NA>  469.452268    <NA>  319.180251    <NA>  12.55    <NA>       264.3    <NA>  107.822852    <NA>   111.4\n"
        "2022-09-12    <NA>  465.276708    <NA>  313.711431    <NA>  12.35    <NA>       259.6    <NA>   109.31349    <NA>   110.5\n"
        "2022-09-13    <NA>  452.352355    <NA>  304.265286    <NA>   12.1    <NA>       250.1    <NA>  104.344695    <NA>   109.5\n"
        "2022-09-14    <NA>  474.224337    <NA>  313.214265    <NA>   12.2    <NA>       256.1    <NA>   109.31349    <NA>   113.0\n"
        "2022-09-15    <NA>   477.20688    <NA>   308.24261    <NA>   11.9    <NA>       258.0    <NA>  106.332213    <NA>  113.05\n"
        "2022-09-16    <NA>  487.049272    <NA>  313.711431    <NA>  11.85    <NA>       259.2    <NA>  108.816611    <NA>   113.0\n"
        "2022-09-19    <NA>  517.868883    <NA>  337.277075    <NA>   12.0    <NA>       270.7    <NA>       105.0    <NA>   114.0\n"
        "2022-09-20    <NA>  500.073043    <NA>  340.657801    <NA>  11.75    <NA>       268.3    <NA>       108.5    <NA>   113.5\n"
        "2022-09-21    <NA>  499.078862    <NA>  338.519989    <NA>   11.6    <NA>       267.6    <NA>       106.0    <NA>   114.0\n"
        "2022-09-22    <NA>   507.03231    <NA>  343.541361    <NA>  11.65    <NA>       269.5    <NA>      108.25    <NA>   113.1\n"
        "2022-09-23    <NA>  485.756837    <NA>  317.390455    <NA>   11.0    <NA>       257.3    <NA>      104.25    <NA>   112.0\n"
        "2022-09-26    <NA>  459.311622    <NA>  303.420105    <NA>  10.65    <NA>      242.35    <NA>       107.0    <NA>   107.6\n"
        "2022-09-27    <NA>  441.714618    <NA>   302.77379    <NA>  10.45    <NA>       228.9    <NA>       100.5    <NA>  106.55\n"
        "2022-09-28    <NA>  438.930912    <NA>  312.219934    <NA>   10.5    <NA>       233.4    <NA>       103.5    <NA>   107.0\n"
        "2022-09-29    <NA>   437.43964    <NA>  309.236941    <NA>  10.35    <NA>      230.55    <NA>       103.0    <NA>   105.4\n"
        "2022-09-30    <NA>       434.0    <NA>  312.219934    <NA>   10.6    <NA>       234.0    <NA>       105.5    <NA>  105.55\n"
        "2022-10-03    <NA>       475.5    <NA>       325.1    <NA>   11.0    <NA>       250.0    <NA>       107.5    <NA>   115.0\n"
        "2022-10-04    <NA>       479.0    <NA>       328.0    <NA>   11.1    <NA>       250.0    <NA>       108.5    <NA>   116.6"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_CHAIN_ONE_ADC_FIELD_ONE_HP_FIELD
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=[
            "SCREEN(U(IN(Equity(active,public,primary))/*UNV:Public*/), "
            'IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010"))'
        ],
        fields=["TR.Revenue", "BID"],
    )
    session.close()

    set_default(None)

    assert result_df.to_string() == expected_str


def test_rdp_get_history_chains_pricing_fields(monkeypatch):
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_CHAINS_PRICING_FIELDS
    )

    def mock_validate_responses(responses: list) -> list:
        """Cut first response to ADC."""
        responses = responses[1:]

    monkeypatch.setattr(
        "refinitiv.data.content._historical_data_provider.validate_responses",
        mock_validate_responses,
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=["0#.DJI"], fields=["BID", "ASK"], interval="1M", count=5
    )
    session.close()

    set_default(None)

    assert result_df.empty is True


def test_rdp_get_history_chains_adc_pricing_fields(monkeypatch):
    expected_str = (
        "              GS.N                     NKE.N                   CSCO.OQ                     JPM.N                      DIS.N                    INTC.OQ                    DOW.N                    MRK.N                     CVX.N                      AXP.N                      VZ.N                      HD.N                    WBA.OQ                     MCD.N                      UNH.N                      KO.N                     JNJ.N                    MSFT.OQ                     HON.OQ                      CRM.N                       PG.N                      IBM.N                      MMM.N                    AAPL.OQ                      WMT.N                      CAT.N                    AMGN.OQ                        V.N                      TRV.N                       BA.N                   \n"
        "               BID     ASK TR.REVENUE    BID    ASK TR.REVENUE     BID    ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID    ASK TR.REVENUE    BID    ASK TR.REVENUE    BID    ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE    BID    ASK TR.REVENUE     BID     ASK TR.REVENUE    BID    ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE    BID    ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE     BID     ASK TR.REVENUE\n"
        "Date                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  \n"
        "1990-03-23    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "1990-10-19    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "1991-10-09    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "1999-05-04    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2000-07-01    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2001-01-02    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2001-10-10    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2002-06-27    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2002-06-28    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2004-06-21    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2007-02-27    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2007-12-26    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2014-12-31    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2019-04-02    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2021-05-11    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>   <NA>       <NA>   <NA>   <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>   <NA>   <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>    <NA>    <NA>       <NA>\n"
        "2022-09-28  300.71  300.72       <NA>  98.66  98.67       <NA>   41.32  41.33       <NA>  108.04  108.05       <NA>   99.36    99.4       <NA>   27.11  27.12       <NA>  45.05  45.06       <NA>  86.78  86.79       <NA>  145.62  145.63       <NA>  140.46  140.49       <NA>  39.35  39.36       <NA>  282.19   282.2       <NA>  33.18  33.19       <NA>  236.89  236.94       <NA>  513.45  513.75       <NA>  56.97  56.98       <NA>  166.47  166.53       <NA>  241.02  241.03       <NA>   173.8  173.83       <NA>  150.17  150.18       <NA>  131.93  131.98       <NA>  122.71  122.72       <NA>  114.25  114.26       <NA>  149.79   149.8       <NA>  133.07  133.11       <NA>  167.69  167.74       <NA>  230.91  230.98       <NA>   179.1  179.24       <NA>  152.98  152.99       <NA>  133.36  133.37       <NA>\n"
        "2022-09-29  296.11  296.22       <NA>  95.49   95.5       <NA>   40.58  40.59       <NA>  106.17  106.18       <NA>   97.51   97.52       <NA>   26.38  26.39       <NA>  44.16  44.17       <NA>   86.7  86.71       <NA>  144.87  144.88       <NA>  137.82  137.87       <NA>  38.67  38.68       <NA>  278.09  278.17       <NA>  31.56  31.57       <NA>  234.33   234.4       <NA>  509.35  509.36       <NA>  56.58  56.59       <NA>  164.58  164.65       <NA>  237.51  237.54       <NA>   170.1  170.14       <NA>  146.92  146.95       <NA>  128.73  128.74       <NA>  121.68  121.71       <NA>  112.26  112.31       <NA>  142.59   142.6       <NA>  132.29  132.34       <NA>  166.06   166.1       <NA>  228.43  228.51       <NA>  180.07  180.13       <NA>  154.68  154.69       <NA>  125.39   125.4       <NA>\n"
        "2022-09-30  293.11  293.28       <NA>  83.11  83.12       <NA>   40.01  40.02       <NA>  104.61  104.67       <NA>   94.42   94.49       <NA>   25.78  25.79       <NA>  43.91  43.94       <NA>  86.17  86.21       <NA>  143.79   143.9       <NA>  134.94  135.02       <NA>  37.99  38.01       <NA>  276.38  276.63       <NA>   31.4  31.42       <NA>  230.84   231.0       <NA>  505.76  506.18       <NA>  56.07  56.08       <NA>  163.54  163.64       <NA>  232.81  232.84       <NA>  166.96  166.99       <NA>  143.98  144.02       <NA>  126.35  126.41       <NA>  118.83  118.92       <NA>  110.57  110.64       <NA>  138.08  138.18       <NA>  129.78  129.89       <NA>   164.1  164.17       <NA>  225.41  225.57       <NA>  177.74   177.9       <NA>  153.23  153.34       <NA>  121.21  121.26       <NA>\n"
        "2022-10-03  299.07  299.21       <NA>  85.39   85.4       <NA>   41.28   41.3       <NA>  107.72  107.73       <NA>   97.09    97.1       <NA>   26.95  26.96       <NA>  45.28  45.29       <NA>  87.55  87.59       <NA>  151.64  151.65       <NA>  139.99   140.0       <NA>  39.17  39.18       <NA>  283.69  283.88       <NA>  32.41  32.43       <NA>  235.26  235.33       <NA>  515.09   515.1       <NA>  56.65  56.66       <NA>  163.17  163.22       <NA>  240.65  240.67       <NA>  173.03  173.04       <NA>   147.8  147.85       <NA>   128.5  128.51       <NA>  121.51  121.56       <NA>  113.18  113.19       <NA>  142.43  142.45       <NA>  132.53  132.54       <NA>   171.4  171.41       <NA>  230.43  230.52       <NA>  181.59  181.69       <NA>  157.04   157.1       <NA>  125.99  126.02       <NA>\n"
        "2022-10-04  315.04  315.05       <NA>  88.66  88.68       <NA>   41.82  41.83       <NA>  112.79   112.8       <NA>  101.44  101.47       <NA>   27.69   27.7       <NA>  46.62  46.63       <NA>  88.39   88.4       <NA>  157.55  157.56       <NA>  145.47  145.51       <NA>  39.81  39.82       <NA>  289.75  289.76       <NA>  33.38  33.39       <NA>   238.5  238.51       <NA>  522.84  523.16       <NA>  56.78   56.8       <NA>  165.61  165.63       <NA>  248.88   248.9       <NA>  178.19  178.29       <NA>  155.82  155.85       <NA>  130.18  130.19       <NA>  125.47   125.5       <NA>  115.58  115.59       <NA>  146.16  146.17       <NA>   134.3  134.31       <NA>  179.76  179.79       <NA>  233.04  233.05       <NA>   185.7  185.77       <NA>  161.46  161.51       <NA>  133.49  133.53       <NA>"
    )
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_CHAINS_PRICING_FIELDS
    )

    def mock_validate_responses(responses: list) -> list:
        """Cut first response to ADC."""
        responses = responses[1:]

    monkeypatch.setattr(
        "refinitiv.data.content._historical_data_provider.validate_responses",
        mock_validate_responses,
    )

    session.type = SessionType.DESKTOP
    set_default(session)
    result_df = get_history(
        universe=["0#.DJI"], fields=["BID", "ASK", "TR.Revenue"], count=5
    )
    session.close()

    set_default(None)

    assert result_df.to_string() == expected_str


def test_hp_one_universe_two_fields():
    expected_str = (
        "EUR=           BID     ASK\n"
        "Date                      \n"
        "2022-09-20   0.997  0.9974\n"
        "2022-09-21  0.9837  0.9839\n"
        "2022-09-22  0.9836   0.984\n"
        "2022-09-23   0.969  0.9694\n"
        "2022-09-26  0.9606  0.9609"
    )
    session = StubSession(is_open=True, response=td.HP_ONE_UNIVERSE_TWO_FIELDS)
    session.type = SessionType.DESKTOP
    set_default(session)

    # when
    testing_df = get_history(
        universe=["EUR="],
        fields=[
            "BID",
            "ASK",
        ],
        start="2020-10-01",
        interval="daily",
        count=5,
    )

    set_default(None)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str


def test_hp_two_universes_one_field():
    expected_str = (
        "BID           EUR=   VOD.L\n"
        "Date                      \n"
        "2022-09-20   0.997  106.38\n"
        "2022-09-21  0.9837  108.78\n"
        "2022-09-22  0.9836  108.84\n"
        "2022-09-23   0.969  108.12\n"
        "2022-09-26  0.9606  106.66"
    )
    session = StubSession(is_open=True, response=td.HP_TWO_UNIVERSES_ONE_FIELD)
    session.type = SessionType.DESKTOP
    set_default(session)

    # when
    testing_df = get_history(
        universe=["EUR=", "VOD.L"],
        fields=["BID"],
        start="2020-10-01",
        interval="daily",
        count=5,
    )

    set_default(None)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str


def test_custom_inst_one_universe_two_fields():
    expected_str = (
        "S)Batman_df3fe62e.GESG1-111923   BID   ASK\n"
        "Date                                      \n"
        "2022-09-26                      <NA>  <NA>\n"
        "2022-09-23                      <NA>  <NA>\n"
        "2022-09-22                      <NA>  <NA>\n"
        "2022-09-21                      <NA>  <NA>\n"
        "2022-09-20                      <NA>  <NA>"
    )
    session = StubSession(is_open=True, response=td.CUSTOM_INST_ONE_UNIVERSE_TWO_FIELDS)
    session.type = SessionType.DESKTOP
    set_default(session)

    # when
    testing_df = get_history(
        universe=["S)Batman_df3fe62e.GESG1-111923"],
        fields=[
            "BID",
            "ASK",
        ],
        start="2020-10-01",
        interval="daily",
        count=5,
    )

    set_default(None)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str


def test_custom_inst_two_universes_one_field():
    expected_str = (
        "BID         S)Batman_df3fe62e.GESG1-111923  S)Batman_92734226.GESG1-111923\n"
        "Date                                                                      \n"
        "2022-09-26                            <NA>                            <NA>\n"
        "2022-09-23                            <NA>                            <NA>\n"
        "2022-09-22                            <NA>                            <NA>\n"
        "2022-09-21                            <NA>                            <NA>\n"
        "2022-09-20                            <NA>                            <NA>"
    )
    session = StubSession(is_open=True, response=td.CUSTOM_INST_TWO_UNIVERSES_ONE_FIELD)
    session.type = SessionType.DESKTOP
    set_default(session)

    # when
    testing_df = get_history(
        universe=["S)Batman_df3fe62e.GESG1-111923", "S)Batman_92734226.GESG1-111923"],
        fields=["BID"],
        start="2020-10-01",
        interval="daily",
        count=5,
    )

    set_default(None)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str


def test_no_request_to_adc_if_universe_expander_and_pricing_fields():
    no_request_to_adc = True

    def check_if_no_adc_request(request: Request):
        nonlocal no_request_to_adc
        url = request.url or ""
        if url == "test_get_udf_url_root":
            no_request_to_adc = False
        return StubResponse()

    session = StubSession(is_open=True)
    session.config.set_param("apis.data.datagrid.underlying-platform", "udf")
    session.http_request = check_if_no_adc_request
    set_default(session)

    peers = Peers("VOD.L")
    peers._universe = ["universe1", "universe2"]

    get_history(universe=peers, fields=["bid", "ask"])
    assert no_request_to_adc

    session.close()


def test_get_history_merge_duplicate_rows_rdp():
    """This is just the edge case for particular set of universes."""
    expected_str = (
        "Close Price  D-PCAQE00  D-WTMYA00  D-AAYAN00  D-AALVZ00\n"
        "Date                                                   \n"
        "2022-11-01       96.92      96.91      89.43     -6.825\n"
        "2022-11-02       96.79      98.15      90.18     -6.675\n"
        "2022-11-03       96.23      98.14      90.22     -6.625\n"
        "2022-11-04       98.43      99.99      91.85     -6.795\n"
        "2022-11-07       99.38     101.06      92.96       -7.3\n"
        "2022-11-08        99.0     101.14      93.31      -7.38\n"
        "2022-11-09       96.67      98.22      90.81     -7.555\n"
        "2022-11-10       94.12      95.21      88.49     -7.755\n"
        "2022-11-11       97.77      98.33       91.5     -7.995\n"
        "2022-11-14       97.97      98.63      91.82     -8.045\n"
        "2022-11-15       94.17       95.0      89.46     -8.305\n"
        "2022-11-15       94.17       95.0      89.46     -8.305"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_MERGE_DUPLICATE_ROWS
    )
    session.type = SessionType.PLATFORM
    set_default(session)

    testing_df = get_history(
        universe=["D-PCAQE00", "D-WTMYA00", "D-AAYAN00", "D-AALVZ00"],
        fields=["TR.CLOSEPRICE"],
        interval="1D",
        start="2022-11-01",
        end="2022-11-16",
    )

    set_default(None)

    testing_str = testing_df.to_string()
    assert testing_str == expected_str


def test_get_history_merge_duplicate_rows_rdp_without_one_item():
    expected_str = (
        "Close Price  D-PCAQE00  D-WTMYA00  D-AAYAN00  D-AALVZ00\n"
        "Date                                                   \n"
        "2022-11-01       96.92      96.91      89.43     -6.825\n"
        "2022-11-02       96.79      98.15      90.18     -6.675\n"
        "2022-11-03       96.23      98.14      90.22     -6.625\n"
        "2022-11-04       98.43      99.99      91.85     -6.795\n"
        "2022-11-07       99.38     101.06      92.96       -7.3\n"
        "2022-11-08        99.0     101.14      93.31      -7.38\n"
        "2022-11-09       96.67      98.22      90.81     -7.555\n"
        "2022-11-10       94.12      95.21      88.49     -7.755\n"
        "2022-11-11       97.77      98.33       91.5     -7.995\n"
        "2022-11-14       97.97      98.63      91.82     -8.045\n"
        "2022-11-15       94.17       95.0      89.46     -8.305\n"
        "2022-11-15       94.17       95.0      89.46       <NA>"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_MERGE_DUPLICATE_ROWS_WITHOUT_ONE_ITEM
    )
    session.type = SessionType.PLATFORM
    set_default(session)

    testing_df = get_history(
        universe=["D-PCAQE00", "D-WTMYA00", "D-AAYAN00", "D-AALVZ00"],
        fields=["TR.CLOSEPRICE"],
        interval="1D",
        start="2022-11-01",
        end="2022-11-16",
    )

    set_default(None)

    testing_str = testing_df.to_string()
    assert testing_str == expected_str


def test_get_history_manages_rics_with_special_characters_udf():
    expected_str = (
        "            aUSCXTRF/C  aUSCXTWF/C USPMI=ECI\n"
        "                 VALUE       VALUE     VALUE\n"
        "Date                                        \n"
        "2021-03-31   116.17654  115.671743      63.7\n"
        "2021-04-30  115.837235  115.230086      60.6\n"
        "2021-05-31  114.801921  113.222264      61.6\n"
        "2021-06-30  115.878533  114.108019      60.9\n"
        "2021-07-31   117.46647  116.159685      59.9\n"
        "2021-08-31  117.864694  116.539961      59.7\n"
        "2021-09-30  118.072946  116.885827      60.5\n"
        "2021-10-31  119.058262  117.323266      60.8\n"
        "2021-11-30  120.214056  118.798192      60.6\n"
        "2021-12-31  121.422381  120.100519      58.8\n"
        "2022-01-31  120.802911  119.467948      57.6\n"
        "2022-02-28  121.015568  119.683503      58.6\n"
        "2022-03-31   122.53071   121.75304      57.1\n"
        "2022-04-30  123.164167  123.984411      55.4\n"
        "2022-05-31  126.220662  127.020842      56.1\n"
        "2022-06-30  127.430749  127.534757      53.0\n"
        "2022-07-31  129.471313  130.698946      52.8\n"
        "2022-08-31  128.915166  130.522793      52.8\n"
        "2022-09-30  132.119783  134.972326      50.9\n"
        "2022-10-31  133.974891  136.973045      50.2"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "udf")
    session = StubSession(
        is_open=True, response=td.UDF_GET_HISTORY_MANAGE_RICS_WITH_SPECIAL_CHARACTERS
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    testing_df = get_history(["aUSCXTRF/C", "aUSCXTWF/C", "USPMI=ECI"])

    set_default(None)
    testing_str = testing_df.to_string()
    assert testing_str == expected_str


def test_get_history_manages_rics_with_special_characters_rdp():
    expected_str = (
        "            aUSCXTRF/C  aUSCXTWF/C USPMI=ECI\n"
        "                 VALUE       VALUE     VALUE\n"
        "Date                                        \n"
        "2021-03-31   116.17654  115.671743      63.7\n"
        "2021-04-30  115.837235  115.230086      60.6\n"
        "2021-05-31  114.801921  113.222264      61.6\n"
        "2021-06-30  115.878533  114.108019      60.9\n"
        "2021-07-31   117.46647  116.159685      59.9\n"
        "2021-08-31  117.864694  116.539961      59.7\n"
        "2021-09-30  118.072946  116.885827      60.5\n"
        "2021-10-31  119.058262  117.323266      60.8\n"
        "2021-11-30  120.214056  118.798192      60.6\n"
        "2021-12-31  121.422381  120.100519      58.8\n"
        "2022-01-31  120.802911  119.467948      57.6\n"
        "2022-02-28  121.015568  119.683503      58.6\n"
        "2022-03-31   122.53071   121.75304      57.1\n"
        "2022-04-30  123.164167  123.984411      55.4\n"
        "2022-05-31  126.220662  127.020842      56.1\n"
        "2022-06-30  127.430749  127.534757      53.0\n"
        "2022-07-31  129.471313  130.698946      52.8\n"
        "2022-08-31  128.915166  130.522793      52.8\n"
        "2022-09-30  132.119783  134.972326      50.9\n"
        "2022-10-31  133.974891  136.973045      50.2"
    )

    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(
        is_open=True, response=td.RDP_GET_HISTORY_MANAGE_RICS_WITH_SPECIAL_CHARACTERS
    )
    session.type = SessionType.DESKTOP
    set_default(session)

    testing_df = get_history(["aUSCXTRF/C", "aUSCXTWF/C", "USPMI=ECI"])

    set_default(None)
    testing_str = testing_df.to_string()
    assert testing_str == expected_str


def test_get_history_missed_data_rdp():
    expected_str = "Empty DataFrame\n" "Columns: [USPMI=ECI, D-PCAQE00]\n" "Index: []"
    get_config().set_param("apis.data.datagrid.underlying-platform", "rdp")
    session = StubSession(is_open=True, response=td.RDP_GET_HISTORY_MISSED_DATA)
    session.type = SessionType.DESKTOP
    set_default(session)

    testing_df = get_history(
        universe=["USPMI=ECI", "D-PCAQE00"],
        fields=["VALUE", "TR.CLOSEPRICE"],
        interval="1D",
        start="2022-10-01",
        end="2022-12-14",
    )

    set_default(None)
    testing_str = testing_df.to_string()
    assert testing_df.empty is True
    assert testing_str == expected_str


def test_get_history_parameters():
    test_sdate = "test_value"

    def http_request(request):
        assert (
            get_from_path(request.json, "Entity.W.requests.0.parameters.SDate")
            == test_sdate
        )

    session = StubSession(is_open=True)
    session.type = SessionType.DESKTOP
    set_default(session)
    session.http_request = http_request

    get_history(
        universe=["USPMI=ECI", "D-PCAQE00"],
        fields=["VALUE", "TR.CLOSEPRICE"],
        interval="1D",
        start="2022-10-01",
        end="2022-12-14",
        parameters={"SDate": test_sdate},
    )
