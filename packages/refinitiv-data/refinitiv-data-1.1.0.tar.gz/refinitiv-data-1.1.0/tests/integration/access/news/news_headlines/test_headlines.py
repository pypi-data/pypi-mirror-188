from datetime import timedelta, datetime

import allure
import pytest

import refinitiv.data as rd
from refinitiv.data.content import news
from tests.integration.content.news.conftest import (
    check_data_in_response_sorted_by_order,
    check_dates_range_in_response,
)
from tests.integration.helpers import (
    check_index_column_contains_dates,
    check_dataframe_column_date_for_datetime_type,
    check_if_dataframe_is_not_none,
)


@allure.suite("FinCoder Layer")
@allure.feature("FinCoder - News Headlines")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("news")
class TestGetHeadlines:
    @allure.title("Get News Headlines with headline query")
    @pytest.mark.caseid("")
    @pytest.mark.parametrize(
        "query,default_count", [("(Britain and (Biden or Trump)) in 2022", 10)]
    )
    def test_get_news_headlines(self, open_session, query, default_count):
        response = rd.news.get_headlines(query=query)
        check_if_dataframe_is_not_none(response)
        check_index_column_contains_dates(response)
        check_dataframe_column_date_for_datetime_type(response)
        assert (
            response.shape[0] == default_count
        ), f"Actual Headlines amount is {response.shape[0]}"

    @allure.title("Get News Headlines with specified count param")
    @pytest.mark.caseid("")
    @pytest.mark.parametrize("sourceCode,count", [("NS:RTRS", 30)])
    def test_get_news_headlines_with_specified_count_param(
        self, open_session, sourceCode, count
    ):
        response = rd.news.get_headlines(query=sourceCode, count=count)
        check_if_dataframe_is_not_none(response)
        check_index_column_contains_dates(response)
        check_dataframe_column_date_for_datetime_type(response)
        assert response.shape[0] == count, f"Headlines amount is {response.shape[0]}"
        assert sourceCode in set(
            response.sourceCode.values
        ), "Inconsistency with result sourceCode"

    @allure.title("Get News Headlines with specified star and end parameters")
    @pytest.mark.caseid("")
    @pytest.mark.parametrize(
        "query,start,end,count",
        [
            (
                "P:4297144968",
                "2021-05-15T13:12:33.307Z",
                "2021-11-29T15:15:10.006Z",
                150,
            ),
            ("R:.FTSE", timedelta(hours=-10), timedelta(0), 5),
            ("Tesla", datetime(2022, 11, 10), datetime.now(), 100),
        ],
        ids=["string", "timedelta", "datetime"],
    )
    def test_get_news_headlines_with_specified_start_end_date(
        self,
        open_session,
        query,
        start,
        end,
        count,
    ):
        response = rd.news.get_headlines(query, start=start, end=end, count=count)

        check_if_dataframe_is_not_none(response)
        check_index_column_contains_dates(response)
        check_dataframe_column_date_for_datetime_type(response)
        check_dates_range_in_response(response, start, end)
        assert (
            response.shape[0] == count
        ), f"Actual Headlines amount is {response.shape[0]}"

    @allure.title("Get News Headlines with closed session")
    @pytest.mark.caseid("")
    @pytest.mark.parametrize("query", ["Microsoft"])
    def test_get_news_headlines_with_closed_session(self, query, open_session):
        session = open_session
        session.close()
        with pytest.raises(ValueError) as error:
            rd.news.get_headlines(query=query)
        assert str(error.value) == "Session is not opened. Can't send any request"

    @allure.title(
        "Get News headlines with specified sort_order param new-to-old/old-to-new "
    )
    @pytest.mark.caseid("")
    @pytest.mark.parametrize(
        "query,sort_order",
        [
            ("R:0#.FTSE", news.headlines.SortOrder.new_to_old),
            ("R:0#.FTSE", news.headlines.SortOrder.old_to_new),
        ],
    )
    def test_get_news_headlines_with_specified_sort_order_param(
        self, open_platform_session, query, sort_order
    ):
        response = rd.news.get_headlines(query=query, order_by=sort_order)
        check_if_dataframe_is_not_none(response)
        check_index_column_contains_dates(response)
        check_dataframe_column_date_for_datetime_type(response)
        check_data_in_response_sorted_by_order(response, sort_order)
