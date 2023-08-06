import allure
import pytest

import refinitiv.data.session.platform as platform
import tests.integration.conftest as conf
from refinitiv.data import OpenState
from refinitiv.data.errors import PlatformSessionError
from refinitiv.data.session import set_default, EventCode
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


@allure.suite("Session layer - Platform session")
@allure.feature("Session layer - Platform session")
@allure.severity(allure.severity_level.CRITICAL)
class TestPlatformSession:
    @allure.title(
        "Verify that session is not opened and error notification received using invalid credentials"
    )
    @pytest.mark.caseid("C37689844")
    def test_session_is_not_opened_using_invalid_credentials(self):
        session = None
        try:
            session = platform.Definition(
                app_key="INVALID",
                grant=platform.GrantPassword(username="USERNAME", password="PASSWORD"),
            ).get_session()

            session.open()
        except PlatformSessionError:
            pass

        assert session.open_state == OpenState.Closed

    @allure.title(
        "Verify that Platform session with valid credentials opens and check callbacks"
    )
    @pytest.mark.parametrize(
        "expected_events",
        [[
            (OpenState.Pending, "Session opening in progress"),
            (EventCode.SessionAuthenticationSuccess, "All is well"),
            (OpenState.Opened, "Session is opened"),
            (OpenState.Closed, "Session is closed"),
        ]],
    )
    @pytest.mark.caseid("C37689397")
    def test_platform_session_with_callbacks(self, expected_events):
        event_list = []
        session = platform.Definition(
            app_key=conf.desktop_app_key,
            grant=platform.GrantPassword(
                username=conf.edp.username, password=conf.edp.password
            ),
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
        compare_list(event_list, expected_events)

    @allure.title("Verify using platform session with ContextManager")
    @pytest.mark.caseid("C44023028")
    @pytest.mark.smoke
    def test_platform_session_is_opened_and_is_closed_using_context_manager(self):
        session = platform.Definition(
            app_key=conf.desktop_app_key,
            grant=platform.GrantPassword(
                username=conf.edp.username, password=conf.edp.password
            ),
        ).get_session()
        with session:
            assert session.open_state == OpenState.Opened
        assert session.open_state == OpenState.Closed

    @allure.title("Verify using platform session with asynchronous ContextManager")
    @pytest.mark.caseid("C44023030")
    @pytest.mark.smoke
    async def test_platform_session_is_opened_and_is_closed_using_async_context_manager(
        self,
    ):
        session = platform.Definition(
            app_key=conf.desktop_app_key,
            grant=platform.GrantPassword(
                username=conf.edp.username, password=conf.edp.password
            ),
        ).get_session()
        async with session:
            assert session.open_state == OpenState.Opened
        assert session.open_state == OpenState.Closed

    @allure.title(
        "Open Platform session with callbacks and verify that all cnx events are received"
    )
    @pytest.mark.parametrize(
        "expected_events",
        [[(OpenState.Pending, "Session opening in progress"),
          (OpenState.Opened, "Session is opened"),
          (EventCode.StreamConnecting, "apis.streaming.pricing.endpoints.main"),
          (EventCode.StreamConnected, "apis.streaming.pricing.endpoints.main"),
          (OpenState.Closed, "Session is closed")]],
    )
    def test_platform_session_with_callbacks(self, expected_events):
        event_list = []
        session = platform.Definition(
            app_key=conf.desktop_app_key,
            grant=platform.GrantPassword(
                username=conf.edp.username, password=conf.edp.password
            ),
        ).get_session()
        set_default(session)
        session.on_event(
            lambda event, message, session: on_event(
                event, message["api_cfg"], session, event_list
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
