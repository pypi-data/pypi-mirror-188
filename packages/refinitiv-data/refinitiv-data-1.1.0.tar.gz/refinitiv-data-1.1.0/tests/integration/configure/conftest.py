import json
import os

import pytest

from refinitiv.data import _configure as configure
from tests.integration.conftest import remove_config


def pytest_addoption(parser):
    parser.addoption(
        "--unit", action="store_true", default=False, help="run unit tests"
    )
    parser.addoption(
        "--integrate", action="store_true", default=False, help="run integration tests"
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "integrate: mark test as integration test")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--unit"):
        skip = pytest.mark.skip(reason="run only unit tests")
        for item in items:
            if "unit" not in item.keywords:
                item.add_marker(skip)

    if config.getoption("--integrate"):
        skip = pytest.mark.skip(reason="run only integration tests")
        for item in items:
            if "integrate" not in item.keywords:
                item.add_marker(skip)


USER_CONFIG_PATH = os.path.join(
    os.path.expanduser("~"), configure._default_config_file_name
)


def remove_user_config():
    remove_config(USER_CONFIG_PATH)


def pytest_runtest_teardown(item, nextitem):
    configure._dispose()


@pytest.fixture()
def user_config_path():
    return USER_CONFIG_PATH


@pytest.fixture(scope="function")
def write_user_config(user_config_path):
    def inner(s):
        if isinstance(s, dict):
            s = json.dumps(s)
        f = open(user_config_path, "w")
        f.write(s)
        f.close()
        return user_config_path

    yield inner

    configure._dispose()

    remove_user_config()


@pytest.fixture
def reload_config_on_teardown():
    yield
    configure.reload()


def open_session_and_get_base_url(session):
    session.open()
    base_url = session._base_url
    session.close()

    return base_url
