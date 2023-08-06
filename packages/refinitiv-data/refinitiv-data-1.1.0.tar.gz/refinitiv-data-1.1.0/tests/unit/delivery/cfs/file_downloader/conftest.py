from types import SimpleNamespace
from unittest.mock import mock_open
from unittest.mock import patch

import pytest


def create_stub_response(*args, **kwargs):
    response = SimpleNamespace()
    response.ok = True
    response.close = lambda: None
    response.iter_content = lambda: []
    return response


@pytest.fixture(scope="module", autouse=True)
def mock_download():
    os_makedirs_mock = patch("os.makedirs", new=lambda *_: None)
    requests_get_mock = patch("requests.get", new=create_stub_response)
    gzip_open_mock = patch("gzip.open", new=mock_open())
    file_downloader_open_mock = patch(
        "refinitiv.data.delivery.cfs._file_downloader.open", new=mock_open()
    )
    cfs_unpacker_open_mock = patch(
        "refinitiv.data.delivery.cfs._unpacker.open", new=mock_open()
    )

    os_makedirs_mock.start()
    cfs_unpacker_open_mock.start()
    requests_get_mock.start()
    gzip_open_mock.start()
    file_downloader_open_mock.start()

    yield

    os_makedirs_mock.stop()
    cfs_unpacker_open_mock.stop()
    requests_get_mock.stop()
    gzip_open_mock.stop()
    file_downloader_open_mock.stop()
