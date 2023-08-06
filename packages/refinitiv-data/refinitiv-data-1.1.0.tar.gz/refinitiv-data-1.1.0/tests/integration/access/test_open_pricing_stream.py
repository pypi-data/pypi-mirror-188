from time import sleep

import allure
import pytest

from refinitiv.data import open_pricing_stream
from refinitiv.data.discovery import Peers, Screener, Chain
from tests.integration.access.conftest import (
    check_stream_opened,
    check_stream_closed,
    check_stream_snapshot,
    check_stream_universe,
    check_stream_fields,
    check_triggered_events,
)
from tests.integration.helpers import check_the_number_of_items_in_dataframe


@allure.suite("FinCoder layer")
@allure.feature("FinCoder - Open Pricing Stream")
@allure.severity(allure.severity_level.CRITICAL)
class TestOpenPricingStream:
    @allure.title("Open pricing stream - no universe and fields")
    @pytest.mark.caseid("C38695920")
    def test_open_pricing_stream_no_universe_and_fields(self):
        with pytest.raises(TypeError) as error:
            open_pricing_stream()
        assert (
            str(error.value)
            == "open_pricing_stream() missing 1 required positional argument: 'universe'"
        )

    @allure.title("Open pricing stream - with universe and fields")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "universe, fields",
        [("GBP=", "BID"), (["USD=", "GBP=", "JPY="], ["BID", "ASK"])],
    )
    @pytest.mark.caseid("C38695923")
    def test_open_pricing_stream_with_universe_and_fields(
        self, open_desktop_session, universe, fields
    ):
        callback_history = []
        stream = open_pricing_stream(
            universe,
            fields,
            on_data=lambda data, ric, stream: callback_history.append(data),
        )
        check_stream_opened(stream)
        sleep(3)
        check_stream_universe(stream, universe)
        check_stream_fields(stream, universe, fields)
        stream.close()
        check_stream_closed(stream)
        check_triggered_events(callback_history, universe)

    @allure.title("Open pricing stream - get snapshot with universe and fields")
    @pytest.mark.parametrize(
        "universe, fields", ((["USD=", "AUD=", "CAD="], ["BID", "ASK", "OPEN_PRC"]),)
    )
    @pytest.mark.caseid("C38695960")
    def test_open_pricing_stream_snapshot_with_universe_and_fields(
        self, open_desktop_session, universe, fields
    ):
        stream = open_pricing_stream(
            universe,
            fields,
        )
        check_stream_opened(stream)
        check_stream_snapshot(stream, universe[:2], fields[:2])

    @allure.title("Open pricing stream - get snapshot with wrong universe and fields")
    @pytest.mark.parametrize(
        "universe, fields, err_msg_universe, err_msg_fields",
        (
            (
                ["USD=", "AUD=", "CAD="],
                ["BID", "ASK", "OPEN_PRC"],
                "Error code -1 | Instrument {'BYN='} was not requested",
                "Error code -1 | Field {'MID_CLOSE'} was not requested",
            ),
        ),
    )
    @pytest.mark.caseid("C38695961")
    def test_open_pricing_stream_snapshot_with_wrong_universe(
        self,
        capsys,
        open_desktop_session,
        universe,
        fields,
        err_msg_universe,
        err_msg_fields,
    ):
        stream = open_pricing_stream(universe, fields)
        check_stream_opened(stream)
        df = stream.get_snapshot("BYN=")
        test_log = capsys.readouterr()
        assert df.empty, f"Snapshot dataframe with wrong universe should be empty"
        assert (
            err_msg_universe in test_log.err
        ), f"Message '{err_msg_universe}' wasn't found in log"

        df = stream.get_snapshot("USD=", ["MID_CLOSE"])
        test_log = capsys.readouterr()
        assert df.empty, f"Snapshot dataframe with wrong fields should be empty"
        assert (
            err_msg_fields in test_log.err
        ), f"Message '{err_msg_fields}' wasn't found in log"

    @allure.title("Open pricing stream - with function and chain as universe")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "universe, fields, expected_universe",
        [
            (Peers("VOD.L"), "BID", "CLNX.MC"),
            pytest.param(Chain("0#.DJI"), None, ["IBM.N", "CSCO.OQ"], id="chain"),
            (
                Screener(
                    'U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010")'
                ),
                ["BID", "ASK"],
                ["BMA.BA", "BBAR.BA", "BHIP.BA"],
            ),
        ],
    )
    @pytest.mark.caseid("C43874350")
    def test_open_pricing_stream_with_function_and_chain_as_universe(
        self,
        request,
        open_desktop_session,
        universe,
        fields,
        expected_universe,
    ):
        stream = open_pricing_stream(
            universe,
            fields,
        )
        check_stream_opened(stream)
        sleep(1)
        check_stream_universe(stream, expected_universe)
        check_stream_fields(stream, expected_universe, fields)

        if "chain" in request.node.callspec.id:
            df = stream.get_snapshot()
            list_of_instruments = list(df["Instrument"])
            check_the_number_of_items_in_dataframe(
                expected_universe[0], list_of_instruments, 1
            )
        stream.close()
        check_stream_closed(stream)

    @allure.title("Open pricing stream - with CustomInstrument objects")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "universe,expected_fields",
        [
            (
                ["EUR=", "GBP="],
                ["BID", "ASK", "TRDPRC_1", "TRADE_DATE", "SALTIM_NS"],
            ),
            (None, ["TRDPRC_1", "TRADE_DATE", "SALTIM_NS"]),
        ],
        ids=["universe_mix", "ci_multi_universe"],
    )
    @pytest.mark.caseid("C43973497")
    def test_open_pricing_stream_with_custom_instrument_objects(
        self,
        open_desktop_session,
        create_instrument,
        universe,
        expected_fields,
        request,
    ):
        fields = []
        symbol_01 = create_instrument()
        symbol_02 = create_instrument()
        if "universe_mix" in request.node.callspec.id:
            universe += [symbol_01, symbol_02]
            fields = expected_fields
        if "ci_multi_universe" in request.node.callspec.id:
            universe = [symbol_01, symbol_02]

        callback_history = []
        stream = open_pricing_stream(
            universe=universe,
            fields=fields,
            on_data=lambda data, ric, stream_item: callback_history.append(data),
        )
        check_stream_opened(stream)
        sleep(2)
        check_stream_universe(stream, universe)
        check_stream_fields(stream, universe, expected_fields)
        stream.close()
        check_stream_closed(stream)
        check_triggered_events(callback_history, universe)
