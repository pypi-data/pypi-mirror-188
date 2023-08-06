import os

import pytest

from refinitiv.data import _configure as configure
from .conftest import (
    remove_user_config,
    write_user_config,
    expected_default_user_config_path,
    expected_default_project_config_path,
    remove_project_config,
    write_project_config,
    get_user_config_path,
    get_project_config_path,
    expected_default_config_filename,
    RDPLIB_ENV_DIR,
    RD_LIB_CONFIG_PATH,
    get_client_config_path,
    annotate,
)


def test_number_config_files_paths_by_default_is_2():
    # given

    # when
    configure.reload()

    # then
    assert len(configure._config_files_paths) == 2


def test_default_config_filename():
    # given

    # when
    configure.reload()

    # then
    assert configure._default_config_file_name == expected_default_config_filename


def test_user_config_file_not_exists_but_has_in_config_files_paths():
    # given
    remove_user_config()

    # when
    configure.reload()

    # then
    assert get_user_config_path(configure) == expected_default_user_config_path


def test_user_config_file_exists():
    # given
    write_user_config('{"prop": "value"}')

    # when
    configure.reload()

    # then
    assert get_user_config_path(configure) == expected_default_user_config_path


def test_user_config_file_created_after_module_imported():
    # given
    configure.reload()

    # when
    write_user_config('{"prop": "value"}')

    # then
    assert get_user_config_path(configure) == expected_default_user_config_path


def test_project_config_file_not_exists_but_has_in_config_files_paths():
    # given
    remove_project_config()

    # when
    configure.reload()

    # then
    assert get_project_config_path(configure) == expected_default_project_config_path


def test_project_config_file_exists():
    # given
    write_project_config('{"prop":"value"}')

    # when
    configure.reload()

    # then
    assert get_project_config_path(configure) == expected_default_project_config_path


def test_project_config_file_created_after_module_imported():
    # given
    configure.reload()

    # when
    write_user_config('{"prop": "value"}')

    # then
    assert get_project_config_path(configure) == expected_default_project_config_path


def test_set_RDPLIB_ENV_DIR(monkeypatch, tmpdir):
    # given
    testing_env_dir = "test_env_dir"
    monkeypatch.setenv(RDPLIB_ENV_DIR, testing_env_dir)

    # when
    configure.reload()

    # then
    assert testing_env_dir in get_project_config_path(configure)


def test_set_RDPLIB_ENV_and_set_RDPLIB_ENV_DIR(monkeypatch, tmpdir):
    #  given
    testing_env_dir = "test_env_dir"
    monkeypatch.setenv(RDPLIB_ENV_DIR, testing_env_dir)
    # when
    configure.reload()
    # then
    assert testing_env_dir in get_project_config_path(configure)


@pytest.mark.parametrize("testing_path", ["/test/path/to/", "\\test\\path\\to\\"])
def test_set_RDP_LIB_CONFIG(monkeypatch, testing_path):
    # given
    monkeypatch.setenv(RD_LIB_CONFIG_PATH, testing_path)

    # when
    configure.reload()

    # then
    assert get_client_config_path(configure) == os.path.join(
        testing_path, "refinitiv-data.config.json"
    )


@pytest.mark.parametrize(
    "testing_rootdir, testing_filename, expected_filepath",
    [annotate(rootdir=None, filename=None, expected_filepath=None)],
)
def test_get_filepath_function(testing_rootdir, testing_filename, expected_filepath):
    # given
    configure.reload()

    # when
    testing_filepath = configure._get_filepath(testing_rootdir, testing_filename)

    # then
    assert testing_filepath == expected_filepath
