import allure
import pytest

from refinitiv.data.content import pricing
from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery._stream import stream_cxn_cache
from tests.integration.content.chain.conftest import (
    open_desktop_session_for_streaming_chain,
    open_deployed_session_for_streaming_chain,
    create_chain_stream,
    create_chain_stream_with_callbacks,
)

CONSTITUENT_ERROR_MESSAGE = "The record could not be found"


@allure.suite("Content object - Streaming Chain")
@allure.feature("Content object - Streaming Chain")
@allure.severity(allure.severity_level.CRITICAL)
class TestStreamingChain:
    @allure.title("Open StreamingPrices using streaming chain and get results")
    @pytest.mark.caseid("33534326")
    @pytest.mark.parametrize("name,expected_fields", [("0#.FCHI", ["ASK", "BID"])])
    def test_open_streaming_prices_using_streaming_chain(
        self, open_desktop_session, name, expected_fields
    ):
        stream = create_chain_stream(name)
        stream.open()
        constituents_list = stream.constituents

        streaming_prices = pricing.Definition(
            universe=constituents_list, fields=expected_fields
        ).get_stream()
        streaming_prices.open()
        snapshot = streaming_prices.get_snapshot()
        field_names = snapshot.columns[1:].tolist()
        instrument_names = snapshot["Instrument"].values
        stream.close()
        streaming_prices.close()

        assert instrument_names == constituents_list, (
            f"Instrument names retrieved from StreamingPrice {instrument_names}"
            f" are not equal to constituents retrieved from StreamingChain {constituents_list}"
        )
        assert (
            field_names.sort() == expected_fields.sort()
        ), f"Field names {field_names} are not equal to requested."

    @allure.title("Open a Streaming Chain with a valid name and  get constituents list")
    @pytest.mark.caseid("33533976")
    @pytest.mark.parametrize("name", ["0#.DJI"])
    @pytest.mark.smoke
    def test_open_streaming_chain_with_valid_name(self, open_desktop_session, name):
        stream = create_chain_stream(name)
        stream.open(with_updates=True)
        constituents_list = stream.constituents
        assert len(constituents_list) > 0, f"The empty list received in response"
        assert (
            CONSTITUENT_ERROR_MESSAGE not in constituents_list
        ), f"Value {CONSTITUENT_ERROR_MESSAGE} found in list of constituents {constituents_list}"
        assert stream.is_chain, "is_chain is not true"
        stream.close()

    @allure.title("Open a Streaming Chain with INVALID name")
    @pytest.mark.caseid("33534354")
    @pytest.mark.parametrize("name", ["test_invalid_name"])
    def test_open_streaming_chain_with_invalid_name(self, open_desktop_session, name):
        triggered_events = []
        stream = create_chain_stream_with_callbacks(
            name=name, triggered_events=triggered_events
        )
        stream.open(with_updates=True)
        constituents_list = stream.constituents
        stream.close()
        assert (
            len(constituents_list) == 0
        ), f"Received non-empty constituents list: {constituents_list}"
        assert "Error received" in triggered_events, f"Error event  was not triggered"

    @allure.title("Open a Streaming Chain with a closed session")
    @pytest.mark.caseid("33533977")
    @pytest.mark.parametrize("name", ["0#.DJI"])
    def test_open_streaming_chain_when_session_is_not_opened(
        self, name, open_platform_session
    ):
        session = open_platform_session
        session.close()
        stream = create_chain_stream(name)
        with pytest.raises(AssertionError, match="Session must be open"):
            stream.open(with_updates=True)

    @allure.title(
        "Open a Streaming Chain with summary_links property and receive an array of Summary links"
    )
    @pytest.mark.caseid("33534056")
    @pytest.mark.parametrize("name", ["0#.DJI"])
    def test_open_streaming_chain_with_summary_links(self, open_desktop_session, name):
        stream = create_chain_stream(name)
        stream.open(with_updates=True)
        summary_links = stream.summary_links
        stream.close()
        assert ".DJI" in summary_links

    @allure.title("Open a StreamingChain with event handler functions")
    @pytest.mark.caseid("33536578")
    @pytest.mark.parametrize(
        "name,open_custom_session,service",
        [
            ("0#.DJI", open_deployed_session_for_streaming_chain, "ELEKTRON_DD"),
            ("0#.DJI", open_desktop_session_for_streaming_chain, None),
        ],
    )
    def test_open_streaming_chain_with_event_handlers(
        self, open_custom_session, name, service
    ):
        session = open_custom_session()
        triggered_events = []
        expected_events = [
            "Add performed",
            "Complete performed",
            "Remove performed",
            "Update performed",
        ]
        stream = create_chain_stream_with_callbacks(
            name, triggered_events, service=service
        )
        stream.open(with_updates=True)

        stream._stream._remove_constituent(1, "TEST remove")
        stream._stream._update_constituent(3, "OLD", "TEST update")
        constituents_list = stream.constituents
        stream.close()
        session.close()

        is_cxn_alive = stream_cxn_cache.is_cxn_alive(
            session, ContentType.STREAMING_PRICING
        )

        assert not is_cxn_alive, f"Connection is alive"
        assert not stream._stream.is_opened, f"Stream is not closed"

        assert len(constituents_list) > 0, f"The empty list received in response"
        for event in expected_events:
            assert (
                event in triggered_events
            ), f"found event '{event}' not handled by handlers or not triggered"
        assert (
            triggered_events.count(expected_events[1]) == 1
        ), f"Callback on_complete called more than once: {triggered_events.count(expected_events[1])}"

    @allure.title("Open and close a Streaming Chain with context manager")
    @pytest.mark.caseid("C44023026")
    @pytest.mark.parametrize("name", ["0#.DJI"])
    @pytest.mark.smoke
    def test_open_streaming_chain_with_context_manager(
        self, open_desktop_session, name
    ):
        with create_chain_stream(name) as chain:
            assert chain._stream.is_open
        assert chain._stream.is_close

    @allure.title("Open and close a Streaming Chain with asynchronous context manager")
    @pytest.mark.caseid("C44023027")
    @pytest.mark.parametrize("name", ["0#.DJI"])
    @pytest.mark.smoke
    async def test_open_streaming_chain_with_async_context_manager(
        self, open_desktop_session_async, name
    ):
        async with create_chain_stream(name) as chain:
            assert chain._stream.is_open
        assert chain._stream.is_close
