import pytest

from refinitiv.data import _configure as configure


@pytest.mark.parametrize(
    "method_name",
    [
        "desktop_session",
        "desktop_base_uri",
        "desktop_platform_paths",
        "desktop_handshake_url",
        "desktop_endpoints",
        "platform_session",
        "platform_endpoints",
        "platform_base_uri",
        "platform_auth_uri",
        "platform_token_uri",
        "platform_auto_reconnect",
        "platform_server_mode",
        "platform_realtime_distribution_system",
    ],
)
def test_config_keys(method_name):
    # given
    testing_subst = "test"
    configure.reload()

    # when
    testing_method = getattr(configure._keys, method_name)
    key = testing_method(testing_subst)

    assert testing_subst in key
