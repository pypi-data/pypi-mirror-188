import json
import os
from importlib import import_module

import pytest

from refinitiv.data import _configure as configure

RDPLIB_ENV = "RDPLIB_ENV"
RDPLIB_ENV_DIR = "RDPLIB_ENV_DIR"
RD_LIB_CONFIG_PATH = "RD_LIB_CONFIG_PATH"

expected_default_config_filename = "refinitiv-data.config.json"
expected_default_user_config_path = os.path.join(
    os.path.expanduser("~"), expected_default_config_filename
)
expected_default_project_config_path = os.path.join(
    os.getcwd(), expected_default_config_filename
)


def annotate(**kwargs):
    return list(kwargs.values())


@pytest.fixture(autouse=True)
def setup_teardown_function(monkeypatch):
    monkeypatch.delenv(RDPLIB_ENV, raising=False)
    monkeypatch.delenv(RDPLIB_ENV_DIR, raising=False)
    monkeypatch.delenv(RD_LIB_CONFIG_PATH, raising=False)

    configure.reload()

    yield

    remove_user_config()
    remove_project_config()


def get_client_config_path(configure):
    return configure._config_files_paths[0]


def get_project_config_path(configure):
    return configure._config_files_paths[0]


def get_user_config_path(configure):
    return configure._config_files_paths[1]


def get_default_config_path(configure):
    return configure._config_files_paths[2]


def remove_config(path):
    while os.path.exists(path):
        try:
            os.remove(path)
        except (PermissionError, FileNotFoundError):
            pass


def remove_user_config():
    remove_config(expected_default_user_config_path)


def remove_project_config():
    remove_config(expected_default_project_config_path)


def write_config(path, s):
    if isinstance(s, dict):
        s = json.dumps(s)
    with open(path, "w") as f:
        f.write(s)

    return write_config


def write_user_config(s):
    write_config(expected_default_user_config_path, s)


def write_project_config(s):
    write_config(expected_default_project_config_path, s)


ENV_NAME = "USER"
ENV_VALUE = "TestingUser"


@pytest.fixture
def mock_env_user(monkeypatch):
    monkeypatch.setenv(ENV_NAME, ENV_VALUE)


@pytest.fixture
def mock_env_missing(monkeypatch):
    monkeypatch.delenv(ENV_NAME, raising=False)
