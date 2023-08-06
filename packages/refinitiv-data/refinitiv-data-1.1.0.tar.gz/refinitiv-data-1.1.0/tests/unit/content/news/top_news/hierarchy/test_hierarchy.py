import json

from refinitiv.data.content import news
from tests.unit.conftest import StubSession, StubResponse
from tests.unit.content.news.top_news.hierarchy.data_for_tests import (
    top_news_hierarchy_df,
)

with open(
    "tests/unit/content/news/top_news/hierarchy/top-news-hierarchy.json", "r"
) as f:
    top_news_response = json.loads(f.read())


def test_top_news_hierarchy_dataframe():
    session = StubSession(is_open=True, response=StubResponse(top_news_response))

    response = news.top_news.hierarchy.Definition().get_data(session=session)

    assert response.data.df.to_string() == top_news_hierarchy_df
    assert response.data.hierarchy
