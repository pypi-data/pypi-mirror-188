from pathlib import Path

import pytest

from refinitiv.data.delivery.cfs import file_downloader
from refinitiv.data.delivery.cfs._file_downloader_facade import FileDownloader
from tests.unit.conftest import StubSession


def test_call_download_without_path():
    # given
    input_value = "filename.json.gzip"
    expected_value = Path("filename.json.gzip")
    file_downloader = FileDownloader(url="", filename_ext=input_value)

    # when
    file_downloader.download()
    testing_value = Path(file_downloader._downloaded_filepath)

    # then
    assert testing_value == expected_value


def test_call_download_with_pass_path():
    # given
    input_value = "filename.json.gzip"
    expected_value = Path("path/to/file/filename.json.gzip")
    file_downloader = FileDownloader(url="", filename_ext=input_value)

    # when
    file_downloader.download("path/to/file")
    testing_value = Path(file_downloader._downloaded_filepath)

    # then
    assert testing_value == expected_value


def test_call_extract_without_path():
    # given
    input_value = "filename.json.gzip"
    expected_value = "filename.json"
    file_downloader = FileDownloader(url="", filename_ext=input_value)

    # when
    testing_value = file_downloader.extract()

    # then
    assert testing_value == expected_value


def test_call_extract_with_pass_path():
    # given
    input_value = "filename.json.gzip"
    expected_value = Path("path/to/file/filename.json")
    file_downloader = FileDownloader(url="", filename_ext=input_value)

    # when
    testing_value = file_downloader.extract("path/to/file")
    testing_value = Path(testing_value)

    # then
    assert testing_value == expected_value


def test_call_download_then_call_extract_methods():
    # given
    input_value = "filename.json.gzip"
    expected_value = "filename.json"
    file_downloader = FileDownloader(url="", filename_ext=input_value)

    # when
    testing_value = file_downloader.download().extract()

    # then
    assert testing_value == expected_value


def test_call_download_with_path_then_call_extract_with_path():
    # given
    input_value = "filename.json.gzip"
    expected_value = Path("path/to/extract/filename.json")
    file_downloader = FileDownloader(url="", filename_ext=input_value)

    # when
    testing_value = file_downloader.download("path/to/download").extract(
        "path/to/extract"
    )
    testing_value = Path(testing_value)

    # then
    assert testing_value == expected_value


def test_call_download_with_path_then_call_extract():
    # given
    input_value = "filename.json.gzip"
    expected_value = Path("path/to/download/filename.json")
    file_downloader = FileDownloader(url="", filename_ext=input_value)

    # when
    testing_value = file_downloader.download("path/to/download").extract()
    testing_value = Path(testing_value)

    # then
    assert testing_value == expected_value


def test_call_download_then_call_extract_with_path():
    # given
    input_value = "filename.json.gzip"
    expected_value = Path("path/to/extract/filename.json")
    file_downloader = FileDownloader(url="", filename_ext=input_value)

    # when
    testing_value = file_downloader.download().extract("path/to/extract")
    testing_value = Path(testing_value)

    # then
    assert testing_value == expected_value


def test_cfs_stream():
    session = StubSession(is_open=True)
    definition = file_downloader.Definition(
        {"id": "file_id", "filename": "filename_ext"}
    )

    with pytest.raises(FileNotFoundError, match="file not found"):
        definition.retrieve(session)
