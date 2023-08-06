import json
from datetime import datetime

from refinitiv.data.content import news
from tests.unit.conftest import StubSession, StubResponse
from tests.unit.content.news.top_news.data_for_tests import top_news_headlines_df

with open("tests/unit/content/news/top_news/top-news.json", "r") as f:
    top_news_headline_response = json.loads(f.read())


def test_news_top_news_dataframe():
    session = StubSession(
        is_open=True, response=StubResponse(top_news_headline_response)
    )

    response = news.top_news.Definition("").get_data(session=session)
    assert response.data.df.to_string() == top_news_headlines_df


def test_top_news_datetime():
    session = StubSession(
        is_open=True, response=StubResponse(top_news_headline_response)
    )

    response = news.top_news.Definition("").get_data(session=session)
    assert isinstance(response.data.headlines[0].version_created, datetime)
    assert isinstance(response.data.headlines[0].first_created, datetime)
