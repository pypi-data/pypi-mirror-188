import allure
import pytest

from refinitiv.data.content.filings import search
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.filings.conftest import (
    check_file_downloaded_response,
    check_file_is_downloaded,
    get_callback,
)
from tests.integration.helpers import (
    get_async_response_from_definition,
    check_response_status,
    check_non_empty_response_data,
    check_response_dataframe_contains_columns_names,
)

query = (
    '{  FinancialFiling(filter: {AND: [{FilingDocument: {DocumentSummary: {FeedName: {EQ: "Edgar"}}}}, '
    '{FilingDocument: {DocumentSummary: {FormType: {EQ: "10-Q"}}}}, {FilingDocument: {DocumentSummary: {'
    'FilingDate: {BETWN: {FROM: "2020-10-01T00:00:00Z", TO: "2020-12-31T00:00:00Z"}}}}}]}, sort: {FilingDocument: '
    "{DocumentSummary: {FilingDate: DESC}}}, limit: 3) {    _metadata {      totalCount    }    FilingDocument { "
    "     Identifiers {        Dcn      }      DocId      FinancialFilingId      DocumentSummary {        "
    "DocumentTitle        FeedName        FormType        HighLevelCategory        MidLevelCategory        "
    "FilingDate        SecAccessionNumber        SizeInBytes          }  FilesMetaData {        FileName        "
    "MimeType      }    }  }} "
)


@allure.suite("Filings Search")
@allure.feature("Filings Search")
@allure.severity(allure.severity_level.CRITICAL)
class TestFilingsSearch:
    @allure.title("Create filings search definition with valid params and get data")
    @pytest.mark.parametrize(
        "expected_titles",
        [
            [
                "DocumentTitle",
                "Filename",
                "MimeType",
                "Dcn",
                "DocId",
                "FinancialFilingId",
            ],
        ],
    )
    @pytest.mark.caseid("C50564778")
    @pytest.mark.smoke
    def test_create_filings_search_definition_with_valid_params_and_get_data(
        self, open_platform_session, expected_titles
    ):
        response = search.Definition(query).get_data()

        file = response.data.files
        file_download_response = file[0].download(path="./")
        expected_file_name = response.data.df["Filename"][0]

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_dataframe_contains_columns_names(response, expected_titles)
        check_non_empty_response_data(response)

        check_file_downloaded_response(file_download_response, expected_file_name)
        check_file_is_downloaded(expected_file_name)

    @allure.title("Create filings search definition and download all files")
    @pytest.mark.caseid("C50564779")
    @pytest.mark.smoke
    def test_create_filings_search_definition_and_download_all_files(
        self, open_platform_session
    ):
        response = search.Definition(query).get_data()

        files = response.data.files
        files.download()

        expected_file_name = response.data.df["Filename"].values
        for filename in expected_file_name:
            check_file_is_downloaded(filename)

    @allure.title(
        "Create filings sync search definition and download all files asynchronously"
    )
    @pytest.mark.parametrize(
        "expected_titles",
        [
            [
                "DocumentTitle",
                "Filename",
                "MimeType",
                "Dcn",
                "DocId",
                "FinancialFilingId",
            ]
        ],
    )
    @pytest.mark.caseid("C50564780")
    @pytest.mark.smoke
    async def test_create_filings_sync_search_definition_and_download_all_files_asynchronously(
            self, expected_titles, open_platform_session_async
    ):
        response = await get_async_response_from_definition(search.Definition(query))

        files = response.data.files
        await files.download_async(callback=get_callback)

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_dataframe_contains_columns_names(response, expected_titles)
        expected_file_name = response.data.df["Filename"].values
        for filename in expected_file_name:
            check_file_is_downloaded(filename)

    @allure.title(
        "Create sync filings search definition and download first file asynchronously"
    )
    @pytest.mark.parametrize(
        "expected_titles",
        [
            [
                "DocumentTitle",
                "Filename",
                "MimeType",
                "Dcn",
                "DocId",
                "FinancialFilingId",
            ]
        ],
    )
    @pytest.mark.caseid("C50645502")
    @pytest.mark.smoke
    async def test_create_filings_search_definition_and_download_first_files_asynchronously(
        self, expected_titles, open_platform_session_async
    ):
        response = search.Definition(query).get_data()

        files = response.data.files
        await files[0].download_async(callback=get_callback)

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_dataframe_contains_columns_names(response, expected_titles)
        expected_file_name = response.data.df["Filename"].values
        for filename in expected_file_name:
            check_file_is_downloaded(filename)