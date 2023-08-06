import time

import allure
import pytest

from refinitiv.data import OpenState
from refinitiv.data._content_type import ContentType
from refinitiv.data._errors import ScopeError
from refinitiv.data.content import pricing
from refinitiv.data.delivery._stream import stream_cxn_cache
from refinitiv.data.delivery.omm_stream import ContribType
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.helpers import (
    add_callbacks_for_universe_stream,
    check_triggered_events,
    check_stream_data,
)
from tests.integration.content.pricing.conftest import (
    check_pricing_data,
    check_item_message_and_status,
    add_callback_for_contribution,
)
from tests.integration.delivery.stream.omm_stream.conftest import on_ack, on_error
from tests.integration.helpers import (
    get_async_response_from_definitions,
    check_contrib_response,
    check_response_status,
)

HALF_SECOND = 0.5


@allure.suite("Content object - Pricing")
@allure.feature("Content object - Pricing")
@allure.severity(allure.severity_level.CRITICAL)
class TestPricing:
    @allure.title(
        "Open a Pricing stream on session and call universe without fields params"
    )
    @pytest.mark.parametrize(
        "universe,fields", [("EUR=", "IRGPRC"), ("GBP=", ["BID", "ASK"])]
    )
    @pytest.mark.caseid("35070172")
    def test_open_pricing_stream_by_universe_without_fields(
        self, universe, fields, open_session
    ):
        pricing_stream = pricing.Definition(
            universe=universe, api="streaming.pricing.endpoints.main"
        ).get_stream(session=open_session)

        check_stream_data(pricing_stream, universe, fields)

    @allure.title(
        "Creating Pricing definition object specifying the universe, fields and get data"
    )
    @pytest.mark.parametrize(
        "universe,fields", [("EUR=", "IRGPRC"), (["USD=", "GBP="], ["BID", "ASK"])]
    )
    @pytest.mark.caseid("35158864")
    def test_create_pricing_object_by_universe_with_fields(
        self, universe, fields, open_platform_session
    ):
        pricing_definition = pricing.Definition(
            universe=universe, fields=fields
        ).get_data(session=open_platform_session)

        check_pricing_data(pricing_definition, universe, fields)

    @allure.title("Open a Pricing stream on session and check item status")
    @pytest.mark.parametrize("universe", ["EUR="])
    @pytest.mark.caseid("35167789")
    def test_open_pricing_stream_by_universe_and_check_item_status(
        self, universe, open_session
    ):
        pricing_stream = pricing.Definition(universe=universe).get_stream(
            session=open_session
        )
        item_status = pricing_stream.open()

        assert (
            item_status == OpenState.Opened
        ), f"Item status is not Open, actual status is {item_status}"
        pricing_stream.close()

    @allure.title("Create a Pricing stream connection and check events")
    @pytest.mark.parametrize(
        "universe,expected_events",
        [(["EUR=", "GBP="], ["Refresh", "Refresh", "Complete", "Update"])],
    )
    @pytest.mark.caseid("35168704")
    @pytest.mark.smoke
    def test_open_pricing_stream_and_check_events(
        self, universe, expected_events, open_desktop_session
    ):
        triggered_events = []
        pricing_stream = pricing.Definition(universe=universe).get_stream()
        add_callbacks_for_universe_stream(pricing_stream, triggered_events)

        pricing_stream.open(with_updates=True)
        time.sleep(3)
        pricing_stream.close()

        check_triggered_events(triggered_events, expected_events)
        assert (
            triggered_events.count(expected_events[2]) == 1
        ), f"Callback on_complete called more than once: {triggered_events.count(expected_events[1])}"

    @allure.title("Create a Pricing stream with an invalid universe name")
    @pytest.mark.parametrize(
        "universe,expected_message",
        [
            ("INVALID", "The record could not be found"),
            (["EUR=", "INVAL"], "The record could not be found"),
        ],
    )
    @pytest.mark.caseid("35360349")
    def test_create_pricing_stream_with_invalid_data(
        self, universe, expected_message, open_desktop_session
    ):
        pricing_stream = pricing.Definition(universe=universe).get_stream(
            session=open_desktop_session
        )
        pricing_stream.open()

        check_item_message_and_status(universe, expected_message, pricing_stream)

    @allure.title(
        "Create a Pricing stream with user creds which does not have permission"
    )
    @pytest.mark.parametrize(
        "universe,fields,expected_message",
        [
            ("USD=", "BID", "A21: DACS User Profile denied access to vendor\n"),
            (
                ["EUR=", "USD="],
                ["BID", "ASK"],
                "A21: DACS User Profile denied access to vendor\n",
            ),
        ],
    )
    @pytest.mark.caseid("C43420983")
    def test_create_pricing_stream_with_user_creds_which_does_not_have_permission(
        self, universe, fields, expected_message, open_platform_session_with_rdp_creds
    ):
        pricing_stream = pricing.Definition(universe=universe).get_stream(
            session=open_platform_session_with_rdp_creds
        )
        pricing_stream.open()

        check_item_message_and_status(universe, expected_message, pricing_stream)

    @allure.title("Create a Pricing stream connection without updates and check events")
    @pytest.mark.parametrize("universe,fields", [("EUR=", "BID")])
    @pytest.mark.caseid("35364411")
    def test_open_pricing_stream_without_update(self, universe, open_session, fields):
        triggered_events_list = []
        pricing_stream = pricing.Definition(
            universe=universe, fields=fields
        ).get_stream()
        add_callbacks_for_universe_stream(pricing_stream, triggered_events_list)

        pricing_stream.open(with_updates=False)
        pricing_stream.close()

        assert "Complete" in triggered_events_list, f"{triggered_events_list}"
        assert (
            "Update" not in triggered_events_list
        ), f"Update is exist, {triggered_events_list}"

    @allure.title(
        "Creation of two pricing streams in one session and receiving data on them"
    )
    @pytest.mark.parametrize("universe_01,universe_02", [("EUR=", "USD=")])
    @pytest.mark.caseid("35371558")
    def test_open_two_pricing_stream_in_one_session(
        self, universe_01, universe_02, open_session
    ):
        pricing_stream_01 = pricing.Definition(universe=universe_01).get_stream()
        pricing_stream_02 = pricing.Definition(universe=universe_02).get_stream()

        check_stream_data(pricing_stream_01, universe_01)
        check_stream_data(pricing_stream_02, universe_02)

    @allure.title("Create a new stream when session is closed")
    @pytest.mark.parametrize("universe,fields", [("EUR=", "BID")])
    @pytest.mark.caseid("35385930")
    def test_open_pricing_stream_when_connection_was_dropped(
        self, universe, fields, open_session
    ):
        session = open_session
        session.close()
        pricing_stream = pricing.Definition(
            universe=universe, fields=fields
        ).get_stream()
        with pytest.raises(AssertionError) as error:
            pricing_stream.open(with_updates=True)
        assert str(error.value) == "Session must be open"

    @allure.title(
        "Creating Pricing definition object specifying the universe, fields and get_data_async"
    )
    @pytest.mark.parametrize(
        "universe,fields,invalid_universe",
        [("EUR=", "BID", []), (["USD=", "GBP="], ["BID", "ASK"], [])],
    )
    @pytest.mark.caseid("35395377")
    async def test_get_data_async(
        self, universe, fields, invalid_universe, open_platform_session_async
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            pricing.Definition(universe=universe, fields=fields),
            pricing.Definition(universe=invalid_universe, fields=fields),
        )

        check_pricing_data(valid_response, universe, fields)
        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.FOUR_HUNDRED,
            expected_http_reason=HttpReason.BAD_REQUEST,
            expected_error_code=HttpStatusCode.FOUR_HUNDRED,
            expected_error_message="Validation error: Missing required parameter 'universe'",
        )

    @allure.title("Create Pricing definition object with extended params")
    @pytest.mark.parametrize(
        "universe,fields,extended_universe,extended_fields",
        [("EUR=", "BID", "GBP", "IRGPRC")],
    )
    @pytest.mark.caseid("35395377")
    def test_get_data_by_extended_params(
        self,
        universe,
        fields,
        extended_universe,
        extended_fields,
        open_platform_session,
    ):
        response = pricing.Definition(
            universe=universe,
            fields=fields,
            extended_params={"universe": extended_universe, "fields": extended_fields},
        ).get_data(session=open_platform_session)

        check_pricing_data(response, extended_universe, extended_fields)

    @allure.title(
        "Create Pricing stream with universe and put to extended_params new fields and check fields is exist"
    )
    @pytest.mark.parametrize("universe,extended_fields", [("EUR=", ["IRGPRC"])])
    @pytest.mark.caseid("35401653")
    def test_create_stream_with_universe_and_put_to_extended_params_new_fields(
        self, universe, extended_fields, open_session
    ):
        stream = pricing.Definition(
            universe=universe, extended_params={"View": extended_fields}
        ).get_stream()
        check_stream_data(
            stream, expected_universe=universe, expected_fields=extended_fields
        )

    @allure.title("Closing streaming when calling session.close()")
    @pytest.mark.parametrize("universe,fields", [("EUR=", "BID")])
    @pytest.mark.caseid("35801379")
    def test_closing_streaming_when_calling_session_close(
        self, universe, fields, open_session
    ):
        session = open_session
        pricing_stream = pricing.Definition(
            universe=universe, fields=fields
        ).get_stream()
        pricing_stream.open(with_updates=True)
        session.close()

        is_cnx_alive = stream_cxn_cache.is_cxn_alive(
            session, ContentType.STREAMING_PRICING
        )

        assert not is_cnx_alive, f"Connection is alive"
        assert not pricing_stream._stream.is_opened, f"Stream is not closed"

    @allure.title("Create pricing definition object with invalid params and get error")
    @pytest.mark.caseid("40147423")
    @pytest.mark.parametrize(
        "universe,fields,expected_error",
        [
            (
                [],
                ["", "INVALID"],
                "Error code 400 | Validation error: Missing required parameter 'universe'",
            ),
        ],
    )
    def test_pricing_definition_object_with_invalid_params_and_get_error(
        self,
        universe,
        fields,
        expected_error,
        open_platform_session,
    ):
        with pytest.raises(RDError) as error:
            pricing.Definition(universe=universe, fields=fields).get_data()
        assert str(error.value) == expected_error

    @allure.title("Open and close streaming with context manager")
    @pytest.mark.parametrize("universe,fields", [("EUR=", "BID")])
    @pytest.mark.caseid("C44023013")
    def test_open_streaming_with_context_manager(self, universe, fields, open_session):
        pricing_stream = pricing.Definition(universe, fields=fields).get_stream()
        with pricing_stream:
            assert pricing_stream._stream.is_opened, f"Stream is not Opened"
        assert not pricing_stream._stream.is_opened, f"Stream is not Closed"

    @allure.title("Open and close streaming with async context manager")
    @pytest.mark.parametrize("universe,fields", [("EUR=", "BID")])
    @pytest.mark.caseid("C44023014")
    async def test_open_streaming_with_async_context_manager(
        self, universe, fields, open_session_async
    ):
        pricing_stream = pricing.Definition(universe, fields=fields).get_stream()
        async with pricing_stream:
            assert pricing_stream._stream.is_opened, f"Stream is not Opened"
        assert not pricing_stream._stream.is_opened, f"Stream is not Closed"

    @pytest.mark.caseid("")
    @allure.title("Create pricing stream with invalid api parameter")
    @pytest.mark.parametrize("universe,fields", [("GBP=", "BID")])
    def test_create_pricing_stream_with_invalid_api(
        self, open_session, universe, fields
    ):
        with pytest.raises(ValueError) as error:
            pricing_stream = pricing.Definition(
                universe, api="streaming.pricing.endpoints.invalid", fields=fields
            ).get_stream()
            pricing_stream.open()
        assert (
            str(error.value)
            == "Not an existing path apis.streaming.pricing.endpoints.invalid to url into config file"
        )

    @pytest.mark.caseid("C47579675")
    @allure.title("Add fields to existing stream")
    @pytest.mark.parametrize(
        "universe, fields, new_fields, expected_fields",
        [
            ("GBP=", "BID", ["ASK", "IRGPRC"], ["BID", "ASK", "IRGPRC"]),
            ("EUR=", "BID", "ASK", ["BID", "ASK"]),
        ],
    )
    def test_add_fields_to_existing_pricing_stream(
        self, open_session, universe, fields, new_fields, expected_fields
    ):

        pricing_stream = pricing.Definition(
            universe=universe, fields=fields
        ).get_stream()
        pricing_stream.open()
        time.sleep(HALF_SECOND)
        pricing_stream.add_fields(new_fields)
        time.sleep(HALF_SECOND)
        snapshot = pricing_stream.get_snapshot()
        check_pricing_data(snapshot, universe, expected_fields)

    @pytest.mark.caseid("C47579665")
    @allure.title("Remove fields in existing stream")
    @pytest.mark.parametrize(
        "universe, fields, removed_fields, expected_fields",
        [
            (["GBP=", "EUR="], ["ASK", "IRGPRC"], "ASK", ["IRGPRC"]),
            ("EUR=", "BID", "BID", None),
            ("EUR=", "BID", "ASK", ["BID"]),
        ],
    )
    def test_remove_fields_in_existing_pricing_stream(
        self, open_session, universe, fields, removed_fields, expected_fields
    ):
        pricing_stream = pricing.Definition(
            universe=universe, fields=fields
        ).get_stream()
        pricing_stream.open()
        time.sleep(HALF_SECOND)
        pricing_stream.remove_fields(removed_fields)
        time.sleep(HALF_SECOND)
        snapshot = pricing_stream.get_snapshot()
        check_pricing_data(snapshot, universe, expected_fields)

    @pytest.mark.caseid("C47579526")
    @allure.title("Add and remove fields to existing stream")
    @pytest.mark.parametrize(
        "universe, fields, new_fields, removed_fields, expected_fields, expected_events",
        [
            (
                ["GBP=", "EUR="],
                ["ASK", "IRGPRC"],
                "PCTCHG_MTD",
                "ASK",
                ["PCTCHG_MTD", "IRGPRC"],
                ["Refresh", "Refresh", "Complete", "Update"],
            ),
            (
                "EUR=",
                "BID",
                "BID",
                "ASK",
                None,
                ["Refresh", "Complete", "Update"],
            ),
        ],
    )
    def test_add_and_remove_fields_to_existing_pricing_stream(
        self,
        open_session,
        universe,
        fields,
        new_fields,
        removed_fields,
        expected_fields,
        expected_events,
    ):
        triggered_events = []
        pricing_stream = pricing.Definition(
            universe=universe, fields=fields
        ).get_stream()
        add_callbacks_for_universe_stream(pricing_stream, triggered_events)
        pricing_stream.open()
        time.sleep(HALF_SECOND)
        pricing_stream.add_fields(new_fields)
        time.sleep(HALF_SECOND)
        pricing_stream.remove_fields(removed_fields)
        time.sleep(HALF_SECOND)
        snapshot = pricing_stream.get_snapshot()
        check_pricing_data(snapshot, universe, expected_fields)
        check_triggered_events(triggered_events, expected_events)
        assert (
            triggered_events.count("Complete") == 1
        ), f"Callback on_complete called more than once: {triggered_events.count(expected_events[1])}"

    @pytest.mark.caseid("C48673914")
    @allure.title("Add and remove instruments to existing stream")
    @pytest.mark.parametrize(
        "universe, fields, new_instrument, removed_instrument, expected_instrument",
        [
            (
                ["GBP=", "EUR="],
                ["ASK", "IRGPRC"],
                "USD=",
                "GBP=",
                ["EUR=", "USD="],
            ),
            (
                "EUR=",
                "BID",
                "USD=",
                "EUR=",
                "USD=",
            ),
        ],
    )
    def test_add_and_remove_instrument_to_existing_pricing_stream(
        self,
        open_desktop_session,
        universe,
        fields,
        new_instrument,
        removed_instrument,
        expected_instrument,
    ):
        triggered_events = []
        pricing_stream = pricing.Definition(
            universe=universe, fields=fields
        ).get_stream()
        add_callbacks_for_universe_stream(pricing_stream, triggered_events)
        pricing_stream.open()
        time.sleep(HALF_SECOND)
        pricing_stream.add_instruments(new_instrument)
        time.sleep(HALF_SECOND)
        pricing_stream.remove_instruments(removed_instrument)
        time.sleep(HALF_SECOND)
        snapshot = pricing_stream.get_snapshot()
        check_pricing_data(snapshot, expected_instrument)
        assert (
            triggered_events.count("Complete") == 1
        ), f"Callback on_complete called more than once: {triggered_events.count('Complete')}"

    @allure.title("Offstream contribute in pricing stream and check response")
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
    @pytest.mark.caseid("C49042542")
    def test_offstream_contribution_pricing_stream_and_check_response(
        self, request, load_config, open_platform_session, name, fields, message
    ):
        event_list = []
        response = pricing.contribute(
            name=name,
            fields=fields,
            on_ack=lambda ack_msg, stream: on_ack(ack_msg, stream, event_list),
            on_error=lambda error_msg, stream: on_error(error_msg, stream, event_list),
            service="ATS_GLOBAL_1",
        )

        check_contrib_response(request, response, event_list, message)

    @allure.title("Offstream contribute async in pricing stream and check response")
    @pytest.mark.parametrize(
        "name,fields,message",
        [
            pytest.param(
                "TEST",
                {"BID": 777.83},
                "[1]: Contribution Accepted",
                id="positive_case",
            ),
            pytest.param(
                "TEST",
                {"INVAL": 777.83},
                "JSON Unexpected FID. Received 'INVAL' for key 'Fields'",
                id="negative_case",
            ),
        ],
    )
    @pytest.mark.caseid("C49042540")
    async def test_offstream_async_contribution_pricing_stream_and_check_response(
        self, request, load_config, open_platform_session_async, name, fields, message
    ):
        event_list = []
        response = await pricing.contribute_async(
            name=name,
            fields=fields,
            on_ack=lambda ack_msg, stream: on_ack(ack_msg, stream, event_list),
            on_error=lambda error_msg, stream: on_error(error_msg, stream, event_list),
            service="ATS_GLOBAL_1",
        )

        check_contrib_response(request, response, event_list, message)

    @allure.title("OnStream contribute in pricing stream and check snapshot")
    @pytest.mark.parametrize(
        "universe, fields, contrib_value, message",
        [
            pytest.param(
                "TEST",
                ["BID", "ASK", "OPEN_PRC"],
                {"BID": 503},
                "[1]: Contribution Accepted",
                id="positive_case",
            ),
            pytest.param(
                "TEST",
                "ASK",
                {"INVAL": 277.83},
                "JSON Unexpected FID. Received 'INVAL' for key 'Fields'",
                id="negative_case",
            ),
        ],
    )
    @pytest.mark.caseid("C49042532")
    def test_on_stream_contribution_pricing_stream(
        self,
        request,
        setup_direct_url,
        open_platform_session,
        universe,
        fields,
        contrib_value,
        message,
    ):
        event_list = []
        definition = pricing.Definition(
            universe=universe, fields=fields, service="ATS_GLOBAL_1"
        )
        stream = definition.get_stream()
        add_callback_for_contribution(stream, event_list)
        stream.open()
        time.sleep(HALF_SECOND)

        response = stream.contribute(
            universe, contrib_value, contrib_type=ContribType.REFRESH
        )
        if "positive_case" in request.node.callspec.id:
            snapshot = stream.get_snapshot()["BID"][0]
            assert (
                snapshot == contrib_value["BID"]
            ), f"Actual value {snapshot} != {contrib_value['BID']}"

        check_contrib_response(request, response, event_list, message)

    @allure.title("OnStream contribute async in pricing stream and check snapshot")
    @pytest.mark.parametrize(
        "universe, fields, contrib_value, message",
        [
            pytest.param(
                "TEST",
                ["BID", "ASK", "OPEN_PRC"],
                {"BID": 503},
                "[1]: Contribution Accepted",
                id="positive_case",
            ),
            pytest.param(
                "TEST",
                "ASK",
                {"INVAL": 277.83},
                "JSON Unexpected FID. Received 'INVAL' for key 'Fields'",
                id="negative_case",
            ),
        ],
    )
    @pytest.mark.caseid("C49042538")
    async def test_on_stream_async_contribution_pricing_stream(
        self,
        request,
        setup_direct_url,
        open_platform_session_async,
        universe,
        fields,
        contrib_value,
        message,
    ):
        event_list = []
        definition = pricing.Definition(
            universe=universe, fields=fields, service="ATS_GLOBAL_1"
        )
        stream = definition.get_stream()
        add_callback_for_contribution(stream, event_list)
        await stream.open_async()

        response = await stream.contribute_async(
            universe, contrib_value, contrib_type=ContribType.UPDATE
        )
        if "positive_case" in request.node.callspec.id:
            snapshot = stream.get_snapshot()["BID"][0]
            assert (
                snapshot == contrib_value["BID"]
            ), f"Actual value {snapshot} != {contrib_value['BID']}"

        check_contrib_response(request, response, event_list, message)

    @allure.title("Get pricing stream/data with scope validation")
    @pytest.mark.caseid("C53817129")
    @pytest.mark.parametrize(
        "universe,fields,scope",
        [
            (["GBP=", "EUR="], ["BID", "ASK", "HIGH_1"], "trapi.invalid_scope"),
        ],
    )
    def test_pricing_stream_data_with_scope_validation(
        self, create_session_with_scope, universe, fields, scope
    ):
        create_session_with_scope(scope=scope, acc="machine")
        with pytest.raises(ScopeError) as error:
            pricing.Definition(universe=universe, fields=fields).get_data()
        assert "Missing scopes" in str(error.value)

        with pytest.raises(ScopeError) as error:
            stream = pricing.Definition(
                universe=universe, fields=fields, api="streaming.pricing.endpoints.main"
            ).get_stream()
            stream.open()
        assert "Missing scopes" in str(error.value)
        time.sleep(1)

        assert (
            stream.open_state == OpenState.Closed
        ), "Pricing Stream is not closed after ScopeError Exception raised"
