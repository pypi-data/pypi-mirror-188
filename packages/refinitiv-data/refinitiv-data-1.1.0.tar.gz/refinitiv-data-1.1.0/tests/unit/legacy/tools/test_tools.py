import pytest
import pandas as pd

from refinitiv.data.eikon._tools import convert_content_data_to_df_udf


@pytest.mark.parametrize(
    ("input_data",),
    [
        (
            {
                "headlines": [
                    {
                        "firstCreated": "2021-12-29T07:00:44.686Z",
                        "sourceCode": "NS:PRN",
                        "storyId": "urn:newsml:reuters.com:20211229:nPRrSFC87a:1",
                        "text": None,
                        "versionCreated": "2021-12-29T07:00:44.686Z",
                    },
                    {
                        "firstCreated": "2021-12-29T02:27:55.372Z",
                        "sourceCode": "NS:ECLCTA",
                        "storyId": "urn:newsml:reuters.com:20211229:nNRAiknlz9:1",
                        "text": "",
                        "versionCreated": "2021-12-29T02:27:55.372Z",
                    },
                    {
                        "firstCreated": "2021-12-29T02:27:08.256Z",
                        "sourceCode": "NS:ECLCTA",
                        "storyId": "urn:newsml:reuters.com:20211229:nNRAiknks9:1",
                        "text": "Ibm Maintenance And Support Renewal",
                        "versionCreated": "2021-12-29T02:27:08.256Z",
                    },
                ],
            },
        )
    ],
)
def test_convert_content_data_to_df_udf(input_data):
    result = convert_content_data_to_df_udf(input_data)
    assert not result.empty

    for row in result.itertuples():
        if row.storyId == "urn:newsml:reuters.com:20211229:nPRrSFC87a:1":
            assert row.text is pd.NA
        if row.storyId == "urn:newsml:reuters.com:20211229:nNRAiknlz9:1":
            assert row.text == ""
        if row.storyId == "urn:newsml:reuters.com:20211229:nNRAiknks9:1":
            assert row.text == "Ibm Maintenance And Support Renewal"


@pytest.mark.parametrize(
    ("input_data",),
    [
        (
            {
                "headlines": [],
            },
        )
    ],
)
def test_convert_content_data_to_df_udf_empty_df(input_data):
    # given
    # when
    result = convert_content_data_to_df_udf(input_data)
    # then
    assert result.empty


def test_convert_content_data_to_df_udf_convert_data_types():
    pass
