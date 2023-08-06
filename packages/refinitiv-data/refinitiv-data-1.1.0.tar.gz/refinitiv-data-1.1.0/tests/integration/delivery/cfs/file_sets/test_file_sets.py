import allure
import pytest

import refinitiv.data as rd
from refinitiv.data.delivery import cfs
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.delivery.cfs.conftest import (
    check_amount_of_objects_in_response_not_bigger_than,
    check_no_objects_in_response,
)
from tests.integration.delivery.cfs.file_sets.conftest import (
    prepare_random_fileset_name,
    check_fileset_contains_all_attributes,
    prepare_random_package_id,
    check_fileset_contains_package_id,
    check_fileset_contains_status,
    check_filesets_in_response_available_after_date,
    check_filesets_in_response_available_before_date,
    check_filesets_in_response_have_content_from_param_after_date,
    check_filesets_in_response_have_content_to_param_before_date,
    check_filesets_in_response_created_after_date,
    check_filesets_in_response_modified_after_date,
    check_filesets_in_two_responses_are_not_the_same,
)
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    get_async_response_from_definition,
)


@allure.suite("Delivery object - CFS file-sets")
@allure.feature("Delivery object - CFS file-sets")
@allure.severity(allure.severity_level.CRITICAL)
class TestCfsFileSets:
    bucket_name = "bulk-ESG"

    @allure.title(
        "Get filesets with valid bucket name and default amount 25 - synchronously "
    )
    @pytest.mark.caseid("36652910")
    def test_get_filesets_with_valid_bucket_name_synchronously(
        self, open_platform_session
    ):
        response = cfs.file_sets.Definition(bucket=self.bucket_name).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(25, response)

    @allure.title(
        "Get filesets with valid bucket name and default amount 25 - asynchronously "
    )
    @pytest.mark.caseid("36652911")
    @pytest.mark.smoke
    async def test_get_filesets_with_valid_bucket_name_asynchronously(
        self, open_platform_session_async
    ):
        response = await get_async_response_from_definition(
            cfs.file_sets.Definition(bucket=self.bucket_name)
        )

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(25, response)

    @allure.title("Get filesets with valid bucket name and closed session")
    @pytest.mark.caseid("36652912")
    def test_get_filesets_with_closed_session(self):
        session = rd.session.desktop.Definition(app_key=" ").get_session()
        rd.session.set_default(session)
        file_sets_definition = cfs.file_sets.Definition(bucket=self.bucket_name)
        with pytest.raises(
            ValueError, match="Session is not opened. Can't send any request"
        ):
            file_sets_definition.get_data()

    @allure.title("Get filesets with valid name parameter")
    @pytest.mark.caseid("36652947")
    def test_get_filesets_with_valid_name_parameter(self, open_platform_session):
        name = prepare_random_fileset_name(self.bucket_name)
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name, name=name
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(1, response)

    @allure.title("Get filesets with non-existing bucket name")
    @pytest.mark.caseid("36652948")
    def test_get_filesets_with_non_existing_bucket_name(self, open_platform_session):
        with pytest.raises(RDError, match="Error code 404 | No resource found for:"):
            cfs.file_sets.Definition(bucket="non-existing bucket name").get_data()

    @allure.title(
        "Get filesets with non-existing name/list of attributes/package id/status"
    )
    @pytest.mark.caseid("36652946")
    @pytest.mark.parametrize(
        "name,attributes,package_id,status",
        [
            (
                "no name",
                {"non-existing-attribute": "some value"},
                "invalid id",
                "invalid status",
            )
        ],
    )
    def test_get_filesets_with_non_existing_params(
        self, open_platform_session, name, attributes, package_id, status
    ):
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name,
            name=name,
            attributes=attributes,
            package_id=package_id,
            status=status,
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_no_objects_in_response(response)

    @allure.title("Get filesets with list of attributes which exist in fileset")
    @pytest.mark.caseid("36652949")
    @pytest.mark.parametrize("attributes", [{"ContentType": "ESG Sources"}])
    def test_get_filesets_with_existing_attributes_param(
        self, open_platform_session, attributes
    ):
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name, attributes=attributes
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        for fileset in response.data.raw["value"]:
            check_fileset_contains_all_attributes(fileset, attributes)

    @allure.title("Get filesets with valid package_id parameter ")
    @pytest.mark.caseid("36652955")
    def test_get_filesets_with_valid_package_id_param(self, open_platform_session):
        package_id = prepare_random_package_id(self.bucket_name)
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name, package_id=package_id
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        for fileset in response.data.raw["value"]:
            check_fileset_contains_package_id(fileset, package_id)

    @allure.title("Get filesets with valid status parameter ")
    @pytest.mark.caseid("36652956")
    @pytest.mark.parametrize("status", ["READY"])
    def test_get_filesets_with_valid_status_param(self, open_platform_session, status):
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name, status=status
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        for fileset in response.data.raw["value"]:
            check_fileset_contains_status(fileset, status)

    @allure.title("Get filesets with available_from and available_to params")
    @pytest.mark.caseid("36652957")
    @pytest.mark.parametrize(
        "available_from,available_to",
        [("2020-10-23T00:00:00Z", "2022-10-23T00:00:00Z")],
    )
    def test_get_filesets_with_available_from_and_available_to_params(
        self, open_platform_session, available_from, available_to
    ):
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name,
            available_from=available_from,
            available_to=available_to,
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_filesets_in_response_available_after_date(response, available_from)
        check_filesets_in_response_available_before_date(response, available_to)

    @allure.title("Get filesets with content_from and content_to params ")
    @pytest.mark.caseid("36652959")
    @pytest.mark.parametrize(
        "content_from,content_to", [("2020-10-23T00:00:00Z", "2022-10-23T00:00:00Z")]
    )
    def test_get_filesets_with_content_from_and_content_to_params(
        self, open_platform_session, content_from, content_to
    ):
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name, content_from=content_from, content_to=content_to
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_filesets_in_response_have_content_from_param_after_date(
            response, content_from
        )
        check_filesets_in_response_have_content_to_param_before_date(
            response, content_to
        )

    @allure.title("Get filesets with created_since param")
    @pytest.mark.caseid("36652962")
    @pytest.mark.parametrize("created_since", ["2021-03-31T14:00:00Z"])
    def test_get_filesets_with_created_since_param(
        self, open_platform_session, created_since
    ):
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name, created_since=created_since
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_filesets_in_response_created_after_date(response, created_since)

    @allure.title("Get filesets with modified_since param")
    @pytest.mark.caseid("36652963")
    @pytest.mark.parametrize("modified_since", ["2021-07-06T14:00:00Z"])
    def test_get_filesets_with_modified_since_param(
        self, open_platform_session, modified_since
    ):
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name, modified_since=modified_since
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_filesets_in_response_modified_after_date(response, modified_since)

    @allure.title("Get filesets with valid skip_token parameter")
    @pytest.mark.caseid("36652964")
    def test_get_filesets_with_valid_skip_token_param(self, open_platform_session):
        response1 = cfs.file_sets.Definition(bucket=self.bucket_name, page_size=20).get_data()
        skip_token = response1.data.raw["skip_token"]
        response2 = cfs.file_sets.Definition(
            bucket=self.bucket_name, skip_token=skip_token
        ).get_data()
        check_response_status(response2, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response2)
        check_filesets_in_two_responses_are_not_the_same(response1, response2)

    @allure.title("Get filesets with valid page_size param")
    @pytest.mark.caseid("36652965")
    @pytest.mark.parametrize("page_size", [27, 100])
    def test_get_filesets_with_page_size_param(self, open_platform_session, page_size):
        response = cfs.file_sets.Definition(
            bucket=self.bucket_name, page_size=page_size
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        filesets_count = len(response.data.raw["value"])
        assert (
            filesets_count <= page_size
        ), f"Filesets count received {filesets_count} more than expected: {page_size}"
