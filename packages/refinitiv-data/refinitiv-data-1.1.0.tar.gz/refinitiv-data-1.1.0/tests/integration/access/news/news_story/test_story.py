import allure
import pytest

import refinitiv.data as rd
from refinitiv.data._fin_coder_layer import Format
from refinitiv.data.errors import RDError
from tests.integration.access.news.conftest import check_story_response_format

ERROR_MESSAGE_PATTERN = {
    "PLATFORM": "Error code 404 | Error while calling the NEP backend: Story not found",
    "DESKTOP": "Error code 404 | Error while calling the NEP backend: Story not found",
}


@allure.suite("FinCoder Layer")
@allure.feature("FinCoder - News Story")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("news")
class TestGetStory:
    @allure.title("Get News Story with opened session and valid story ID")
    @pytest.mark.caseid("")
    @pytest.mark.parametrize(
        "response_format",
        [(Format.HTML), (Format.TEXT)],
    )
    def test_get_news_story_with_valid_story_id(self, open_session, response_format):
        story_keywords = ["NASA", "SpaceX", "mission"]

        def get_format(session, story_format):
            if session.type.name == "PLATFORM" and story_format == Format.HTML:
                return "Html"
            elif session.type.name == "DESKTOP" and story_format == Format.TEXT:
                return "Text"

        _format = get_format(open_session, response_format) or response_format
        response = rd.news.get_story(
            story_id="urn:newsml:reuters.com:20211125:nNRAhybonl:1",
            format=_format,
        )

        assert response, f"Response is empty - {response}"
        assert isinstance(response, str), f"Story has type {type(response)}"
        assert any(
            key in response for key in story_keywords
        ), "The unexpected story is responded"
        check_story_response_format(response, response_format)

    @allure.title("Get News Story using opened session with the invalid storyId ")
    @pytest.mark.caseid("")
    @pytest.mark.parametrize("id", ["invalid"])
    def test_get_news_story_with_invalid_story_id(self, open_session, id):
        underlying_mark = open_session.type.name
        expected_error_message = ERROR_MESSAGE_PATTERN[underlying_mark]
        with pytest.raises(RDError) as error:
            rd.news.get_story(id)
        assert str(error.value) == expected_error_message
