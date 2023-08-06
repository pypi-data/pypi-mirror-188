import allure
import pytest

from refinitiv.data.content import news
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.news.conftest import (
    check_story_title,
)
from tests.integration.helpers import (
    check_response_status,
    get_async_response_from_definition,
)

ERROR_MESSAGE_PATTERN = {
    "PLATFORM": "Error code 404 | Error while calling the NEP backend: Story not found",
    "DESKTOP": "Error code 404 | Error while calling the NEP backend: Story not found",
}


@allure.suite("Content object - News Story")
@allure.feature("Content object - News Story")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("news")
class TestNewsStory:
    @allure.title("Create News Story object with opened session and valid story ID")
    @pytest.mark.caseid("34114894")
    @pytest.mark.parametrize(
        "id,story_title",
        [
            (
                "urn:newsml:reuters.com:20171030:nTOPMTL:169",
                "*TOP NEWS* Metals",
            )
        ],
    )
    @pytest.mark.smoke
    def test_create_news_story_object_with_valid_story_id_and_get_data(
        self, open_session, id, story_title
    ):
        response = news.story.Definition(id).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_story_title(response, story_title)

    @allure.title(
        "Create News Story object with opened session and valid story ID - asynchronously"
    )
    @pytest.mark.caseid("34114895")
    @pytest.mark.parametrize(
        "id,story_title",
        [
            (
                "urn:newsml:reuters.com:20171030:nTOPMTL:169",
                "*TOP NEWS* Metals",
            )
        ],
    )
    async def test_create_news_story_object_with_valid_story_id_and_get_data_async(
        self, open_session_async, id, story_title
    ):
        response = await get_async_response_from_definition(news.story.Definition(id))
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_story_title(response, story_title)

    @allure.title(
        "Create News Story object using opened session with the invalid storyId "
    )
    @pytest.mark.caseid("34114895")
    @pytest.mark.parametrize("id", ["invalid"])
    def test_create_news_story_object_with_invalid_story_id(self, open_session, id):
        underlying_mark = open_session.type.name
        expected_error_message = ERROR_MESSAGE_PATTERN[underlying_mark]
        with pytest.raises(RDError) as error:
            news.story.Definition(id).get_data()
        assert str(error.value) == expected_error_message

    @allure.title("Create News Story object with closed session and check error")
    @pytest.mark.caseid("34114897")
    @pytest.mark.parametrize("id", ["urn:newsml:reuters.com:20201026:nPt6BSyBh"])
    async def test_create_news_story_object_with_closed_session(self, open_session_async, id):
        session = open_session_async
        await session.close_async()
        news_definition = news.story.Definition(id)
        with pytest.raises(ValueError) as error:
            await get_async_response_from_definition(news_definition)
        assert str(error.value) == "Session is not opened. Can't send any request"
