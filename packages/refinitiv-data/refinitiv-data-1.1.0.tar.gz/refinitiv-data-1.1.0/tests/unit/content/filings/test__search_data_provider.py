import pandas as pd
import pytest
from refinitiv.data.delivery._data._parsed_data import ParsedData

from refinitiv.data._content_type import ContentType
from refinitiv.data.content._df_builder_factory import get_dfbuilder
from refinitiv.data.content.filings._errors import DownloadFileError
from refinitiv.data.content.filings._search_data_provider import (
    FilingsSearchRequestFactory,
    FilingsSearchValidator,
    FilingsSearchFile,
    FilingsSearchData,
)


def test_filings_search_request_factory_get_body_parameters_query_override():
    # given
    data = {"query": "query", "variables": "variables"}

    # when
    body = FilingsSearchRequestFactory().get_body_parameters(**data)

    # then
    assert body.get("query") == "query"


def test_filings_search_data_df():
    # given
    raw_data = {
        "data": {
            "FinancialFiling": [
                {
                    "FilingDocument": {
                        "Identifiers": [{"Dcn": "dcn"}],
                        "DocId": "doc_id",
                        "FinancialFilingId": 1,
                        "DocumentSummary": {"DocumentTitle": "title"},
                        "FilesMetaData": [
                            {"FileName": "filename", "MimeType": "mimetype"}
                        ],
                    }
                }
            ]
        }
    }
    expected_raw_data = [["title", "filename", "mimetype", "dcn", "doc_id", 1]]
    columns = [
        "DocumentTitle",
        "Filename",
        "MimeType",
        "Dcn",
        "DocId",
        "FinancialFilingId",
    ]
    expected_df = pd.DataFrame(data=expected_raw_data, columns=columns)
    df_builder = get_dfbuilder(ContentType.FILINGS_SEARCH)

    # when
    data = FilingsSearchData(raw_data, use_field=False, dfbuilder=df_builder)
    df = data.df

    # then
    assert df.compare(expected_df).empty


def test_filing_file_download_none_error():
    # when
    f = FilingsSearchFile("name")

    # then
    with pytest.raises(DownloadFileError) as err:
        f.download()

    assert (
        err.value.message
        == "Cannot download file. Missing one of Filename, DCN, DocID and Filing ID"
    )


async def test_filing_file_download_async_none_error():
    # when
    f = FilingsSearchFile("name")

    # then
    response = await f.download_async()

    assert (
        response.errors[0].message
        == "Cannot download file. Missing one of Filename, DCN, DocID and Filing ID"
    )


def test_filing_content_data_has_errors():
    # given
    raw_data = {
        "errors": [
            {
                "message": "Validation error",
                "locations": [{"line": 1, "column": 4}],
                "extensions": {"classification": "ValidationError"},
            }
        ],
        "data": "None",
    }

    # when
    data = ParsedData(status=None, raw_response=raw_data, content_data=raw_data)

    # then
    assert not FilingsSearchValidator.content_data_has_no_errors(data)
