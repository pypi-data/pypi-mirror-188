import time

import allure
import pytest

import refinitiv.data as rd
from refinitiv.data.content import trade_data_service
from tests.integration.content.trade_data_service.conftest import (
    create_trade_data_service_with_all_callbacks,
    check_triggered_event_list,
)

ONE_SEC = 1


@allure.suite("Content object - Trade Data Service")
@allure.feature("Content object - Trade Data Service")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("tds")
class TestTradeDataService:
    @allure.title("Create TDS object when session is not open")
    @pytest.mark.parametrize("universe", [["U1"]])
    @pytest.mark.caseid("33468307")
    def test_create_tds_when_session_is_not_open(self, universe):
        with pytest.raises(
            AttributeError,
            match="No default session created yet. Please create a session first!",
        ):
            rd.session.set_default(None)
            stream = create_trade_data_service_with_all_callbacks(universe=universe)
            stream.open()

    @allure.title("Create TDS object in session with default values")
    @pytest.mark.parametrize("universe", [["U1"]])
    @pytest.mark.caseid("33466883")
    def test_open_trade_data_service_with_default_values(self, universe, open_session):
        triggered_events_list = []
        stream = create_trade_data_service_with_all_callbacks(
            universe=universe,
            api="streaming.trading-analytics.endpoints.redi",
            session=open_session,
            triggered_events_list=triggered_events_list,
        )
        stream.open()
        time.sleep(ONE_SEC)
        stream.close()
        check_triggered_event_list(triggered_events_list)

    @allure.title(
        "Create TDS object in session with a specific universe name and without specifying fields"
    )
    @pytest.mark.parametrize("universe", [["U1"]])
    @pytest.mark.caseid("33466895")
    @pytest.mark.smoke
    def test_create_tds_object_by_specific_universe(self, universe, open_session):
        triggered_events_list = []
        stream = create_trade_data_service_with_all_callbacks(
            universe=universe,
            session=open_session,
            triggered_events_list=triggered_events_list,
        )
        stream.open()

        actual_fields_list = stream._stream._headers_ids
        actual_universe = stream._stream._universe

        assert (
            len(actual_fields_list) == 57
        ), f"Actual fields length = {len(actual_fields_list)}"
        assert (
            actual_universe == universe
        ), f"Universe not found, {actual_universe} != {universe}"

    @allure.title("Create TDS object in session before closing session")
    @pytest.mark.parametrize("universe", [["U1"]])
    @pytest.mark.caseid("33466895")
    def test_create_tds_in_session_before_closing_session(self, universe, open_session):
        with pytest.raises(AssertionError, match="Session must be open"):
            session = open_session
            stream = create_trade_data_service_with_all_callbacks(
                universe=universe,
                session=open_session,
            )
            session.close()
            stream.open()

    @allure.title(
        "Create TDS object in session with default values and without any parameters"
    )
    @pytest.mark.caseid("C33466888")
    def test_open_trade_data_service_without_any_params(self, open_platform_session):
        stream = trade_data_service.Definition().get_stream(
            session=open_platform_session
        )
        stream.open()
        time.sleep(ONE_SEC)
        assert stream._stream.state.name == "Opened"

    @allure.title(
        "Stop listening closed TDS stream on session and keep retrieving data for active stream"
    )
    @pytest.mark.parametrize("universe", [["U2"]])
    @pytest.mark.caseid("33468283")
    def test_keep_retrieving_data_for_active_stream(self, universe, open_session):
        triggered_events_list_01 = []
        stream_01 = create_trade_data_service_with_all_callbacks(
            universe=universe,
            universe_type=trade_data_service.UniverseTypes.RIC,
            session=open_session,
            triggered_events_list=triggered_events_list_01,
        )
        stream_01.open()

        triggered_events_list_02 = []
        stream_02 = create_trade_data_service_with_all_callbacks(
            universe=universe,
            universe_type=trade_data_service.UniverseTypes.UserID,
            session=open_session,
            triggered_events_list=triggered_events_list_02,
        )
        stream_02.open()
        stream_01.close()
        time.sleep(ONE_SEC)
        check_triggered_event_list(triggered_events_list_02)
        stream_02.close()

    @allure.title(
        "Receiving TDS data when the session was interrupted during the process"
    )
    @pytest.mark.parametrize("universe", [[]])
    @pytest.mark.caseid("33468321")
    def test_receiving_tds_when_session_was_interrupted(self, universe, open_session):
        with pytest.raises(AssertionError, match="Session must be open"):
            session = open_session
            stream = trade_data_service.Definition(
                universe=universe,
                finalized_orders=trade_data_service.FinalizedOrders.P1D,
                events=trade_data_service.Events.Full,
            ).get_stream(session=open_session)
            stream.open()
            session.close()
            stream.open()

    @allure.title(
        "Create TDS object in session with a specific universe name, fields and extended params"
    )
    @pytest.mark.parametrize(
        "universe,extended_fields",
        [(["U1"], ["InstrumentLongName", "OrderLifeDuration"])],
    )
    @pytest.mark.caseid("33468337")
    def test_create_trade_data_service_with_extended_params(
        self, universe, extended_fields, open_session
    ):
        stream = create_trade_data_service_with_all_callbacks(
            universe=universe,
            fields=["PrimaryListedRIC"],
            session=open_session,
            universe_type=trade_data_service.UniverseTypes.UserID,
            extended_params={"universe": ["U2"], "view": extended_fields},
        )
        stream.open()
        time.sleep(ONE_SEC)

        actual_fields_list = stream._stream._headers_ids

        assert (
            len(actual_fields_list) == 3
        ), f"Actual fields length = {len(actual_fields_list)}"
        for fields in extended_fields:
            assert fields in actual_fields_list, f"{fields} not in {actual_fields_list}"

        stream.close()

    @allure.title(
        "Checking the receipt of data using the user type RIC, UserID or Symbol"
    )
    @pytest.mark.parametrize(
        "universe,universe_type",
        [
            (["INUV"], trade_data_service.UniverseTypes.RIC),
            (["U10"], trade_data_service.UniverseTypes.UserID),
            (["MARA"], trade_data_service.UniverseTypes.Symbol),
        ],
    )
    @pytest.mark.caseid("")
    def test_checking_the_receipt_of_data_using_the_user_type_ric_or_symbol(
        self, universe, universe_type, open_session
    ):
        triggered_events_list = []
        stream = create_trade_data_service_with_all_callbacks(
            universe=universe,
            fields=["OrderKey", "InstrumentId", "PrimaryListedRIC", "CompositeRIC"],
            session=open_session,
            universe_type=universe_type,
            triggered_events_list=triggered_events_list,
        )
        stream.open()
        time.sleep(ONE_SEC)
        stream.close()
        check_triggered_event_list(triggered_events_list)

    @allure.title("Checking that no data was received when using an invalid user type")
    @pytest.mark.parametrize(
        "universe,universe_type",
        [
            (["AAPL.OQ"], trade_data_service.UniverseTypes.Symbol),
            # (["AAPL"], trade_data_service.UniverseTypes.UserID),
            (["U1"], trade_data_service.UniverseTypes.Symbol),
            (["U1"], trade_data_service.UniverseTypes.RIC),
        ],
    )
    @pytest.mark.caseid("")
    def test_checking_that_no_data_was_received(
        self, universe, universe_type, open_session
    ):
        triggered_events_list = []
        stream = create_trade_data_service_with_all_callbacks(
            universe=universe,
            session=open_session,
            universe_type=universe_type,
            triggered_events_list=triggered_events_list,
        )
        stream.open()
        time.sleep(ONE_SEC)
        stream.close()
        check_triggered_event_list(triggered_events_list)

    @pytest.mark.caseid("")
    @allure.title("Create trade data service stream with invalid api parameter")
    @pytest.mark.parametrize(
        "universe,universe_type",
        [
            (["U1"], trade_data_service.UniverseTypes.Symbol),
        ],
    )
    def test_create_trade_data_service_with_invalid_api(
        self, open_desktop_session, universe, universe_type
    ):
        with pytest.raises(ValueError) as error:
            stream = create_trade_data_service_with_all_callbacks(
                api="streaming.trading-analytics.endpoints.invalid",
                universe=universe,
                session=open_desktop_session,
                universe_type=universe_type,
            )
            stream.open()
        assert (
            str(error.value)
            == "Not an existing path apis.streaming.trading-analytics.endpoints.invalid to url into config file"
        )
