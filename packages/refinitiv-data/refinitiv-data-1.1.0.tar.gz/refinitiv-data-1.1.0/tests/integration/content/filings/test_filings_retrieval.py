import allure
import pytest

from refinitiv.data.content import filings
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


@allure.suite("Filings Retrieval")
@allure.feature("Filings Retrieval")
@allure.severity(allure.severity_level.CRITICAL)
class TestFilingsRetrieval:
    @allure.title("Create filings retrieval definition with valid params and get data")
    @pytest.mark.parametrize(
        "filename,dcn,doc_id,filing_id,expected_titles",
        [
            (
                "ecpfilings_34359955599_pdf",
                None,
                None,
                None,
                ["Filename", "SignedURL", "MimeType"],
            ),
            (None, "cr00329072", None, None, ["Filename", "SignedURL", "MimeType"]),
            (None, None, "49612437", None, ["Filename", "SignedURL", "MimeType"]),
            (None, None, None, "34359955599", ["Filename", "SignedURL", "MimeType"]),
        ],
    )
    @pytest.mark.caseid("C43473347")
    @pytest.mark.smoke
    def test_create_filings_retrieval_definition_with_valid_params_and_get_data(
        self, filename, dcn, doc_id, filing_id, expected_titles, open_platform_session
    ):
        response = filings.retrieval.Definition(
            filename=filename, dcn=dcn, doc_id=doc_id, filing_id=filing_id
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_dataframe_contains_columns_names(response, expected_titles)
        check_non_empty_response_data(response)

    @allure.title("Create filings retrieval definition and download file")
    @pytest.mark.parametrize(
        "filename",
        [
            "ecpfilings_34359955599_pdf",
        ],
    )
    @pytest.mark.caseid("C43473348")
    @pytest.mark.smoke
    def test_create_filings_retrieval_definition_and_download_file(
        self, filename, open_platform_session
    ):
        response = filings.retrieval.Definition(filename=filename).get_data()

        file = response.data.files
        file_download_response = file[0].download(path="./")
        expected_file_name = response.data.df["Filename"][0]

        check_file_downloaded_response(file_download_response, expected_file_name)
        check_file_is_downloaded(expected_file_name)

    @allure.title("Create filings retrieval definition and download all files")
    @pytest.mark.parametrize(
        "doc_id",
        [
            "49612437",
        ],
    )
    @pytest.mark.caseid("C43473350")
    @pytest.mark.smoke
    def test_create_filings_retrieval_definition_and_download_all_files(
        self, doc_id, open_platform_session
    ):
        response = filings.retrieval.Definition(doc_id=doc_id).get_data()

        files = response.data.files
        files.download()

        expected_file_name = response.data.df["Filename"].values
        for filename in expected_file_name:
            check_file_is_downloaded(filename)

    @allure.title("Create filings retrieval definition with more than one parameter")
    @pytest.mark.parametrize(
        "doc_id,filename",
        [("49612437", "file")],
    )
    @pytest.mark.caseid("C43473351")
    @pytest.mark.smoke
    def test_create_filings_retrieval_definition_with_more_than_one_parameter(
        self, doc_id, filename, open_platform_session
    ):
        with pytest.raises(ValueError) as error:
            filings.retrieval.Definition(doc_id=doc_id, filename=filename).get_data()

        assert (
            str(error.value)
            == "Only one of filename, dcn, doc_id or filing_id, can be used in a Definition"
        )

    @allure.title(
        "Create filings retrieval definition and download all files asynchronously"
    )
    @pytest.mark.parametrize(
        "doc_id,expected_titles",
        [("49612437", ["Filename", "SignedURL", "MimeType"])],
    )
    @pytest.mark.caseid("C43473352")
    @pytest.mark.smoke
    async def test_create_filings_retrieval_definition_and_download_all_files_asynchronously(
        self, doc_id, expected_titles, open_platform_session_async
    ):
        response = await get_async_response_from_definition(
            filings.retrieval.Definition(doc_id=doc_id)
        )

        files = response.data.files
        await files.download_async(callback=get_callback)

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_response_dataframe_contains_columns_names(response, expected_titles)
        expected_file_name = response.data.df["Filename"].values
        for filename in expected_file_name:
            check_file_is_downloaded(filename)
