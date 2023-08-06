import allure
import pytest

from refinitiv.data.errors import RDError
from refinitiv.data.content import news
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.news.conftest import (
    check_news_headlines_date_for_datetime_type,
)
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
    get_async_response_from_definition,
    check_index_column_contains_dates,
)


@allure.suite("Content object - TopNews")
@allure.feature("Content object - TopNews")
@allure.severity(allure.severity_level.CRITICAL)
class TestTopNews:
    @allure.title("Create TopNews object with top_news_id and call get_data")
    @pytest.mark.caseid("C51290262")
    @pytest.mark.parametrize(
        "news_id,revision", [("urn:newsml:reuters.com:20020923:SPDOC_119827232002", 17)]
    )
    @pytest.mark.smoke
    def test_create_top_news_object_and_get_data(
        self, open_platform_session, news_id, revision
    ):
        response = news.top_news.Definition(
            top_news_id=news_id, revision_id=revision
        ).get_data()

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_index_column_contains_dates(response)
        check_news_headlines_date_for_datetime_type(response)

    @allure.title("Create TopNews object using closed session")
    @pytest.mark.caseid("C51290263")
    @pytest.mark.parametrize(
        "news_id", ["urn:newsml:reuters.com:20020923:SPDOC_119827232002"]
    )
    def test_create_top_news_object_when_session_is_not_opened(
        self, news_id, open_platform_session
    ):
        session = open_platform_session
        session.close()
        with pytest.raises(ValueError) as error:
            news.top_news.Definition(top_news_id=news_id).get_data()
        assert str(error.value) == "Session is not opened. Can't send any request"

    @allure.title("Create TopNews object and call get_data_async")
    @pytest.mark.caseid("C51290264")
    @pytest.mark.parametrize(
        "news_id", ["urn:newsml:reuters.com:20020923:SPDOC_119827232002"]
    )
    async def test_create_top_news_object_and_get_data_async(
        self, open_platform_session_async, news_id
    ):
        response = await get_async_response_from_definition(
            news.top_news.Definition(top_news_id=news_id)
        )
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)

    @allure.title("Create TopNews object with the invalid top_news_id")
    @pytest.mark.caseid("C51290265")
    @pytest.mark.parametrize("news_id", ["invalid"])
    def test_create_top_news_object_with_invalid_story_id(
        self, open_platform_session, news_id
    ):
        with pytest.raises(RDError) as error:
            news.top_news.Definition(top_news_id=news_id).get_data()
        assert (
            str(error.value)
            == f'Error code 400 | topNewsId "{news_id}" is malformatted.'
        )
