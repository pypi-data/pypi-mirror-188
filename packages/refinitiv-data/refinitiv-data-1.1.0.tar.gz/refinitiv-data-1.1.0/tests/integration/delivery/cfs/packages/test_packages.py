import allure
import pytest

import refinitiv.data as rd
from refinitiv.data.delivery import cfs
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.delivery.cfs.conftest import (
    check_amount_of_objects_in_response_not_bigger_than,
)
from tests.integration.delivery.cfs.packages.conftest import (
    check_all_packages_names_contain_keyword,
    check_all_packages_types,
    check_bucket_name_in_all_packages,
    check_included_total_result_in_response,
    check_included_entitlement_result_in_response,
    check_packages_in_two_responses_are_not_the_same,
    check_packages_in_second_response_are_on_proper_position_in_first_response,
)
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    get_async_response_from_definition,
)


@allure.suite("Delivery object - CFS packages")
@allure.feature("Delivery object - CFS packages")
@allure.severity(allure.severity_level.CRITICAL)
class TestCfsPackages:
    @allure.title("Get packages with no params and default amount 25 - synchronously")
    @pytest.mark.caseid("36839411")
    @pytest.mark.smoke
    def test_get_packages_synchronously(self, open_platform_session):
        response = cfs.packages.Definition().get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(25, response)

    @allure.title("Get packages with no params and default amount 25 - synchronously")
    @pytest.mark.caseid("36839412")
    async def test_get_packages_asynchronously(self, open_platform_session_async):
        response = await get_async_response_from_definition(cfs.packages.Definition())

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(25, response)

    @allure.title("Get packages with closed session")
    @pytest.mark.caseid("36839413")
    def test_get_packages_with_closed_session(self):
        session = rd.session.desktop.Definition(app_key=" ").get_session()
        rd.session.set_default(session)
        packages_definition = cfs.packages.Definition()
        with pytest.raises(
            ValueError, match="Session is not opened. Can't send any request"
        ):
            packages_definition.get_data()

    @allure.title("Get packages with existing package_name param (full/partial match)")
    @pytest.mark.parametrize("package_name", ["cfs", "RDP Bulk CFS Package"])
    @pytest.mark.caseid("36839415")
    def test_get_packages_with_package_name_param(
        self, open_platform_session, package_name
    ):
        response = cfs.packages.Definition(package_name=package_name).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_all_packages_names_contain_keyword(response, package_name)

    @allure.title("Get packages with valid package_type param")
    @pytest.mark.parametrize("package_type", ["core"])
    @pytest.mark.caseid("36839422")
    def test_get_packages_with_package_type_param(
        self, open_platform_session, package_type
    ):
        response = cfs.packages.Definition(package_type=package_type).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_all_packages_types(response, package_type)

    @allure.title("Get packages with existing bucket_name param")
    @pytest.mark.parametrize("bucket_name", ["ESG"])
    @pytest.mark.caseid("36839584")
    def test_get_packages_with_bucket_name_param(
        self, open_platform_session, bucket_name
    ):
        response = cfs.packages.Definition(bucket_name=bucket_name).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_bucket_name_in_all_packages(response, bucket_name)

    @allure.title(
        "Get packages with included_total_result and included_entitlement_result params set to true"
    )
    @pytest.mark.caseid("36839589")
    def test_get_packages_with_included_total_result_and_included_entitlement_result_params(
        self, open_platform_session
    ):
        response = cfs.packages.Definition(
            included_total_result=True,
            included_entitlement_result=True,
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_included_total_result_in_response(response)
        check_included_entitlement_result_in_response(response)

    @allure.title(" Get packages with valid page_size param ")
    @pytest.mark.parametrize("page_size", [5])
    @pytest.mark.caseid("36839601")
    def test_get_packages_with_page_size_param(self, open_platform_session, page_size):
        response = cfs.packages.Definition(page_size=page_size).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(page_size, response)

    @allure.title("Get packages with valid skip_token parameter")
    @pytest.mark.caseid("36842315")
    def test_get_packages_with_skip_token_param(self, open_platform_session):
        response1 = cfs.packages.Definition().get_data()
        skip_token = response1.data.raw["skip_token"]
        response2 = cfs.packages.Definition(skip_token=skip_token).get_data()
        check_response_status(response2, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response2)
        check_packages_in_two_responses_are_not_the_same(response1, response2)

    @allure.title("Get packages with valid page param")
    @pytest.mark.parametrize("page_size,page", [(10, 2)])
    @pytest.mark.caseid("36839601")
    def test_get_packages_with_page_param(self, open_platform_session, page_size, page):
        response1 = cfs.packages.Definition(page_size=50).get_data()
        response2 = cfs.packages.Definition(page_size=page_size, page=page).get_data()
        check_packages_in_second_response_are_on_proper_position_in_first_response(
            response1, response2, page_size, page
        )
