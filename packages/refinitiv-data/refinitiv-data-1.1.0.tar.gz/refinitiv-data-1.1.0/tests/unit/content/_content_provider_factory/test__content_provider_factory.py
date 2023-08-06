from unittest.mock import patch

import pytest

from refinitiv.data import _configure as configure
from refinitiv.data.delivery._data import _data_provider_factory as factory
from tests.unit.conftest import StubConfigure, StubConfig


def test_get_url_method_return_not_none(content_type):
    # given
    get_url = factory.get_url
    config = configure.get_config()

    # when
    testing_value = get_url(content_type, config)

    # then
    assert testing_value is not None


def test_get_url_method_raise_error_if_invalid_content_type():
    # given
    content_type = None
    get_url = factory.get_url
    config = configure.get_config()

    # then
    with pytest.raises(AttributeError, match="Cannot find api_key"):
        # when
        get_url(content_type, config)


def test_get_url_method_raise_error_if_invalid_config(content_type):
    # given
    get_url = factory.get_url

    api_config_key = factory._get_api_config_key(content_type)
    url_config_key = factory._get_url_config_key(content_type)

    # then
    with pytest.raises(AttributeError, match="Cannot find content_url"):
        # when
        get_url(
            content_type,
            StubConfig({api_config_key: StubConfig({url_config_key: None})}),
        )


def test_make_provider_method_return_not_none(content_type):
    # given
    make_provider = factory.make_provider

    # when
    testing_value = make_provider(content_type)

    # then
    assert testing_value is not None


def test_make_provider_method_raise_error_if_invalid_content_type():
    # given
    content_type = None
    make_provider = factory.make_provider

    # then
    with pytest.raises(
        AttributeError, match="Cannot get data provider by content type"
    ):
        # when
        make_provider(content_type)
