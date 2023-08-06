import allure
import pytest

import refinitiv.data.session.desktop as desktop
import tests.integration.conftest as conf
from refinitiv.data import OpenState
from refinitiv.data.session import EventCode
from refinitiv.data._core.session import set_default
from tests.integration.core.session.conftest import (
    assert_session_open_state,
    on_state,
    on_event,
)
from refinitiv.data.delivery import omm_stream
from tests.integration.helpers import (
    compare_list,
    check_event_code,
    check_event_message
)

def check_port_dummy(*args, **kwargs):
    pass


@allure.suite("Session layer - Desktop session")
@allure.feature("Session layer - Desktop session")
@allure.severity(allure.severity_level.CRITICAL)
class TestDesktopSession:
    @allure.title(
        "Verify that desktop session is not opened and error notification received using incorrect application key"
    )
    @pytest.mark.caseid("C39516003")
    def test_session_is_not_opened_using_invalid_credentials(self):
        event_list = []
        session = desktop.Definition(
            app_key="INVALID_APP_KEY",
        ).get_session()
        session.on_event(
            lambda event_code, event_msg, _: on_event(
                event_code, event_msg, session, event_list
            )
        )
        session.open()

        assert event_list[0][0] == EventCode.SessionAuthenticationFailed
        assert event_list[0][1] == "Status code 400: App key is incorrect"
        assert session.open_state == OpenState.Closed

    @allure.title(
        "Verify that desktop session is not opened and error notification received if Eikon is not running"
    )
    @pytest.mark.caseid("C39516004")
    def test_session_is_not_opened_when_eikon_is_not_run(self):
        event_list = []
        session = desktop.Definition(
            app_key=conf.desktop_app_key,
        ).get_session()
        set_default(session)
        session.on_event(
            lambda event_code, event_msg, _: on_event(
                event_code, event_msg, session, event_list
            )
        )
        session._connection.check_proxy = check_port_dummy
        session.open()

        assert event_list[0][0] == EventCode.SessionAuthenticationFailed
        assert event_list[0][1] == "Eikon is not running"
        assert session.open_state == OpenState.Closed
        session.close()

    @allure.title(
        "Open desktop session with callbacks and verify that desktop session is opened"
    )
    @pytest.mark.parametrize(
        "expected_events",
        [[(OpenState.Pending, "Session opening in progress"),
          (OpenState.Opened, "Session is opened"),
          (OpenState.Closed, "Session is closed")]],
    )
    @pytest.mark.caseid("C39515688")
    def test_desktop_session_with_callbacks(self, expected_events):
        event_list = []
        session = desktop.Definition(
            app_key=conf.desktop_app_key,
        ).get_session()
        set_default(session)
        session.on_event(
            lambda event, message, session: on_event(
                event, message, session, event_list
            )
        )
        session.on_state(
            lambda open_state, message, session: on_state(
                open_state, message, session, event_list
            )
        )
        session.open()
        assert_session_open_state(session)

        session.close()
        compare_list(event_list, expected_events)

    @allure.title("Verify using desktop session with ContextManager")
    @pytest.mark.caseid("C44023031")
    @pytest.mark.smoke
    def test_desktop_session_is_opened_and_is_closed_using_context_manager(self):
        session = desktop.Definition(
            app_key=conf.desktop_app_key,
        ).get_session()
        with session:
            assert session.open_state == OpenState.Opened
        assert session.open_state == OpenState.Closed

    @allure.title("Verify using desktop session with asynchronous ContextManager")
    @pytest.mark.caseid("C44023032")
    @pytest.mark.smoke
    async def test_desktop_session_is_opened_and_is_closed_using_async_context_manager(
        self,
    ):
        session = desktop.Definition(
            app_key=conf.desktop_app_key,
        ).get_session()
        async with session:
            assert session.open_state == OpenState.Opened
        assert session.open_state == OpenState.Closed

    @allure.title(
        "Open desktop session with callbacks and verify that all cnx events are received"
    )
    @pytest.mark.parametrize(
        "expected_events",
        [[(OpenState.Pending, "Session opening in progress"),
          (OpenState.Opened, "Session is opened"),
          (EventCode.StreamConnecting, {'url': 'ws://localhost:9060/api/rdp/streaming/pricing/v1/WebSocket', 'api_cfg': 'apis.streaming.pricing.endpoints.main'}),
          (EventCode.StreamConnected, {'url': 'ws://localhost:9060/api/rdp/streaming/pricing/v1/WebSocket', 'api_cfg': 'apis.streaming.pricing.endpoints.main'}),
          (OpenState.Closed, "Session is closed")]],
    )
    @pytest.mark.caseid("C39515688")
    def test_desktop_session_with_callbacks(self, expected_events):
        event_list = []
        session = desktop.Definition(
            app_key=conf.desktop_app_key,
        ).get_session()
        set_default(session)
        session.on_event(
            lambda event, message, session: on_event(
                event, message, session, event_list
            )
        )
        session.on_state(
            lambda open_state, message, session: on_state(
                open_state, message, session, event_list
            )
        )
        session.open()
        stream = omm_stream.Definition(name="GBP=", fields=["BID", "ASK"]).get_stream(session=session)
        stream.open()
        assert stream.open_state == OpenState.Opened, "Stream is not in opened state"
        stream.close()
        assert stream.open_state == OpenState.Closed, "Stream is not in closed state"

        assert_session_open_state(session)
        session.close()
        check_event_code(event_list, expected_events)
        check_event_message(event_list, expected_events)
