import refinitiv.data as rd
from refinitiv.data._core.session.grant_password import GrantPassword
from refinitiv.data._core.session.http_service import get_http_limits


def test_session_event_code():
    import refinitiv.data as rd

    try:
        rd.session.EventCode
    except Exception as e:
        assert False, str(e)


def test_session_id():
    session_1 = rd.session.desktop.Definition(app_key="foo").get_session()
    session_2 = rd.session.platform.Definition(
        app_key="foo", grant=GrantPassword(username="username", password="password")
    ).get_session()
    session_3 = rd.session.desktop.Definition(app_key="foo").get_session()

    assert session_1.session_id is not None
    assert session_2.session_id == session_1.session_id + 1
    assert session_3.session_id == session_2.session_id + 1


def test_get_http_limits():
    # given
    max_connections = 21
    max_keepalive_connections = max_connections
    config = {
        "http.max-connections": max_connections,
        "http.max-keepalive-connections": max_keepalive_connections,
    }

    # when
    result = get_http_limits(config)

    # then
    assert result.max_connections == max_connections
    assert result.max_keepalive_connections == max_keepalive_connections
