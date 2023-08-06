import allure
import pytest

from refinitiv.data.content import search
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.search.conftest import (
    check_document_title_contains_query,
    check_business_entity_for_every_document_in_response,
    check_navigator_entity_in_response,
    check_hits_and_dataframe_columns,
)
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    check_extended_params_were_sent_in_request,
    get_async_response_from_definitions,
)


@allure.suite("Content object - Search")
@allure.feature("Content object - Search")
@allure.severity(allure.severity_level.CRITICAL)
class TestSearch:
    @allure.title(
        "Create a Content object Search with query using a string and get data"
    )
    @pytest.mark.caseid("35382768")
    @pytest.mark.parametrize("query", ["Microsoft"])
    def test_create_content_object_search_with_query_using_string_and_get_data(
        self, open_session, query
    ):
        response = search.Definition(query).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_document_title_contains_query(response, query)

    @allure.title("Create a Content object Search when session is not opened")
    @pytest.mark.caseid("35384395")
    @pytest.mark.parametrize("query", ["Microsoft"])
    def test_create_content_object_search_when_session_is_not_opened(self, query):
        with pytest.raises(AttributeError) as error:
            search.Definition(query).get_data()
        assert str(error.value) == "No default session created yet. Please create a session first!"

    @allure.title("Create a Content object Search with query and optional parameters")
    @pytest.mark.caseid("35385811")
    @pytest.mark.parametrize("query", ["Tesla"])
    def test_create_content_object_search_with_query_and_optional_parameters(
        self, open_session, query
    ):
        response = search.Definition(query, view=search.Views.PEOPLE).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_business_entity_for_every_document_in_response(response, "PERSON")

    @allure.title("Create a Content object Search with invalid query")
    @pytest.mark.caseid("35385844")
    @pytest.mark.parametrize("query", [111])
    def test_create_content_object_search_with_invalid_query(self, open_session, query):
        with pytest.raises(RDError) as error:
            search.Definition(query).get_data()
        assert (
            str(error.value)
            == "Error code 400 | Validation error: json.Query in body must be of type string"
        )

    @allure.title(
        "Create a Content object Search with valid query and invalid optional parameters"
    )
    @pytest.mark.caseid("35385858")
    @pytest.mark.parametrize(
        "query,expected_error",
        [
            (
                "IBM",
                "Error code 400 | Validation error: json.View in body should be one of",
            )
        ],
    )
    def test_create_content_object_search_with_valid_query_and_invalid_optional_parameters(
        self, open_session, query, expected_error
    ):
        definition = search.Definition(query, view="invalid")
        with pytest.raises(RDError) as error:
            definition.get_data()
        assert expected_error in str(error.value)

    @allure.title("Extended params: override all fields")
    @pytest.mark.caseid("35513512")
    @pytest.mark.smoke
    @pytest.mark.parametrize("query,overridden_query", [("Microsoft", "Tesla")])
    def test_create_content_object_search_with_extended_params_overriding_all_fields(
        self, open_session, query, overridden_query
    ):
        extended_params = {"Query": overridden_query, "View": "Organisations"}
        response = search.Definition(
            query, view=search.Views.PEOPLE, extended_params=extended_params
        ).get_data()
        check_extended_params_were_sent_in_request(response, extended_params)
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_document_title_contains_query(response, overridden_query)

    @allure.title("Extended params: send additional fields")
    @pytest.mark.caseid("36105757")
    @pytest.mark.parametrize("query", ["IBM"])
    def test_create_content_object_search_with_extended_params_with_additional_fields(
        self, open_session, query
    ):
        extended_params = {
            "View": "Organisations",
            "INVALID_PARAM": "INVALID_PARAM_VALUE",
        }
        response = search.Definition(query, extended_params=extended_params).get_data()
        check_extended_params_were_sent_in_request(response, extended_params)
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)

    @allure.title(
        "Create a Content object Search with valid and invalid definition get data asynchronously"
    )
    @pytest.mark.caseid("35382768")
    @pytest.mark.parametrize(
        "query_1,query_2,order_by,select",
        [
            (
                "Oracle",
                "ceo",
                ["YearOfBirth desc,LastName,FirstName"],
                "YearOfBirth,DocumentTitle",
            )
        ],
    )
    async def test_create_content_object_search_with_query_using_string_and_get_data_asynchronously(
        self, open_session_async, query_1, query_2, order_by, select
    ):
        valid_response, invalid_response = await get_async_response_from_definitions(
            search.Definition(query=query_1),
            search.Definition(query=query_2, order_by=order_by, select=select),
        )

        check_response_status(valid_response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(valid_response)
        check_document_title_contains_query(valid_response, query_1)

        check_response_status(
            response=invalid_response,
            expected_status_code=HttpStatusCode.FOUR_HUNDRED,
            expected_http_reason=HttpReason.BAD_REQUEST,
            expected_error_message='Validation error: json.OrderBy in body must be of type string: "array"',
            expected_error_code=HttpStatusCode.FOUR_HUNDRED,
        )

    @allure.title("Create a Content object Search with navigators")
    @pytest.mark.caseid("C51600314")
    @pytest.mark.parametrize("navigator", [("Currency")])
    def test_create_content_object_search_with_navigators(
        self, open_session, navigator
    ):
        response = search.Definition(
            view=search.Views.GOV_CORP_INSTRUMENTS,
            top=0,
            navigators=f"{navigator}(buckets:10,desc:sum_FaceOutstandingUSD,calc:max_CouponRate)",
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_navigator_entity_in_response(
            response,
            navigator,
            navigator_props=["sum_FaceOutstandingUSD", "max_CouponRate"],
        )

        assert response.data.df.empty, f"Empty response.data.df received"
        assert len(response.data.hits) == 0

    @allure.title("Create a Content object Search with sub navigators")
    @pytest.mark.caseid("C51600315")
    @pytest.mark.parametrize(
        "hits_item_attributes,navigator_1,sub_navigator_1,navigator_2,sub_navigator_2",
        [
            (
                ["BusinessEntity", "DocumentTitle", "PI", "PermID", "RIC"],
                "MaturityDate",
                "BusinessEntity",
                "FirstName",
                "LastName",
            )
        ],
    )
    def test_create_content_object_search_with_sub_navigators(
        self,
        open_session,
        hits_item_attributes,
        navigator_1,
        sub_navigator_1,
        navigator_2,
        sub_navigator_2,
    ):
        response = search.Definition(
            view="GovCorpInstruments",
            filter="DbType eq 'CORP' and IsActive eq true and (MaturityDate ge 2020-01-01 and MaturityDate le 2025-12-31)",
            navigators=f"{navigator_1}(type:histogram, buckets:7, sub:{sub_navigator_1}(calc:sum_FaceOutstandingUSD)),"
            f"{navigator_2}(buckets:5,sub:{sub_navigator_2}(buckets:2))",
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_hits_and_dataframe_columns(response, hits_item_attributes)
        check_navigator_entity_in_response(response, navigator_1, sub_navigator_1)
        check_navigator_entity_in_response(response, navigator_2, sub_navigator_2)
