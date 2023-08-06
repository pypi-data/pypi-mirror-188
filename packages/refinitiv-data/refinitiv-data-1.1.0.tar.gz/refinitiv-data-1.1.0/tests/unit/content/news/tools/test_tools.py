import pytest

from refinitiv.data.content.news._tools import (
    news_build_df_rdp,
    _get_text_from_story,
    _get_headline_from_story,
)


@pytest.mark.parametrize(
    ("input_data",),
    [
        (
            {
                "data": [
                    {
                        "storyId": "urn:newsml:reuters.com:20211229:nNDL1r6YQr:1",
                        "newsItem": {
                            "contentMeta": {
                                "infoSource": [
                                    {"_qcode": "NS:PUBT", "_role": "sRole:source"},
                                    {"_qcode": "NS:PUBT", "_role": "sRole:origProv"},
                                ],
                            },
                            "itemMeta": {
                                "firstCreated": {"$": "2021-12-29T12:15:06Z"},
                                "versionCreated": {"$": "2021-12-29T12:15:06Z"},
                                "title": [
                                    {
                                        "$": "HubSpot Inc. - 26 Companies With Really Catchy Slogans & Brand Taglines"
                                    }
                                ],
                            },
                        },
                    },
                    {
                        "storyId": "urn:newsml:reuters.com:20211229:nDjc3FXTxC:1",
                        "newsItem": {
                            "_version": 1,
                            "contentMeta": {
                                "infoSource": [
                                    {"_qcode": "NS:DJCP", "_role": "sRole:source"},
                                    {"_qcode": "NS:DJCP", "_role": "sRole:origProv"},
                                ],
                            },
                            "itemMeta": {
                                "firstCreated": {"$": "2021-12-29T00:00:00Z"},
                                "versionCreated": {"$": "2021-12-29T11:30:00Z"},
                                "title": [
                                    {
                                        "$": "The Public Safety Analytics Market is Expected to Witness a CAGR of Over 29.39% During the Forecast Period (2021 - 2026)"
                                    }
                                ],
                            },
                        },
                    },
                    {
                        "storyId": "urn:newsml:reuters.com:20211229:nDjc7scRMV:1",
                        "newsItem": {
                            "_version": 1,
                            "contentMeta": {
                                "infoSource": [
                                    {"_qcode": "NS:DJCP", "_role": "sRole:source"},
                                    {"_qcode": "NS:DJCP", "_role": "sRole:origProv"},
                                ],
                            },
                            "itemMeta": {
                                "firstCreated": {"$": "2021-12-29T00:00:00Z"},
                                "versionCreated": {"$": "2021-12-29T11:15:00Z"},
                                "title": [
                                    {
                                        "$": "Global Healthcare CRM Market 2021-2026: Key Players Include Accenture, Amdocs, Microsoft, Oracle, Salesforce and SAP"
                                    }
                                ],
                            },
                        },
                    },
                ],
            },
        )
    ],
)
def test_convert_content_data_to_df_rdp(input_data):
    # given
    # when
    result = news_build_df_rdp(input_data)
    # then
    assert not result.empty


@pytest.mark.parametrize(
    ("input_data",),
    [
        (
            {
                "data": [],
            },
        )
    ],
)
def test_convert_content_data_to_df_rdp_empty_df(input_data):
    # given
    # when
    result = news_build_df_rdp(input_data)
    # then
    assert result.empty


def test__get_text_from_story():
    # given
    expected_result = "expected_result"
    input_story = {"newsItem": {"contentSet": {"inlineData": [{"$": expected_result}]}}}

    # when
    result = _get_text_from_story(input_story)

    # then
    assert result == expected_result


def test__get_headline_from_story():
    # given
    expected_result = "expected_result"
    input_story = {"newsItem": {"contentMeta": {"headline": [{"$": expected_result}]}}}

    # when
    result = _get_headline_from_story(input_story)

    # then
    assert result == expected_result
