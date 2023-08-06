import allure
import pytest

import refinitiv.data as rd
from refinitiv.data.delivery import cfs
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.delivery.cfs.buckets.conftest import (
    check_buckets_in_response_created_after_date,
    check_buckets_in_response_modified_after_date,
    check_buckets_in_response_available_before_date,
    check_buckets_in_response_available_after_date,
    check_all_buckets_contain_attributes,
    check_buckets_in_two_responses_are_not_the_same,
)
from tests.integration.delivery.cfs.conftest import (
    check_amount_of_objects_in_response_not_bigger_than,
    check_no_objects_in_response,
)
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    get_async_response_from_definition,
)


@allure.suite("Delivery object - CFS Buckets")
@allure.feature("Delivery object - CFS Buckets")
@allure.severity(allure.severity_level.CRITICAL)
class TestCfsBuckets:
    @allure.title("Get buckets with no params and default amount 25 - synchronously")
    @pytest.mark.caseid("36629292")
    @pytest.mark.smoke
    def test_get_buckets_with_no_params_synchronously(self, open_platform_session):
        response = cfs.buckets.Definition().get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(25, response)

    @allure.title("Get buckets with no params and default amount 25 - asynchronously")
    @pytest.mark.caseid("36629294")
    async def test_get_buckets_with_no_params_asynchronously(
        self, open_platform_session_async
    ):
        response = await get_async_response_from_definition(cfs.buckets.Definition())

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(25, response)

    @allure.title("Get buckets with closed session ")
    @pytest.mark.caseid("36629293")
    def test_get_buckets_with_closed_session(self):
        session = rd.session.desktop.Definition(app_key=" ").get_session()
        rd.session.set_default(session)
        buckets_definition = cfs.buckets.Definition()
        with pytest.raises(
            ValueError, match="Session is not opened. Can't send any request"
        ):
            buckets_definition.get_data()

    @allure.title("Get buckets with existing name param - partial match")
    @pytest.mark.caseid("C36629295")
    @pytest.mark.parametrize("name", ["cfs"])
    def test_get_buckets_with_existing_name_param(self, open_platform_session, name):
        response = cfs.buckets.Definition(name=name).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_amount_of_objects_in_response_not_bigger_than(25, response)

    @allure.title("Get buckets with non-existing name param")
    @pytest.mark.caseid("36629300")
    @pytest.mark.parametrize("name", ["Invalid_bucket_name"])
    def test_get_buckets_with_non_existing_name_param(
        self, open_platform_session, name
    ):
        response = cfs.buckets.Definition(name=name).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_no_objects_in_response(response)

    @allure.title("Get buckets with created_since param")
    @pytest.mark.caseid("36629552")
    @pytest.mark.parametrize("created_since", ["2020-10-23T00:00:00Z"])
    def test_get_buckets_with_created_since_param(
        self, open_platform_session, created_since
    ):
        response = cfs.buckets.Definition(created_since=created_since).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_buckets_in_response_created_after_date(created_since, response)

    @allure.title("Get buckets with modified_since param")
    @pytest.mark.caseid("36629552")
    @pytest.mark.parametrize("modified_since", ["2020-10-23T00:00:00Z"])
    def test_get_buckets_with_modified_since_param(
        self, open_platform_session, modified_since
    ):
        response = cfs.buckets.Definition(modified_since=modified_since).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_buckets_in_response_modified_after_date(modified_since, response)

    @allure.title("Get buckets with available_from param")
    @pytest.mark.caseid("36629591")
    @pytest.mark.parametrize("available_from", ["2020-10-23T00:00:00Z"])
    def test_get_buckets_with_available_from_param(
        self, open_platform_session, available_from
    ):
        response = cfs.buckets.Definition(available_from=available_from).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_buckets_in_response_available_before_date(available_from, response)

    @allure.title("Get buckets with available_to param")
    @pytest.mark.caseid("36629804")
    @pytest.mark.parametrize("available_to", ["2040-10-23T00:00:00Z"])
    def test_get_buckets_with_available_to_param(
        self, open_platform_session, available_to
    ):
        response = cfs.buckets.Definition(available_to=available_to).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_buckets_in_response_available_after_date(available_to, response)

    @pytest.mark.xfail(reason="https://jira.refinitiv.com/browse/EAPI-3100")
    @allure.title("Get buckets with list of attributes")
    @pytest.mark.parametrize(
        "attributes",
        [
            (["size", "depth", "purpose", "team"]),
            ("dayofweek"),
        ],
    )
    @pytest.mark.caseid("36629805")
    def test_get_buckets_with_list_of_attributes(
        self, open_platform_session, attributes
    ):
        response = cfs.buckets.Definition(attributes=attributes).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_all_buckets_contain_attributes(response, attributes)

    @allure.title("Get buckets with valid page_size param")
    @pytest.mark.caseid("36629806")
    @pytest.mark.parametrize("page_size", [26, 1000])
    def test_get_buckets_with_valid_page_size_param(
        self, open_platform_session, page_size
    ):
        response = cfs.buckets.Definition(page_size=page_size).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        buckets_count = len(response.data.raw["value"])
        assert (
            buckets_count <= page_size
        ), f"Buckets count received {buckets_count} more than expected: {page_size}"

    @allure.title("Get buckets with valid skip_token parameter")
    @pytest.mark.caseid("36629807")
    def test_get_buckets_with_valid_skip_token_param(self, open_platform_session):
        response1 = cfs.buckets.Definition().get_data()
        skip_token = response1.data.raw["skip_token"]
        response2 = cfs.buckets.Definition(skip_token=skip_token).get_data()
        check_response_status(response2, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response2)
        check_buckets_in_two_responses_are_not_the_same(response1, response2)
