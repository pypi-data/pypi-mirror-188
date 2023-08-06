import pytest
import requests

from refinitiv.data._core import session
from refinitiv.data._core.session import UpdateEvent
from refinitiv.data._core.session._default_session_manager import Wrapper
from refinitiv.data._core.session.access_token_updater import AccessTokenUpdater
from refinitiv.data._core.session.auth_manager import TokenInfo
from refinitiv.data._core.session.refresh_token_updater import RefreshTokenUpdater
from refinitiv.data._core.session.tools import Delays
from tests.unit.conftest import StubSession, StubResponse

codes = requests.codes


@pytest.fixture(scope="function")
def auth_manager(request):
    #
    expires_in = 3
    marker_expires_in = request.node.get_closest_marker("expires_in")
    if marker_expires_in is not None:
        expires_in = marker_expires_in.args[0]

    #
    status_code = 200
    marker_status_code = request.node.get_closest_marker("status_code")
    if marker_status_code is not None:
        status_code = marker_status_code.args[0]

    content_data = {
        "access_token": "access_token",
        "expires_in": expires_in,
        "scope": "scope",
        "refresh_token": "refresh_token",
        "token_type": "token_type",
    }
    response = StubResponse(content_data)
    response.status_code = status_code
    session_mock = StubSession(response=response)
    auto_reconnect = False
    am = session.AuthManager(session_mock, auto_reconnect)
    yield am
    am.dispose()


@pytest.mark.parametrize("auto_reconnect", [True, False])
def test_authorize_is_true_if_success_authorization(auth_manager, auto_reconnect):
    # given
    auth_manager._auto_reconnect = auto_reconnect

    # when
    authorized = auth_manager.authorize()

    # then
    assert authorized is True


@pytest.mark.parametrize("auto_reconnect", [True, False])
def test_is_authorized_return_true_if_success_authorization(
    auth_manager, auto_reconnect
):
    # given
    auth_manager._auto_reconnect = auto_reconnect

    # when
    auth_manager.authorize()

    # then
    assert auth_manager.is_authorized() is True


@pytest.mark.status_code(404)
@pytest.mark.parametrize("auto_reconnect", [False])
def test_authorize_return_false_if_fail(auth_manager, auto_reconnect):
    # given
    auth_manager._auto_reconnect = auto_reconnect

    # when
    authorized = auth_manager.authorize()

    # then
    assert authorized is False


@pytest.mark.status_code(404)
@pytest.mark.parametrize("auto_reconnect", [False])
def test_is_authorized_return_false_if_closed(auth_manager, auto_reconnect):
    # given
    auth_manager._auto_reconnect = auto_reconnect

    # when
    testing_value = auth_manager.is_authorized()

    # then
    assert testing_value is False


@pytest.mark.parametrize("auto_reconnect", [True, False])
def test_authorize_twice(auth_manager, auto_reconnect):
    # given
    auth_manager._auto_reconnect = auto_reconnect

    # when
    auth_manager.authorize()
    testing_value = auth_manager.authorize()

    # then
    assert testing_value is True


def test_refresh_token_updater_will_raise_error_if_delay_less_or_equal_then_0():
    # given
    updater = RefreshTokenUpdater(
        StubSession(), Wrapper(), 1, lambda *args, **kwargs: None
    )

    # then
    with pytest.raises(ValueError, match="Delay must be greater than 0"):
        # when
        updater.delay = 0


def test_access_token_updater_will_raise_error_if_delay_less_or_equal_then_0():
    # given
    updater = AccessTokenUpdater(StubSession(), 1, lambda *args, **kwargs: None)

    # then
    with pytest.raises(ValueError, match="Delay must be greater than 0"):
        # when
        updater.delay = 0


@pytest.mark.parametrize(
    "status_code",
    [codes.ok, codes.bad, codes.unauthorized, codes.forbidden, codes.not_found],
)
def test_access_token_updater_can_process_status_codes(status_code):
    handled = False

    def handler(*args, **kwargs):
        nonlocal handled
        handled = True
        updater.stop()

    # given
    response = StubResponse(status_code=status_code)
    updater = AccessTokenUpdater(StubSession(response=response), 0.001, handler)

    # when
    updater.start()

    # then
    assert handled is True


@pytest.mark.parametrize(
    "status_code",
    [
        codes.ok,
    ],
)
def test_access_token_updater_return_event_ACCESS_TOKEN_SUCCESS(status_code):
    event = None

    def handler(event_, message, json_content):
        nonlocal event
        event = event_
        updater.stop()

    # given
    response = StubResponse(status_code=status_code)
    updater = AccessTokenUpdater(StubSession(response=response), 0.001, handler)

    # when
    updater.start()

    # then
    assert event == UpdateEvent.ACCESS_TOKEN_SUCCESS


@pytest.mark.parametrize(
    "status_code",
    [
        codes.bad,
        codes.unauthorized,
        codes.forbidden,
    ],
)
def test_access_token_updater_return_event_ACCESS_TOKEN_UNAUTHORIZED(status_code):
    event = None

    def handler(event_, message, json_content):
        nonlocal event
        event = event_
        updater.stop()

    # given
    response = StubResponse(status_code=status_code)
    updater = AccessTokenUpdater(StubSession(response=response), 0.001, handler)

    # when
    updater.start()

    # then
    assert event == UpdateEvent.ACCESS_TOKEN_UNAUTHORIZED


@pytest.mark.parametrize("status_code", [codes.not_found])
def test_access_token_updater_return_event_ACCESS_TOKEN_FAILED(status_code):
    event = None

    def handler(event_, message, json_content):
        nonlocal event
        event = event_
        updater.stop()

    # given
    response = StubResponse(status_code=status_code)
    updater = AccessTokenUpdater(StubSession(response=response), 0.001, handler)

    # when
    updater.start()

    # then
    assert event == UpdateEvent.ACCESS_TOKEN_FAILED


@pytest.mark.parametrize(
    "status_code",
    [codes.ok, codes.bad, codes.unauthorized, codes.forbidden, codes.not_found],
)
def test_refresh_token_updater_can_process_status_codes(status_code):
    handled = False

    def handler(*args, **kwargs):
        nonlocal handled
        handled = True
        updater.stop()

    # given
    response = StubResponse(status_code=status_code)
    updater = RefreshTokenUpdater(
        StubSession(response=response),
        TokenInfo("", 1, {""}, ""),
        0.001,
        handler,
    )

    # when
    updater.start()

    # then
    assert handled is True


@pytest.mark.parametrize(
    "status_code",
    [
        codes.ok,
    ],
)
def test_refresh_token_updater_return_event_REFRESH_TOKEN_SUCCESS(status_code):
    event = None

    def handler(event_, message, json_content):
        nonlocal event
        event = event_
        updater.stop()

    # given
    response = StubResponse(status_code=status_code)
    updater = RefreshTokenUpdater(
        StubSession(response=response),
        TokenInfo("", 1, {""}, ""),
        0.001,
        handler,
    )

    # when
    updater.start()

    # then
    assert event == UpdateEvent.REFRESH_TOKEN_SUCCESS


@pytest.mark.parametrize(
    "status_code",
    [
        codes.bad,
        codes.unauthorized,
        codes.forbidden,
    ],
)
def test_refresh_token_updater_return_event_REFRESH_TOKEN_BAD(status_code):
    event = None

    def handler(event_, message, json_content):
        nonlocal event
        event = event_
        updater.stop()

    # given
    response = StubResponse(status_code=status_code)
    updater = RefreshTokenUpdater(
        StubSession(response=response),
        TokenInfo("", 1, {""}, ""),
        0.001,
        handler,
    )

    # when
    updater.start()

    # then
    assert event == UpdateEvent.REFRESH_TOKEN_BAD


@pytest.mark.parametrize("status_code", [codes.not_found])
def test_refresh_token_updater_return_event_REFRESH_TOKEN_FAILED(status_code):
    event = None

    def handler(event_, message, json_content):
        nonlocal event
        event = event_
        updater.stop()

    # given
    response = StubResponse(status_code=status_code)
    updater = RefreshTokenUpdater(
        StubSession(response=response),
        TokenInfo("", 1, {""}, ""),
        0.001,
        handler,
    )

    # when
    updater.start()

    # then
    assert event == UpdateEvent.REFRESH_TOKEN_FAILED


def test_delays_next():
    # given
    delays = Delays([1])

    # when
    delay = delays.next()

    # then
    assert delay == 1


def test_delays_next_twice():
    # given
    delays = Delays([1, 2])

    # when
    delay = delays.next()
    delay = delays.next()

    # then
    assert delay == 2


def test_delays_next_twice_same_result():
    # given
    delays = Delays([1])

    # when
    delay = delays.next()
    delay = delays.next()

    # then
    assert delay == 1


def test_delays_reset():
    # given
    delays = Delays([2, 1])

    # when
    delay = delays.next()
    delay = delays.next()
    delays.reset()
    delay = delays.next()

    # then
    assert delay == 2


def test_auth_manager_mandatory_parameters_for_access_token_updater():
    # given
    content_data = {
        "access_token": "access_token",
        "refresh_token": "refresh_token",
    }
    session_mock = StubSession()
    am = session.AuthManager(session_mock, False)

    try:
        # when
        am._access_token_update_handler(
            UpdateEvent.ACCESS_TOKEN_SUCCESS, "", content_data
        )
    except Exception as e:
        assert False, e
    else:
        assert True


def test_auth_manager_mandatory_parameters_for_refresh_token_updater():
    # given
    content_data = {
        "access_token": "access_token",
        "refresh_token": "refresh_token",
    }
    session_mock = StubSession()
    am = session.AuthManager(session_mock, False)

    try:
        # when
        am._refresh_token_update_handler(
            UpdateEvent.REFRESH_TOKEN_SUCCESS, "", content_data
        )
    except Exception as e:
        assert False, e
    else:
        assert True
