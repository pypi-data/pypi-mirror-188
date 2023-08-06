import asyncio
from time import sleep

import allure
import pytest

from refinitiv.data import OpenState
from refinitiv.data.content import custom_instruments as ci
from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery._stream import stream_cxn_cache
from tests.integration.content.custom_instruments.conftest import (
    check_stream_instrument,
    check_open_and_close_stream_state,
    check_stream_snapshot,
    check_close_and_open_stream_state,
    is_stream_id_equal,
)
from tests.integration.content.helpers import (
    add_callbacks_for_universe_stream,
    check_triggered_events,
    check_stream_data,
)
from tests.integration.helpers import (
    assert_error,
)


@allure.suite("Content object - Custom Instrument")
@allure.feature("Custom Instrument Stream")
@allure.severity(allure.severity_level.CRITICAL)
class TestCustomInstrumentStream:
    @allure.title(
        "Create CustomInstrument stream multi-request with callbacks without updates and check events"
    )
    @pytest.mark.caseid("C40492347")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "expected_events,expected_fields",
        [
            (
                ["Refresh", "Refresh", "Complete"],
                ["TRDPRC_1", "TRADE_DATE", "SALTIM_NS"],
            )
        ],
    )
    def test_create_custom_instrument_multi_request_stream_with_callbacks(
        self,
        open_session_with_rdp_creds_for_ci,
        create_instrument,
        expected_events,
        expected_fields,
    ):
        symbol_01 = create_instrument()
        symbol_02 = create_instrument()
        triggered_events = []
        stream = ci.Definition(
            universe=[symbol_01, symbol_02],
            api="streaming.custom-instruments.endpoints.resource",
        ).get_stream()
        add_callbacks_for_universe_stream(stream, triggered_events)

        check_stream_data(stream, [symbol_01, symbol_02], expected_fields)
        check_triggered_events(triggered_events, expected_events)
        check_stream_instrument([symbol_01, symbol_02], stream)

    @allure.title(
        "Create several custom instruments streams with valid Symbol in names using the same session"
    )
    @pytest.mark.caseid("C40492351")
    @pytest.mark.parametrize(
        "expected_events",
        [
            (["Refresh", "Complete", "Update"]),
        ],
    )
    async def test_create_custom_instrument_streams_with_same_session(
        self, open_desktop_session_async, create_instrument, expected_events
    ):
        symbol_01 = create_instrument()
        symbol_02 = create_instrument()
        symbol_03 = create_instrument()

        triggered_events_01 = []
        stream_01 = ci.Definition(universe=symbol_01).get_stream()
        add_callbacks_for_universe_stream(stream_01, triggered_events_01)

        triggered_events_02 = []
        stream_02 = ci.Definition(universe=symbol_02).get_stream()
        add_callbacks_for_universe_stream(stream_02, triggered_events_02)

        triggered_events_03 = []
        stream_03 = ci.Definition(universe=symbol_03).get_stream()
        add_callbacks_for_universe_stream(stream_03, triggered_events_03)

        await asyncio.gather(
            stream_01.open_async(), stream_02.open_async(), stream_03.open_async()
        )
        sleep(2)
        check_close_and_open_stream_state(stream_01, stream_02, stream_03, wait_time=2)
        check_triggered_events(triggered_events_01, expected_events)
        check_triggered_events(triggered_events_02, expected_events)
        check_triggered_events(triggered_events_03, expected_events)
        check_stream_instrument(symbol_01, stream_01)
        check_stream_instrument(symbol_02, stream_02)
        check_stream_instrument(symbol_03, stream_03)

    @allure.title(
        "Create two custom instruments streams with valid Symbol in names using separate sessions"
    )
    @pytest.mark.caseid("C40492355")
    @pytest.mark.parametrize(
        "expected_events",
        [
            (["Refresh", "Complete", "Update"]),
        ],
    )
    async def test_create_custom_instruments_with_separate_sessions(
        self,
        expected_events,
        open_platform_session_with_rdp_creds_async,
        open_desktop_session_async,
        create_instrument,
    ):
        symbol_01 = create_instrument(
            session=open_platform_session_with_rdp_creds_async
        )
        symbol_02 = create_instrument(session=open_desktop_session_async)

        triggered_events_01 = []
        stream_01 = ci.Definition(universe=symbol_01).get_stream(
            session=open_platform_session_with_rdp_creds_async
        )
        add_callbacks_for_universe_stream(stream_01, triggered_events_01)

        triggered_events_02 = []
        stream_02 = ci.Definition(universe=symbol_02).get_stream(
            session=open_desktop_session_async
        )
        add_callbacks_for_universe_stream(stream_02, triggered_events_02)

        await asyncio.gather(stream_01.open_async(), stream_02.open_async())
        sleep(3)
        assert stream_01.open_state == OpenState.Opened
        assert stream_02.open_state == OpenState.Opened

        check_triggered_events(triggered_events_01, expected_events)
        check_triggered_events(triggered_events_02, expected_events)
        assert not is_stream_id_equal(stream_01, stream_02)
        stream_01.close()
        stream_02.close()

    @pytest.mark.caseid("C41030998")
    @allure.title("Create Custom Instrument stream without required parameters")
    def test_create_custom_instrument_stream_without_required_parameters(self):
        with pytest.raises(TypeError) as error:
            ci.Definition().get_stream()
        assert_error(error, "universe")

    @allure.title(
        "Create Custom Instrument stream with non-existed Symbol and get error event"
    )
    @pytest.mark.caseid("C41030999")
    @pytest.mark.parametrize(
        "name,expected_events,expected_msg",
        [
            (
                "W)INVALID",
                ["Error"],
                "Custom instrument symbol is invalid. Valid format example: S)INSTRUMENTSYMBOL.USER_UUID",
            )
        ],
    )
    def test_create_custom_instrument_stream_with_invalid_symbol(
        self, open_desktop_session, name, expected_events, expected_msg
    ):
        stream = ci.Definition(universe=name).get_stream()
        triggered_events = []
        add_callbacks_for_universe_stream(stream, triggered_events)
        check_open_and_close_stream_state(stream, wait_before_close=1)
        check_triggered_events(triggered_events, expected_events)
        # assert_stream_error(error_list, expected_msg, symbol)

    @pytest.mark.caseid("C40492362")
    @allure.title("Close Custom Instrument stream by closing session")
    def test_close_custom_instrument_stream_after_session_close(
        self, open_session_with_rdp_creds_for_ci, create_instrument
    ):
        symbol = create_instrument()
        session = open_session_with_rdp_creds_for_ci
        stream = ci.Definition(universe=symbol).get_stream()
        stream.open()
        session.close()
        assert stream.open_state == OpenState.Closed, "Stream is not in closed state"

        is_cnx_alive = stream_cxn_cache.is_cxn_alive(
            session, ContentType.STREAMING_CUSTOM_INSTRUMENTS
        )
        assert not is_cnx_alive, f"Connection is alive"
        session.open()

    @allure.title("Create Custom Instrument stream with get_snapshot")
    @pytest.mark.caseid("C41031000")
    @pytest.mark.parametrize(
        "expected_fields", [(["Instrument", "TRDPRC_1", "TRADE_DATE", "SALTIM_NS"])]
    )
    def test_create_custom_instrument_stream_and_get_snapshot(
        self, open_session, create_instrument, expected_fields
    ):
        symbol = create_instrument()
        stream = ci.Definition(universe=symbol).get_stream()
        stream.open(with_updates=False)
        check_stream_snapshot(
            stream=stream, universe=symbol, expected_fields=expected_fields
        )

    @allure.title(
        "Create CustomInstrument stream with universe and put to extended_params new universe and check if it exist"
    )
    @pytest.mark.caseid("C43998924")
    @pytest.mark.parametrize(
        "expected_fields",
        [(["TRDPRC_1", "TRADE_DATE", "SALTIM_NS"],)],
    )
    def test_create_custom_instrument_stream_with_universe_and_put_to_extended_params_new_universe(
        self,
        open_desktop_session,
        create_instrument,
        expected_fields,
    ):
        symbol = create_instrument()
        extended_symbol = create_instrument()

        stream = ci.Definition(
            universe=symbol, extended_params={"universe": extended_symbol}
        ).get_stream()

        check_stream_instrument(extended_symbol, stream)
        check_stream_data(stream, extended_symbol, expected_fields)

    @allure.title("Open and close CustomInstrument stream with context manager")
    @pytest.mark.caseid("C44023012")
    def test_open_custom_instrument_streaming_with_context_manager(
        self, create_instrument, open_session_with_rdp_creds_for_ci
    ):
        symbol = create_instrument(session=open_session_with_rdp_creds_for_ci)
        ci_stream = ci.Definition(universe=symbol).get_stream()
        with ci_stream:
            assert ci_stream._stream.is_opened, f"Stream is not Opened"
        assert not ci_stream._stream.is_opened, f"Stream is not Сlosed"

    @allure.title("Open and close CustomInstrument stream with async context manager")
    @pytest.mark.caseid("C44023011")
    async def test_open_custom_instrument_streaming_with_async_context_manager(
        self, create_instrument, open_desktop_session_async
    ):
        symbol = create_instrument(session=open_desktop_session_async)
        ci_stream = ci.Definition(universe=symbol).get_stream()
        async with ci_stream:
            assert ci_stream._stream.is_opened, f"Stream is not Opened"
        assert not ci_stream._stream.is_opened, f"Stream is not Сlosed"

    @pytest.mark.caseid("")
    @allure.title("Create Custom Instrument stream with invalid api parameter")
    def test_create_custom_instrument_stream_with_invalid_api(
        self, open_session_with_rdp_creds_for_ci, create_instrument
    ):
        with pytest.raises(ValueError) as error:
            stream = ci.Definition(
                universe=create_instrument(),
                api="streaming.custom-instruments.endpoints.invalid",
            ).get_stream()
            stream.open()
        assert (
            str(error.value)
            == "Not an existing path apis.streaming.custom-instruments.endpoints.invalid to url into config file"
        )
