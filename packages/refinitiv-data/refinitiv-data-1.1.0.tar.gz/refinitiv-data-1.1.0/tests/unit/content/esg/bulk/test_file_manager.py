from types import SimpleNamespace
from unittest.mock import patch

import pytest

from .conftest import raise_

package = {
    "bucket": "ESG",
    "name": "RFT-ESG-Scores-Wealth-Standard",
    "download": {
        "path": "./downloads/esg/standard_scores",
        "auto-extract": False,
        "auto-retry": {"enabled": False},
    },
}
logger = SimpleNamespace()
logger.log = lambda *_: None
logger.warning = lambda *_: None
logger.error = lambda *_: None
logger.debug = lambda *_: None
logger.info = lambda *_: None


def test_clean_up_files(file_manager):
    # given
    remove_file_mock = patch("os.remove", new=lambda *_: _)

    # when
    remove_file_mock.start()
    result = file_manager.cleanup_files()
    remove_file_mock.stop()

    # then
    assert result is None


def test_clean_up_files_if_permissions_error(file_manager):
    # given
    remove_file_mock = patch("os.remove", new=lambda *_: raise_(PermissionError))

    # when
    remove_file_mock.start()
    result = file_manager.cleanup_files()
    remove_file_mock.stop()

    # then
    assert result is None


def test_file_manager_read_file(file_manager):
    # given
    mock_path_exists = patch("os.path.exists", new=lambda: False)

    # when
    # then
    with pytest.raises(FileNotFoundError):
        file_manager.read_file("filename")
