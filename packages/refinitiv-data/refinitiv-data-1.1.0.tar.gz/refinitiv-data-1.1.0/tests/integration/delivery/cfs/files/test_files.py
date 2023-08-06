import allure
import pytest

from refinitiv.data.delivery import cfs
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.delivery.cfs.conftest import (
    check_amount_of_objects_in_response_not_bigger_than,
)
from tests.integration.delivery.cfs.file_sets.conftest import (
    get_fileset_from_bucket_with_numfiles_bigger_than,
)
from tests.integration.delivery.cfs.files.conftest import (
    get_random_file_name_from_fileset,
    check_single_file_received,
    check_all_files_contain_fileset_id,
    check_file_name_in_response,
    check_files_in_response_created_after_date,
    check_files_in_response_modified_after_date,
    check_files_in_two_responses_are_not_the_same,
)
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    get_async_response_from_definition,
)


@allure.suite("Delivery object - CFS files")
@allure.feature("Delivery object - CFS files")
@allure.severity(allure.severity_level.CRITICAL)
class TestCfsFiles:
    @allure.title(
        "Get files with valid fileset id and default amount 25 - synchronously"
    )
    @pytest.mark.caseid("36823477")
    @pytest.mark.smoke
    def test_get_files_with_valid_fileset_id_synchronously(
        self, open_platform_session, get_random_fileset
    ):
        file_set = get_random_fileset
        response = cfs.files.Definition(file_set.id).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(25, response)

    @allure.title(
        "Get files with valid fileset id and default amount 25 - asynchronously"
    )
    @pytest.mark.caseid("36823478")
    async def test_get_files_with_valid_fileset_id_asynchronously(
        self, open_platform_session_async, get_random_fileset
    ):
        file_set = get_random_fileset

        response = await get_async_response_from_definition(
            cfs.files.Definition(file_set.id)
        )
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(25, response)

    @allure.title("Get files with invalid fileset id")
    @pytest.mark.caseid("36823479")
    def test_get_files_with_invalid_fileset_id(self, open_platform_session):
        with pytest.raises(RDError, match="Error code 404 | No resource found for:"):
            cfs.files.Definition("invalid fileset id").get_data()

    @allure.title("Get files with closed session")
    @pytest.mark.caseid("36823480")
    def test_get_files_with_closed_session(self, open_platform_session):
        session = open_platform_session
        session.close()
        files_definition = cfs.files.Definition("some id")
        with pytest.raises(
            ValueError, match="Session is not opened. Can't send any request"
        ):
            files_definition.get_data()

    @allure.title("Get files with valid file_name parameter")
    @pytest.mark.caseid("36823482")
    def test_get_files_with_valid_file_name_parameter(
        self, open_platform_session, get_random_fileset
    ):
        file_set = get_random_fileset
        file_name = get_random_file_name_from_fileset(file_set)
        response = cfs.files.Definition(file_set.id, file_name=file_name).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_single_file_received(response)
        check_all_files_contain_fileset_id(response, file_set.id)
        check_file_name_in_response(response, file_name)

    @allure.title("Get files with valid created_since param")
    @pytest.mark.parametrize("created_since", ["2021-06-25T14:00:00Z"])
    @pytest.mark.caseid("36823485")
    def test_get_files_with_valid_created_since_param(
        self, open_platform_session, get_random_fileset, created_since
    ):
        file_set = get_random_fileset
        response = cfs.files.Definition(
            file_set.id, created_since=created_since
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_files_in_response_created_after_date(response, created_since)

    @allure.title("Get files with valid modified_since param")
    @pytest.mark.parametrize("modified_since", ["2021-02-25T14:00:00Z"])
    @pytest.mark.caseid("36823486")
    def test_get_files_with_valid_modified_since_param(
        self, open_platform_session, get_random_fileset, modified_since
    ):
        file_set = get_random_fileset
        response = cfs.files.Definition(
            file_set.id, modified_since=modified_since
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_files_in_response_modified_after_date(response, modified_since)

    @allure.title("Get files with valid skip_token parameter")
    @pytest.mark.caseid("36823487")
    def test_get_files_with_valid_skip_token_param(self, open_platform_session):
        file_set = get_fileset_from_bucket_with_numfiles_bigger_than("bulk-ESG", 5)
        response1 = cfs.files.Definition(file_set.id, page_size=5).get_data()
        skip_token = response1.data.raw["skip_token"]
        response2 = cfs.files.Definition(file_set.id, skip_token=skip_token).get_data()
        check_response_status(response2, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response2)
        check_files_in_two_responses_are_not_the_same(response1, response2)

    @allure.title("Get files with valid page_size param")
    @pytest.mark.parametrize("page_size", [3])
    @pytest.mark.caseid("36823490")
    def test_get_files_with_valid_page_size_param(
        self, open_platform_session, page_size
    ):
        file_set = get_fileset_from_bucket_with_numfiles_bigger_than("bulk-ESG", 5)
        response = cfs.files.Definition(file_set.id, page_size=page_size).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        files_count = len(response.data.raw["value"])
        assert (
            files_count <= page_size
        ), f"Files count received {files_count} more than expected: {page_size}"
