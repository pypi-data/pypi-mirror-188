import allure
import pytest

from refinitiv.data import OpenState
from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery import rdp_stream
from refinitiv.data.delivery._stream import stream_cxn_cache
from tests.integration.delivery.stream.conftest import (
    check_open_and_close_stream_state,
)
from tests.integration.delivery.stream.rdp_stream.conftest import (
    get_financial_contracts_stream,
    get_benchmark_stream,
    get_trading_analytics_stream,
    check_stream_view,
    check_stream_universe,
    add_callbacks,
)


@allure.suite("Delivery object - Stream")
@allure.feature("Delivery object - RDP Stream")
@allure.severity(allure.severity_level.CRITICAL)
class TestRdpStream:
    @allure.title("Open RDP stream, check stream parameters")
    @pytest.mark.parametrize(
        "rdp_stream_definition,expected_universe,expected_view",
        [
            [
                get_financial_contracts_stream,
                {
                    "instrumentType": "FxCross",
                    "instrumentDefinition": {
                        "instrumentTag": "USDAUD",
                        "fxCrossType": "FxSpot",
                        "fxCrossCode": "USDAUD",
                    },
                },
                [
                    "InstrumentTag",
                    "FxSpot_BidMidAsk",
                    "ErrorCode",
                    "Ccy1SpotDate",
                    "Ccy2SpotDate",
                ],
            ],
            [get_benchmark_stream, ["TSLA.O", "AAPL.O", "AMZN.O"], None],
            [get_trading_analytics_stream, [], None],
        ],
    )
    @pytest.mark.caseid("C39068745")
    def test_open_rdp_stream(
        self, open_session, rdp_stream_definition, expected_universe, expected_view
    ):
        stream = rdp_stream_definition()
        check_open_and_close_stream_state(stream)
        check_stream_universe(stream, expected_universe)
        check_stream_view(stream, expected_view)

    @allure.title("Open RDP stream with callbacks")
    @pytest.mark.parametrize(
        "expected_universe,expected_view",
        [
            [
                [
                    {
                        "instrumentType": "FxCross",
                        "instrumentDefinition": {
                            "instrumentTag": "USDAUD",
                            "fxCrossType": "FxSpot",
                            "fxCrossCode": "USDAUD",
                        },
                    }
                ],
                [
                    "InstrumentTag",
                    "FxSpot_BidMidAsk",
                    "ErrorCode",
                    "Ccy1SpotDate",
                    "Ccy2SpotDate",
                ],
            ]
        ],
    )
    @pytest.mark.caseid("C39068832")
    def test_open_rdp_stream_with_callbacks(
        self, open_session, expected_universe, expected_view
    ):
        stream = get_financial_contracts_stream()
        stream_log = []
        add_callbacks(stream, stream_log)

        check_open_and_close_stream_state(stream, wait_before_close=3)

        expected_event_types = ["response", "update"]
        for event in expected_event_types:
            assert event in stream_log, f"No event {event} received"

    @allure.title("Open RDP stream without required parameters")
    @pytest.mark.caseid("C39068923")
    def test_open_rdp_stream_without_required_parameters(self, open_session):
        with pytest.raises(TypeError, match="missing .* required positional argument"):
            rdp_stream.Definition(
                universe=[],
                view=None,
                service=None,
                api="streaming.trading-analytics.endpoints.redi",
            )

    @allure.title("Open RDP stream with extended params")
    @pytest.mark.caseid("C39068927")
    def test_open_rdp_stream_with_extended_params(self, open_session):
        stream = get_financial_contracts_stream(
            extended_params={"EXTENDED_PARAM": "EXTENDED_PARAM_VALUE"}
        )
        check_open_and_close_stream_state(stream)
        assert stream._extended_params["EXTENDED_PARAM"] == "EXTENDED_PARAM_VALUE"

    @allure.title("Open async RDP stream")
    @pytest.mark.caseid("C39068929")
    async def test_open_rdp_stream_async(self, open_session_async):
        stream = get_financial_contracts_stream()
        await stream.open_async()
        assert stream.open_state == OpenState.Opened, "Stream is not in opened state"
        stream.close()
        assert stream.open_state == OpenState.Closed, "Stream is not in closed state"

    @allure.title("Close RDP stream by closing session")
    @pytest.mark.caseid("C39068931")
    def test_stream_closes_after_session_close(self, open_desktop_session):
        session = open_desktop_session
        stream = get_financial_contracts_stream()
        stream.open()
        session.close()

        assert stream.open_state == OpenState.Closed, "Stream is not in closed state"
        is_cxn_alive = stream_cxn_cache.is_cxn_alive(
            session, ContentType.STREAMING_CONTRACTS
        )
        assert not is_cxn_alive, f"Connection is alive"

    @allure.title("Verify RDP stream is opened and closed with ContextManager")
    @pytest.mark.parametrize(
        "rdp_stream_definition",
        [get_financial_contracts_stream],
    )
    @pytest.mark.caseid("C44023017")
    def test_open_rdp_stream_with_context_manager(
        self, open_session, rdp_stream_definition
    ):
        stream = rdp_stream_definition()
        with stream:
            assert (
                stream.open_state == OpenState.Opened
            ), "RDP Stream is not opened in ContextManager"
        assert (
            stream.open_state == OpenState.Closed
        ), "RDP Stream is not closed outside ContextManager"

    @allure.title(
        "Verify RDP stream is opened and closed with asynchronous ContextManager"
    )
    @pytest.mark.parametrize(
        "rdp_stream_definition",
        [
            get_financial_contracts_stream,
        ],
    )
    @pytest.mark.caseid("C44023018")
    async def test_open_rdp_stream_with_async_context_manager(
        self, open_session_async, rdp_stream_definition
    ):
        stream = rdp_stream_definition()
        async with stream:
            assert (
                stream.open_state == OpenState.Opened
            ), "RDP Stream is not opened in ContextManager"
        assert (
            stream.open_state == OpenState.Closed
        ), "RDP Stream is not closed outside ContextManager"
