import pytest

from refinitiv.data.content.news import Urgency
from refinitiv.data.content.news._data_classes import HeadlineRDP, Story
from refinitiv.data.content.news._news_data_provider import (
    NewsStoryRDPData,
    NewsStoryUDFData,
)

HEADLINE_RAW_JSON = {
    "storyId": "urn:newsml:reuters.com:20210713:nBw2Wmkgya:1",
    "newsItem": {
        "_version": 1,
        "contentMeta": {
            "audience": [{"_qcode": "NP:BSW"}, {"_qcode": "NP:CNR"}],
            "creator": [{"_qcode": "NS:BSW", "_role": "sRole:source"}],
            "infoSource": [
                {"_qcode": "NS:BSW", "_role": "sRole:source"},
                {"_qcode": "NS:BSW", "_role": "sRole:origProv"},
            ],
            "language": [{"_tag": "en"}],
            "subject": [
                {"_qcode": "B:255"},
                {"_qcode": "M:27I"},
                {"_qcode": "B:198"},
                {"_qcode": "G:4"},
                {"_qcode": "M:1WK"},
                {"_qcode": "B:162"},
                {"_qcode": "B:279"},
                {"_qcode": "M:1TG"},
                {"_qcode": "B:69"},
                {"_qcode": "M:Z"},
                {"_qcode": "B:291"},
                {"_qcode": "G:9"},
                {"_qcode": "M:E7"},
                {"_qcode": "M:2CQ"},
                {"_qcode": "B:278"},
                {"_qcode": "M:1WJ"},
                {"_qcode": "M:1TH"},
                {"_qcode": "M:1WN"},
                {"_qcode": "B:161"},
                {"_qcode": "B:282"},
                {"_qcode": "E:1"},
                {"_qcode": "M:2CX"},
                {"_qcode": "M:1T4"},
                {"_qcode": "G:6J"},
                {"_qcode": "M:2CP"},
                {"_qcode": "M:2D1"},
                {"_qcode": "M:2CS"},
                {"_qcode": "M:NL"},
                {"_qcode": "R:GOOGL.O"},
                {"_qcode": "B:285"},
                {"_qcode": "M:23G"},
                {"_qcode": "B:172"},
                {"_qcode": "M:1ZD"},
                {"_qcode": "B:257"},
                {"_qcode": "M:32"},
                {"_qcode": "B:75"},
                {"_qcode": "B:87"},
                {"_qcode": "G:50"},
                {"_qcode": "M:V"},
                {"_qcode": "B:256"},
                {"_qcode": "M:1QD"},
                {"_qcode": "M:2CR"},
                {"_qcode": "M:1WL"},
                {"_qcode": "B:173"},
                {"_qcode": "M:1ZN"},
                {"_qcode": "R:005930.KS"},
                {"_qcode": "B:86"},
                {"_qcode": "M:1P2"},
                {"_qcode": "E:6Q"},
                {"_qcode": "E:40"},
                {"_qcode": "B:78"},
                {"_qcode": "B:290"},
                {"_qcode": "B:1805"},
                {"_qcode": "M:2CN"},
                {"_qcode": "P:4295882451"},
                {"_qcode": "P:5046736305"},
                {"_qcode": "P:5030853586"},
                {"_qcode": "P:4298538029"},
                {"_qcode": "P:4295899948"},
            ],
            "urgency": {"$": 3},
        },
        "itemMeta": {
            "firstCreated": {"$": "2021-07-13T14:00:00.749Z"},
            "versionCreated": {"$": "2021-07-13T14:00:00.749Z"},
            "title": [
                {
                    "$": "Backtracks Releases New Integration with Google "
                    "Cloud for Podcast Audience and Engagement Data"
                }
            ],
        },
    },
}

STORY_RAW_JSON = {
    "newsItem": {
        "contentMeta": {
            "urgency": {"$": 3},
            "subject": [
                {
                    "_confidence": 100,
                    "_creator": "rftResRef:sys26",
                    "_how": "howextr:tool",
                    "_id": "S1",
                    "_qcode": "B:161",
                    "_why": "why:inferred",
                    "related": [
                        {
                            "_creator": "rftResRef:sys24",
                            "_how": "howextr:tool",
                            "_id": "grp0",
                            "_qcode": "hmlInd:high",
                            "_rel": "extCptRel:hasRelevanceGroup",
                            "_why": "why:inferred",
                        }
                    ],
                }
            ],
            "creator": [{"_qcode": "mocked_qcode"}],
            "infoSource": "mocked_infoSource",
            "language": "mocked_language",
        },
        "itemMeta": {
            "versionCreated": {"$": "2021-05-24T04:13:02Z"},
            "firstCreated": {"$": "2021-05-24T04:13:02Z"},
            "title": [{"$": "mocked_title"}],
        },
    }
}


@pytest.mark.parametrize("news_story_class", [NewsStoryRDPData, NewsStoryUDFData])
def test_story_response(news_story_class):
    raw_json = {"mocked": "json"}
    result = news_story_class(raw_json)

    assert result.raw == raw_json


def test_headlines_create_values():
    headline = HeadlineRDP.from_dict(HEADLINE_RAW_JSON)
    assert headline.creator == "NS:BSW"
    assert headline.language == [{"_tag": "en"}]
    assert headline.source == [
        {"_qcode": "NS:BSW", "_role": "sRole:source"},
        {"_qcode": "NS:BSW", "_role": "sRole:origProv"},
    ]
    assert headline.story_id == "urn:newsml:reuters.com:20210713:nBw2Wmkgya:1"
    assert (
        headline.title == "Backtracks Releases New Integration with Google"
        " Cloud for Podcast Audience and Engagement Data"
    )
    assert headline.urgency == Urgency.Regular


def test_story_create_values():
    story = Story.from_dict(STORY_RAW_JSON)
    assert story.creator == "mocked_qcode"
    assert story.item_codes == ["B:161"]
    assert story.language == "mocked_language"
    assert story.source == "mocked_infoSource"
    assert story.title == "mocked_title"
    assert story.urgency == Urgency.Regular
