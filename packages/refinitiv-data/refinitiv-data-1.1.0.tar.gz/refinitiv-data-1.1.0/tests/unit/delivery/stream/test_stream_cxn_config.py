import pytest

from refinitiv.data.delivery._stream._stream_cxn_config_data import (
    StreamServiceInfo,
    PlatformStreamCxnConfig,
)


def test_first_info():
    # given
    first_info = StreamServiceInfo("", "first_info", "", "", "", "", "")
    infos = [
        first_info,
        StreamServiceInfo("", "second_info", "", "", "", "", ""),
        StreamServiceInfo("", "third_info", "", "", "", "", ""),
    ]
    config = PlatformStreamCxnConfig(infos, protocols=[""])

    # when

    # then
    assert config.info == first_info


def test_next_available_info():
    # given
    second_info = StreamServiceInfo("", "second_info", "", "", "", "", "")
    infos = [
        StreamServiceInfo("", "first_info", "", "", "", "", ""),
        second_info,
        StreamServiceInfo("", "third_info", "", "", "", "", ""),
    ]
    config = PlatformStreamCxnConfig(infos, protocols=[""])

    # when
    config.next_available_info()

    # then
    assert config.info == second_info


def test_last_info():
    # given
    infos = [
        StreamServiceInfo("", "first_info", "", "", "", "", ""),
        StreamServiceInfo("", "second_info", "", "", "", "", ""),
        StreamServiceInfo("", "third_info", "", "", "", "", ""),
    ]
    config = PlatformStreamCxnConfig(infos, protocols=[""])
    config.next_available_info()
    config.next_available_info()

    # then
    with pytest.raises(StopIteration):
        # when
        config.next_available_info()


def test_has_available_info():
    # given
    infos = [
        StreamServiceInfo("", "first_info", "", "", "", "", ""),
        StreamServiceInfo("", "second_info", "", "", "", "", ""),
        StreamServiceInfo("", "third_info", "", "", "", "", ""),
    ]
    config = PlatformStreamCxnConfig(infos, protocols=[""])

    # then
    assert config.has_available_info() is True


def test_info_not_available():
    # given
    infos = [
        StreamServiceInfo("", "first_info", "", "", "", "", ""),
        StreamServiceInfo("", "second_info", "", "", "", "", ""),
        StreamServiceInfo("", "third_info", "", "", "", "", ""),
    ]
    config = PlatformStreamCxnConfig(infos, protocols=[""])

    # when
    config.info_not_available()

    # then
    assert config.has_available_info() is True


def test_all_infos_not_available():
    # given
    infos = [
        StreamServiceInfo("", "first_info", "", "", "", "", ""),
        StreamServiceInfo("", "second_info", "", "", "", "", ""),
        StreamServiceInfo("", "third_info", "", "", "", "", ""),
    ]
    config = PlatformStreamCxnConfig(infos, protocols=[""])

    # when
    config.info_not_available()

    config.next_available_info()
    config.info_not_available()

    config.next_available_info()
    config.info_not_available()

    # then
    assert config.has_available_info() is False


def test_raise_if_all_infos_not_available_and_call_next_available_info():
    # given
    infos = [
        StreamServiceInfo("", "first_info", "", "", "", "", ""),
        StreamServiceInfo("", "second_info", "", "", "", "", ""),
        StreamServiceInfo("", "third_info", "", "", "", "", ""),
    ]
    config = PlatformStreamCxnConfig(infos, protocols=[""])

    config.info_not_available()

    config.next_available_info()
    config.info_not_available()

    config.next_available_info()
    config.info_not_available()

    # then
    with pytest.raises(ValueError):
        # when
        config.next_available_info()
