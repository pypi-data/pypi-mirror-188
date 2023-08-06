import os
import random

import pandas as pd
import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data.content._df_builder_factory import get_dfbuilder
from refinitiv.data.content.filings._retrieval_data_provider import (
    Error,
    DownloadFileError,
    FilingsRequestFactory,
    DownloadAllFileResponse,
    DownloadFileResponse,
    FilingsFile,
    ListOfFile,
    FilingsData,
)
from tests.unit.conftest import StubSession


# ---------------------------------------------------------------------------
#   Test FilingRequestFactory
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("input_value", "expected_url"),
    [
        ({}, ""),
        ({"filename": "test"}, "/{filename}"),
        ({"dcn": "test"}, "/search/{identifier}/{value}"),
        ({"doc_id": "test"}, "/search/{identifier}/{value}"),
        ({"filing_id": "test"}, "/search/{identifier}/{value}"),
    ],
)
def test_filing_request_factory_get_url(input_value, expected_url):
    # given
    prefix_url = "/data/filings/v1/retrieval"
    session = None

    # when
    url = FilingsRequestFactory().get_url(session, prefix_url, **input_value)

    # then
    assert url == f"{prefix_url}{expected_url}"


@pytest.mark.parametrize(
    ("input_value", "expected_path_parameters"),
    [
        ({}, {}),
        ({"filename": "filename_1"}, {"filename": "filename_1"}),
        (
            {"dcn": "dcn_1"},
            {"identifier": "dcn", "value": "dcn_1"},
        ),
        (
            {"doc_id": "doc_id_1"},
            {"identifier": "docid", "value": "doc_id_1"},
        ),
        (
            {"filing_id": "filing_id_1"},
            {"identifier": "filingid", "value": "filing_id_1"},
        ),
    ],
)
def test_filing_request_factory_get_path_parameters(
    input_value, expected_path_parameters
):
    # when
    session = StubSession()
    path_parameters = FilingsRequestFactory().get_path_parameters(
        session, **input_value
    )

    # then
    assert path_parameters == expected_path_parameters


def test_filing_request_factory_get_header_parameters():
    # given
    session = StubSession(is_open=True)
    # header is currently hard-coded in their document
    expected_headers = {
        "ClientID": "API_Playground",
        "X-Api-Key": "155d9dbf-f0ac-46d9-8b77-f7f6dcd238f8",
        "Accept": "*/*",
    }

    # when
    headers = FilingsRequestFactory().get_header_parameters(session)

    # then
    assert headers == expected_headers


# ---------------------------------------------------------------------------
#   Test FilingsFile
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("attrib", (["filename", "signed_url", "mimetype"]))
def test_filings_file_attrib(attrib):
    # when
    filings_file = FilingsFile()

    # then
    assert hasattr(filings_file, attrib)


def test_filing_file_download(mock_server_success):
    # given
    filename = "name.txt"
    server_port = mock_server_success.server_port

    # when
    response = FilingsFile("name", f"http://127.0.0.1:{server_port}").download()
    obj_id = hex(id(response))

    # then
    assert os.path.exists(filename)

    with open(filename, "r") as f:
        content = f.read()
    assert content == "test text"

    os.remove(filename)


def test_filing_file_download_http_error(mock_server_error):
    # given
    server_port = mock_server_error.server_port

    # when
    f = FilingsFile("name", f"http://127.0.0.1:{server_port}")

    # then
    with pytest.raises(DownloadFileError) as err:
        f.download()
    assert err.value.code == 404
    assert err.value.message == "File not found"


def test_filing_file_download_file_location_error(mock_server_success):
    # given
    server_port = mock_server_success.server_port

    # when
    f = FilingsFile("name", f"http://127.0.0.1:{server_port}")

    # then
    with pytest.raises(DownloadFileError) as err:
        f.download(
            path=os.path.join(
                os.getcwd(),
                f"FILINGS_INVALID_PATH_{str(random.randint(0, 999999))}",
            )
        )

    assert "No such directory exists" in err.value.message


def test_filing_file_download_none_error(mock_server_error):
    # when
    f = FilingsFile("name")

    # then
    with pytest.raises(DownloadFileError) as err:
        f.download()

    assert "Invalid type for url" in err.value.message


@pytest.mark.asyncio
async def test_filing_file_download_async(mock_server_success):
    # given
    filename = "name.txt"
    server_port = mock_server_success.server_port

    def on_complete(resp):
        assert len(resp.errors) == 0

    # when
    await FilingsFile("name", f"http://127.0.0.1:{server_port}").download_async(
        callback=on_complete
    )

    # then
    assert os.path.exists(filename)

    with open(filename, "r") as f:
        content = f.read()
    assert content == "test text"

    os.remove(filename)


@pytest.mark.asyncio
async def test_filing_file_download_async_http_error(mock_server_error):
    # given
    server_port = mock_server_error.server_port

    def on_complete(resp):
        assert len(resp.errors) == 1

    # when
    filing = FilingsFile("name", f"http://127.0.0.1:{server_port}")
    response = await filing.download_async(callback=on_complete)

    # then
    assert len(response.errors) == 1


@pytest.mark.asyncio
async def test_filing_file_download_async_file_location_error(mock_server_success):
    # given
    server_port = mock_server_success.server_port

    def on_complete(resp):
        assert len(resp.errors) == 1

    # when
    response = await FilingsFile(
        "name", f"http://127.0.0.1:{server_port}"
    ).download_async(
        path=os.path.join(
            os.getcwd(),
            f"FILINGS_INVALID_PATH_{str(random.randint(0, 999999))}",
        ),
        callback=on_complete,
    )

    # then
    assert "No such directory exists" in response.errors[0].message


@pytest.mark.asyncio
async def test_filing_file_download_async_none_error(mock_server_error):
    # given
    filing = FilingsFile("name")

    # when
    response = await filing.download_async()

    # then
    assert "Invalid type for url" in response.errors[0].message


# ---------------------------------------------------------------------------
#   Test FilingData
# ---------------------------------------------------------------------------


def test_filings_data_df_none():
    # given
    df_builder = get_dfbuilder(ContentType.FILINGS_RETRIEVAL)

    # when
    df = FilingsData(raw={}, use_field=False, dfbuilder=df_builder).df

    assert df is None


@pytest.mark.parametrize(
    ("input_value", "expected_data"),
    [
        (
            {"signedUrl": "http://example/file_pdf"},
            [["file_pdf", "http://example/file_pdf", ""]],
        ),
        (
            {
                "file_pdf": {"signedUrl": "http://example/file_pdf", "mimeType": "pdf"},
                "file_txt": {"signedUrl": "http://example/file_txt", "mimeType": "txt"},
            },
            [
                ["file_pdf", "http://example/file_pdf", "pdf"],
                ["file_txt", "http://example/file_txt", "txt"],
            ],
        ),
    ],
)
def test_filings_data_df(input_value, expected_data):
    # given
    columns = ["Filename", "SignedURL", "MimeType"]
    expected_df = pd.DataFrame(data=expected_data, columns=columns)
    df_builder = get_dfbuilder(ContentType.FILINGS_RETRIEVAL)

    # when
    data = FilingsData(input_value, use_field=False, dfbuilder=df_builder)
    df = data.df

    # then
    assert df.compare(expected_df).empty


def test_filing_data_files():
    # given
    content = {"signedUrl": "http://example/file_pdf"}
    df_builder = get_dfbuilder(ContentType.FILINGS_RETRIEVAL)

    # when
    data = FilingsData(content, use_field=False, dfbuilder=df_builder).files

    # then
    f = data[0]
    assert type(f) == FilingsFile
    assert f.filename == "file_pdf"
    assert f.signed_url == "http://example/file_pdf"


def test_filings_data_files_when_df_is_none():
    # given
    df_builder = get_dfbuilder(ContentType.FILINGS_RETRIEVAL)

    # when
    data = FilingsData(None, use_field=False, dfbuilder=df_builder)

    # then
    assert len(data.files) == 0


def test_filings_download_file_response_errors():
    # given
    kwargs = {"error_code": [400, 401], "error_message": ["Error1", "Error2"]}

    # when
    response = DownloadFileResponse(**kwargs)

    # then
    assert response.errors == [Error(400, "Error1"), Error(401, "Error2")]


def test_filings_download_all_file_response():
    # given
    errors = []
    files = []

    # when
    response = DownloadAllFileResponse(files, errors)

    # then
    assert response.data.files == files
    assert response.errors == errors


def test_filings_list_of_file_download(mock_server_success):
    # given
    filename = "name.txt"
    server_port = mock_server_success.server_port

    # when
    list_of_file = ListOfFile()
    list_of_file.append(FilingsFile("name", f"http://127.0.0.1:{server_port}"))
    list_of_file.download()

    # then
    assert os.path.exists(filename)

    with open(filename, "r") as f:
        content = f.read()
    assert content == "test text"

    os.remove(filename)


@pytest.mark.asyncio
async def test_filings_list_of_file_download_async(mock_server_success):
    # given
    filename = "name.txt"
    server_port = mock_server_success.server_port

    def get_callback(resp):
        assert len(resp.errors) == 0

    # when
    list_of_file = ListOfFile()
    list_of_file.append(FilingsFile("name", f"http://127.0.0.1:{server_port}"))
    await list_of_file.download_async(callback=get_callback)

    # then
    assert os.path.exists(filename)

    with open(filename, "r") as f:
        content = f.read()
    assert content == "test text"

    os.remove(filename)


def test_filings_list_of_file_download_empty_files():
    # when
    list_of_file = ListOfFile()
    # then
    with pytest.raises(DownloadFileError) as err:
        list_of_file.download()
    assert err.value.message == "Cannot download any file. Files are empty."


@pytest.mark.asyncio
async def test_filings_list_of_file_download_async_empty_files():
    # given
    def get_callback(resp):
        assert resp.errors[0].message == "Cannot download any file. Files are empty."

    # when
    list_of_file = ListOfFile()

    # then
    response = await list_of_file.download_async(callback=get_callback)
    assert response.errors[0].message == "Cannot download any file. Files are empty."
