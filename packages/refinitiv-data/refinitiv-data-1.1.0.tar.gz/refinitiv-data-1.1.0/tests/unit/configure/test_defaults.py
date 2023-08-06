from refinitiv.data import _configure as configure
from refinitiv.data import _config_defaults


def test_defaults():
    assert configure.defaults


def test_http_request_timeout():
    assert configure.defaults.http_request_timeout


def test_log_level():
    assert configure.defaults.log_level


def test_platform_server_mode():
    assert configure.defaults.platform_server_mode is not None


def test_checksum():
    assert _config_defaults.current_checksum == _config_defaults.fixed_checksum
