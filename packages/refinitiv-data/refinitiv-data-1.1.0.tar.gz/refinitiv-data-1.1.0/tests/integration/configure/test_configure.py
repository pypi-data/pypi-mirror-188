import os
import random

from refinitiv.data import _configure as configure
from . import conftest
from ..conftest import remove_project_config

BASE_URL = "https://api.refinitiv.com"
TEST_BASE_URL = "https://api.test.refinitiv.com"

EXPECTED_CONFIG_FILE_PATHS_COUNT = 2

# endregion


# region USER_CONFIG_FILE
def test_user_config_file_path_not_exists(user_config_path, write_user_config):
    path = write_user_config('{"prop": "value"}')

    configure.reload()
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert path == configure._config_files_paths[1]

    conftest.remove_user_config()

    configure.reload()
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert path != configure._config_files_paths[0]


def test_user_config_file_path_already_exists(write_user_config):
    path = write_user_config('{"prop": "value"}')

    configure.reload()
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert path == configure._config_files_paths[1]
    assert path != configure._config_files_paths[0]


def test_user_config_file_path_created_after_load_package(user_config_path):
    conftest.remove_user_config()

    configure.reload()
    with open(user_config_path, "w"):
        pass
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert user_config_path != configure._config_files_paths[0]

    conftest.remove_user_config()


# endregion


# region PROJECT_CONFIG_FILE
def test_project_config_file_path_not_exists(project_config_path):
    remove_project_config()

    configure.reload()
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert project_config_path != configure._config_files_paths[1]


def test_project_config_file_path_already_exists(write_project_config):
    path = write_project_config('{"prop":"value"}')

    configure.reload()
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert path == configure._config_files_paths[0]
    assert path != configure._config_files_paths[1]


def test_project_config_file_path_created_at_runtime(project_config_path):
    remove_project_config()

    configure.reload()
    with open(project_config_path, "w"):
        pass
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert project_config_path != configure._config_files_paths[1]


# endregion


def test_environ_env_name_and_env_dir(monkeypatch, tmpdir):
    env_dir = str(random.randint(0, 100))
    d = tmpdir / env_dir
    d.mkdir()
    f = tmpdir / env_dir / (configure._default_config_file_name)
    f.write('{"prop": "value"}')

    monkeypatch.setenv(configure._RDPLIB_ENV_DIR, str(d))

    configure.reload()

    assert d == configure._project_config_dir
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert f == configure._config_files_paths[0]


def test_environ_env_name(monkeypatch):
    from pathlib import Path

    f = Path(os.getcwd()) / (configure._default_config_file_name)
    f.write_text('{"prop": "value"}', encoding="utf-8")

    monkeypatch.delenv(configure._RDPLIB_ENV_DIR, raising=False)

    configure.reload()
    assert os.getcwd() == configure._project_config_dir
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert str(f) == configure._config_files_paths[0]

    f.unlink()
    monkeypatch.delenv(configure._RD_LIB_CONFIG_PATH, raising=False)


def test_environ_env_dir(monkeypatch, tmpdir):
    configure.reload()
    env_dir = str(random.randint(0, 100))
    d = tmpdir / env_dir
    d.mkdir()
    f = tmpdir / env_dir / configure._default_config_file_name
    f.write('{"prop": "value"}')

    monkeypatch.setenv(configure._RDPLIB_ENV_DIR, str(d))

    configure.reload()
    assert d == configure._project_config_dir
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert str(f) == configure._config_files_paths[0]


def test_environ_empty(monkeypatch):
    from pathlib import Path

    f = Path(os.getcwd()) / configure._default_config_file_name
    f.write_text('{"prop": "value"}', encoding="utf-8")

    monkeypatch.delenv(configure._RDPLIB_ENV_DIR, raising=False)

    configure.reload()
    assert os.getcwd() == configure._project_config_dir
    assert EXPECTED_CONFIG_FILE_PATHS_COUNT == len(configure._config_files_paths)
    assert str(f) == configure._config_files_paths[0]

    f.unlink()


def test_config_provided_by_user(monkeypatch, tmp_path):
    assert (
        configure.get_config().get_str("sessions.platform.default.base-url")
        == "https://api.refinitiv.com"
    )
    config_path = os.path.dirname(os.path.realpath(__file__))
    monkeypatch.setenv(configure._RD_LIB_CONFIG_PATH, config_path)
    configure.reload()
    assert (
        configure.get_config().get_str("sessions.platform.default.base-url")
        == "https://api.test.refinitiv.com"
    )
    monkeypatch.delenv(configure._RD_LIB_CONFIG_PATH, raising=False)
    configure.reload()


def test_config_provided_by_user_load():
    assert (
        configure.get_config().get_str("sessions.platform.default.base-url")
        == "https://api.refinitiv.com"
    )
    config_path = os.path.dirname(os.path.realpath(__file__))
    custom_config_path = os.path.join(config_path, "refinitiv-data.config.json")
    configure.get_config().load(custom_config_path)
    assert (
        configure.get_config().get_str("sessions.platform.default.base-url")
        == "https://api.test.refinitiv.com"
    )
    configure.reload()
