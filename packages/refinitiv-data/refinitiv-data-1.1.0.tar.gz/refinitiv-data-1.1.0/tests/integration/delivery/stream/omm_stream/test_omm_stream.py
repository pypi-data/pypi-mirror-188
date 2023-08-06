import asyncio
from time import sleep

import allure
import pytest

from refinitiv.data import OpenState
from refinitiv.data._content_type import ContentType
from refinitiv.data.delivery import omm_stream
from refinitiv.data.delivery._stream import stream_cxn_cache
from tests.integration.delivery.stream.conftest import (
    check_open_and_close_stream_state,
)
from tests.integration.delivery.stream.omm_stream.conftest import (
    open_deployed_session_for_omm_stream,
    open_platform_session_for_omm_stream,
    check_triggered_events,
    check_stream_view,
    check_stream_universe,
    check_extended_params,
    get_error_event_text_msg,
    on_ack,
    on_error,
)
from tests.integration.helpers import add_callbacks, assert_error
from tests.integration.helpers import check_contrib_response


@allure.suite("Delivery object - Stream")
@allure.feature("Delivery object - OMM stream")
@allure.severity(allure.severity_level.CRITICAL)
class TestOMMStream:
    @allure.title(
        "Create OMM stream object with all callbacks, check stream parameters"
    )
    @pytest.mark.parametrize(
        "open_custom_session,name,fields,api,domain,service,expected_events",
        [
            (
                open_platform_session_for_omm_stream,
                "GBP=",
                ["BID", "ASK"],
                "streaming.pricing.endpoints.main",
                "MarketPrice",
                None,
                ["Refresh", "Complete", "Update"],
            ),
            (
                open_platform_session_for_omm_stream,
                "GBP=",
                [],
                "streaming.pricing.endpoints.direct-websocket",
                "MarketPrice",
                "ELEKTRON_DD",
                ["Refresh", "Complete", "Update"],
            ),
            (
                open_deployed_session_for_omm_stream,
                "BB.TO",
                None,
                None,
                "MarketByPrice",
                "ELEKTRON_DD",
                ["Refresh"],
            ),
        ],
    )
    @pytest.mark.caseid("37805456")
    def test_create_omm_stream_with_all_callbacks(
        self,
        open_custom_session,
        name,
        fields,
        api,
        domain,
        service,
        expected_events,
    ):
        session = open_custom_session()
        triggered_events = []
        stream = omm_stream.Definition(
            name=name, api=api, service=service, fields=fields, domain=domain
        ).get_stream(session)
        add_callbacks(stream, triggered_events)
        check_open_and_close_stream_state(stream, wait_before_close=6)
        session.close()
        check_triggered_events(triggered_events, expected_events)
        check_stream_universe(name, triggered_events)
        check_stream_view(fields, triggered_events)

    @allure.title("Listening two streams and keep retrieving data for active stream")
    @pytest.mark.parametrize(
        "name,fields01,fields02,expected_events",
        [("GBP=", "BID", "ASK", ["Refresh", "Complete"])],
    )
    @pytest.mark.caseid("39516504")
    async def test_keep_retrieving_data_for_two_streams(
        self, name, fields01, fields02, open_session_async, expected_events
    ):
        triggered_events_01 = []
        stream_01 = omm_stream.Definition(name=name, fields=fields01).get_stream()
        add_callbacks(stream_01, triggered_events_01)
        triggered_events_02 = []
        stream_02 = omm_stream.Definition(name=name, fields=fields02).get_stream()
        add_callbacks(stream_02, triggered_events_02)

        await asyncio.gather(stream_01.open_async(), stream_02.open_async())
        sleep(5)
        check_triggered_events(triggered_events_01, expected_events)
        check_triggered_events(triggered_events_02, expected_events)

    @allure.title(
        "Stop listening closed OMM stream and keep retrieving data for active stream"
    )
    @pytest.mark.parametrize(
        "name01,name02,expected_events",
        [("EUR=", "GBP=", ["Refresh", "Complete", "Update"])],
    )
    @pytest.mark.caseid("37805459")
    async def test_keep_retrieving_data_for_active_stream(
        self, name01, name02, expected_events, open_session_async
    ):
        stream_01 = omm_stream.Definition(name=name01).get_stream()
        stream_01.open()

        triggered_events_02 = []
        stream_02 = omm_stream.Definition(name=name02).get_stream()
        add_callbacks(stream_02, triggered_events_02)
        stream_02.open()
        sleep(6)
        stream_01.close()
        assert stream_01.open_state == OpenState.Closed, "Stream is not in closed state"

        check_triggered_events(triggered_events_02, expected_events)
        stream_02.close()

    @allure.title("Open OMM stream without required parameters")
    @pytest.mark.caseid("39516358")
    def test_open_omm_stream_without_required_parameters(self):
        with pytest.raises(TypeError) as error:
            omm_stream.Definition().get_stream()
        assert_error(error, "name")

    @allure.title("Get an error for OMM stream with invalid name")
    @pytest.mark.parametrize(
        "name,error_msg", [("INVALID", "The record could not be found")]
    )
    @pytest.mark.caseid("37805461")
    def test_open_omm_stream_with_invalid_params(self, open_session, name, error_msg):
        stream = omm_stream.Definition(name=name).get_stream()
        triggered_events = []
        add_callbacks(stream, triggered_events)
        check_open_and_close_stream_state(stream, wait_before_close=3)
        assert error_msg in get_error_event_text_msg(triggered_events)

    @allure.title("Open OMM stream with extended params")
    @pytest.mark.parametrize(
        "name,fields,extended_params", [("GBP=", ["ASK"], {"View": ["BID"]})]
    )
    @pytest.mark.caseid("37805458")  # review case with w/o defining fields
    def test_open_omm_stream_with_extended_params(
        self, open_session, name, fields, extended_params
    ):
        stream = omm_stream.Definition(
            name=name, fields=fields, extended_params=extended_params
        ).get_stream()
        triggered_events_list = []
        add_callbacks(stream, triggered_events_list)
        check_open_and_close_stream_state(stream, wait_before_close=6)
        check_extended_params(stream, extended_params, triggered_events_list)

    @allure.title("Open async OMM stream")
    @pytest.mark.parametrize("name,fields", [("GBP=", ["BID", "ASK"])])
    @pytest.mark.caseid("39516353")
    async def test_open_omm_stream_async(self, open_session_async, name, fields):
        stream = omm_stream.Definition(name=name, fields=fields).get_stream()
        await stream.open_async()
        assert stream.open_state == OpenState.Opened, "Stream is not in opened state"
        stream.close()
        assert stream.open_state == OpenState.Closed, "Stream is not in closed state"

    @allure.title("Close OMM stream by closing session")
    @pytest.mark.parametrize("name,fields", [("GBP=", ["BID", "ASK"])])
    @pytest.mark.caseid("39516313")
    def test_stream_closes_after_session_close(
        self, open_desktop_session, name, fields
    ):
        session = open_desktop_session
        stream = omm_stream.Definition(name, fields=fields).get_stream()
        stream.open()
        session.close()

        assert stream.open_state == OpenState.Closed, "Stream is not in closed state"
        is_cxn_alive = stream_cxn_cache.is_cxn_alive(
            session, ContentType.STREAMING_PRICING
        )
        assert not is_cxn_alive, f"Connection is alive"

    @allure.title("Verify OMM stream is opened and closed with ContextManager")
    @pytest.mark.parametrize("name,fields", [("GBP=", ["BID", "ASK"])])
    @pytest.mark.caseid("C44023016")
    def test_open_omm_stream_with_context_manager(self, open_session, name, fields):
        stream = omm_stream.Definition(name=name, fields=fields).get_stream()
        with stream:
            assert (
                stream.open_state == OpenState.Opened
            ), "OMM Stream is not opened in ContextManager"
        assert (
            stream.open_state == OpenState.Closed
        ), "OMM Stream is not closed outside ContextManager"

    @allure.title(
        "Verify OMM stream is opened and closed with asynchronous ContextManager"
    )
    @pytest.mark.parametrize("name,fields", [("GBP=", ["BID", "ASK"])])
    @pytest.mark.caseid("C44023015")
    async def test_open_omm_stream_with_async_context_manager(
        self, open_session_async, name, fields
    ):
        stream = omm_stream.Definition(name=name, fields=fields).get_stream()
        async with stream:
            assert (
                stream.open_state == OpenState.Opened
            ), "OMM Stream is not opened in ContextManager"
        assert (
            stream.open_state == OpenState.Closed
        ), "OMM Stream is not closed outside ContextManager"

    @allure.title("Offstream contribute in OMM stream and check response")
    @pytest.mark.parametrize(
        "name,fields,message",
        [
            pytest.param(
                "TEST",
                {"BID": 240.83},
                "[1]: Contribution Accepted",
                id="positive_case",
            ),
            pytest.param(
                "TEST",
                {"INVAL": 240.83},
                "JSON Unexpected FID. Received 'INVAL' for key 'Fields'",
                id="negative_case",
            ),
        ],
    )
    @pytest.mark.caseid("C48464965")
    def test_offstream_contribution_omm_stream_and_check_response(
        self, request, load_config, open_platform_session, name, fields, message
    ):
        event_list = []
        response = omm_stream.contribute(
            name=name,
            fields=fields,
            on_ack=lambda ack_msg, stream: on_ack(ack_msg, stream, event_list),
            on_error=lambda error_msg, stream: on_error(error_msg, stream, event_list),
            service="ATS_GLOBAL_1",
        )

        check_contrib_response(request, response, event_list, message)

    @allure.title("Offstream async contribute in OMM stream and check response")
    @pytest.mark.parametrize(
        "name,fields,message",
        [
            pytest.param(
                "TEST",
                {"BID": 240.83},
                "[1]: Contribution Accepted",
                id="positive_case",
            ),
            pytest.param(
                "TEST",
                {"INVAL": 240.83},
                "JSON Unexpected FID. Received 'INVAL' for key 'Fields'",
                id="negative_case",
            ),
        ],
    )
    @pytest.mark.caseid("C48464966")
    async def test_offstream_async_contribution_omm_stream_and_check_response(
        self, request, load_config, open_platform_session_async, name, fields, message
    ):
        event_list = []
        response = await omm_stream.contribute_async(
            name=name,
            fields=fields,
            on_ack=lambda ack_msg, stream: on_ack(ack_msg, stream, event_list),
            on_error=lambda error_msg, stream: on_error(error_msg, stream, event_list),
            service="ATS_GLOBAL_1",
        )

        check_contrib_response(request, response, event_list, message)
