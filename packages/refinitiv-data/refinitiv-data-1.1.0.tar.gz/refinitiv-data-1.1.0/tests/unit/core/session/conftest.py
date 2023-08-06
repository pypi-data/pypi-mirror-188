import pytest

from refinitiv.data._core.session import (
    DesktopSession,
    PlatformSession,
    GrantPassword,
)


def create_platform_session():
    return PlatformSession(
        app_key="desktop_app_key",
        grant=GrantPassword(username="edp_username", password="edp_password"),
    )


def create_desktop_session():
    return DesktopSession(app_key="desktop_app_key")


@pytest.fixture(
    scope="function", params=[create_platform_session, create_desktop_session]
)
def session(request):
    create_session = request.param
    session = create_session()
    return session
