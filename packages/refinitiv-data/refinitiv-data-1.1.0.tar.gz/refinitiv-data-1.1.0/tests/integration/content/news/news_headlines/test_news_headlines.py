import allure
import pytest

from refinitiv.data.content import news
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.news.conftest import (
    check_every_story_title_contains_keyword,
    check_count_in_response_equal_to,
    check_data_in_response_sorted_by_order,
    check_dates_range_in_response,
    check_extended_params_were_sent_in_news_request, check_news_headlines_date_for_datetime_type,
)
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    get_async_response_from_definition,
    check_index_column_contains_dates,
)


@allure.suite("Content object - News Headlines")
@allure.feature("Content object - News Headlines")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("news")
class TestNewsHeadlines:
    @allure.title("Create News Headlines object with headline query and call get_data")
    @pytest.mark.caseid("34114877")
    @pytest.mark.parametrize("query", ["Google"])
    @pytest.mark.smoke
    def test_create_news_headlines_object_and_get_data(self, open_session, query):
        response = news.headlines.Definition(query).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_every_story_title_contains_keyword(response, query)
        check_news_headlines_date_for_datetime_type(response)

    @allure.title("Create News Headlines object using closed session")
    @pytest.mark.caseid("34114878")
    @pytest.mark.parametrize("query", ["Microsoft"])
    def test_create_content_object_search_when_session_is_not_opened(
        self, query, open_session
    ):
        session = open_session
        session.close()
        with pytest.raises(ValueError) as error:
            news.headlines.Definition(query).get_data()
        assert str(error.value) == "Session is not opened. Can't send any request"

    @allure.title("Create News headlines object with specified count param")
    @pytest.mark.caseid("34114877")
    @pytest.mark.parametrize("query,count,expected_raw_count", [("SpaceX", 150, 200)])
    def test_create_news_headlines_object_with_specified_count_param(
        self, open_session, query, count, expected_raw_count
    ):
        session = open_session
        session_type = session.type.name
        response = news.headlines.Definition(query, count=count).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_count_in_response_equal_to(
            count, response, session_type, expected_raw_count
        )

    @allure.title(
        "News headlines object with specified sort_order param new-to-old/old-to-new "
    )
    @pytest.mark.caseid("34114880")
    @pytest.mark.parametrize(
        "query,sort_order",
        [
            ("Tesla", news.headlines.SortOrder.new_to_old),
            ("Tesla", news.headlines.SortOrder.old_to_new),
        ],
    )
    def test_create_news_headlines_object_with_specified_sort_order_param(
        self, open_platform_session, query, sort_order
    ):
        response = news.headlines.Definition(query, sort_order=sort_order).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_data_in_response_sorted_by_order(response, sort_order)

    @allure.title(
        "News headlines object with specified date_from and date_to parameters"
    )
    @pytest.mark.caseid("34114882")
    @pytest.mark.parametrize(
        "query,date_from,date_to,count",
        [("Tesla", "2021-05-15T13:12:33.307Z", "2021-11-29T15:15:10.006Z", 115)],
    )
    def test_create_news_headlines_object_with_specified_date_from_and_date_to(
        self,
        open_session,
        query,
        date_from,
        date_to,
        count,
    ):
        response = news.headlines.Definition(
            query, date_from=date_from, date_to=date_to, count=count
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_dates_range_in_response(response, date_from, date_to)
        check_index_column_contains_dates(response)
        assert (
            response.data.df.index.size == count
        ), f"Actual DF size is {response.data.df.index.size}"

    @allure.title("News headlines object with specified extended_params")
    @pytest.mark.caseid("34114881")
    @pytest.mark.parametrize(
        "query,count,overridden_query,overridden_count",
        [("Microsoft", 5, "Google", "20")],
    )
    def test_create_news_headlines_object_with_specified_extended_params(
        self,
        open_session,
        query,
        count,
        overridden_query,
        overridden_count,
    ):
        extended_params = {"query": overridden_query, "number": overridden_count}
        response = news.headlines.Definition(
            query, count=count, extended_params=extended_params
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_extended_params_were_sent_in_news_request(response, extended_params)
        check_every_story_title_contains_keyword(response, overridden_query)

    @allure.title(
        "Create News Headlines object with headline query and call get_data_async "
    )
    @pytest.mark.caseid("35150253")
    @pytest.mark.parametrize("query", ["refinitiv"])
    async def test_create_news_headlines_object_and_get_data_async(
        self, open_session_async, query
    ):
        response = await get_async_response_from_definition(
            news.headlines.Definition(query)
        )
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_every_story_title_contains_keyword(response, query)

    @allure.title("Create News Headlines object using closed session (asynchronously)")
    @pytest.mark.caseid("35150254")
    @pytest.mark.parametrize("query", ["Microsoft"])
    async def test_create_news_headlines_object_when_session_is_not_opened_async(
        self, query, open_session_async
    ):
        session = open_session_async
        await session.close_async()
        news_definition = news.headlines.Definition(query)
        with pytest.raises(ValueError) as error:
            await get_async_response_from_definition(news_definition)
        assert str(error.value) == "Session is not opened. Can't send any request"
