from unittest.mock import Mock

import pytest
import refinitiv.data as rd

from tests.unit.conftest import StubSession, StubResponse


def test_import():
    try:
        from refinitiv.data.content.news import headlines
    except ImportError as e:
        assert False, str(e)


def test_attributes():
    from refinitiv.data.content.news import headlines

    assert hasattr(headlines, "Definition")


def test_get_data_called__check_response():
    from refinitiv.data.content.news import headlines

    # given
    response = StubResponse({"data": {}, "headlines": []})
    session = StubSession(is_open=True, response=response)

    definition_layer = headlines.Definition(...)
    definition_layer._check_response = Mock()

    # when
    definition_layer.get_data(session)

    # then
    definition_layer._check_response.assert_called_once()


@pytest.mark.parametrize(
    "news_definition, expected_repr",
    [
        (
            rd.content.news.headlines.Definition("Apple"),
            "<refinitiv.data.content.news.headlines.Definition object at {0} {{query='Apple'}}>",
        ),
        (
            rd.content.news.story.Definition(
                "urn:newsml:reuters.com:20201026:nPt6BSyBh"
            ),
            "<refinitiv.data.content.news.story.Definition object at {0} {{story_id='urn:newsml:reuters.com:20201026:nPt6BSyBh'}}>",
        ),
    ],
)
def test_esg_content_repr(news_definition, expected_repr):
    # given
    obj_id = hex(id(news_definition))

    # when
    s = repr(news_definition)

    # then
    assert s == expected_repr.format(obj_id), s
