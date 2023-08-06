import os
import shutil
import pytest

from refinitiv.data import _configure as configure
from refinitiv.data.content.esg.bulk._package_manager import (
    get_console_logger,
    create_logpath,
    _PackageManager,
    get_package_config_by_package_name,
)
from tests.unit.conftest import StubSession


def test_get_console_logger():
    # given
    test_id = "1"

    # when
    result = get_console_logger(test_id)

    # then
    assert result


def test_create_log_path():
    # given
    package_name = "esg.test_package"
    configure.set_param(
        f"bulk.{package_name}.package.download.path",
        "test_folder",
        auto_create=True,
    )

    # when
    result = create_logpath(package_name)

    # then
    assert result == os.path.join("test_folder", "log.txt")

    os.rmdir("test_folder")


def test_file_manager():
    try:
        # given
        package_manager = _PackageManager("esg.standard_scores")
        # when
        fm = package_manager.file_manager
        # then
        assert fm is package_manager.file_manager
        shutil.rmtree("downloads")
    except OSError:
        pass


def test_get_package_config_by_package_name():
    # given
    package_name = "wrong_name"

    # then
    with pytest.raises(ValueError):
        # when
        get_package_config_by_package_name(package_name)


def test_file_manager_get_session():
    session = StubSession()
    package_manager = _PackageManager("esg.standard_scores", session)
    assert isinstance(package_manager.file_manager.session, StubSession)
