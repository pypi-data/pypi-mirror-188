import json
import os
import shutil

import numpy as np
import pandas as pd

from refinitiv.data._tools import to_datetime
from refinitiv.data.content.news.headlines import SortOrder
from tests.integration.helpers import check_if_dataframe_is_not_none


def check_extended_params_were_sent_in_news_request(response, expected_extended_params):
    params_sent_in_request = None
    if response.request_message.method == "GET":  # rdp
        params_sent_in_request = response.request_message.url.params._dict
    elif response.request_message.method == "POST":  # udf
        content = json.loads(response.request_message.content.decode("utf-8"))
        params_sent_in_request = content["Entity"]["W"]
    for key in expected_extended_params.keys():
        try:
            assert expected_extended_params[key] in params_sent_in_request[key]
        except KeyError:
            raise AssertionError(
                f"Key '{key}' not found in params sent in request: {params_sent_in_request}"
            )


def check_story_title(response, story_title):
    assert (
        response.data.story.title == story_title
    ), f"The story with unexpected title received: {response.data.story.title}"


def check_every_story_title_contains_keyword(response, keyword):
    if response.request_message.method == "GET":  # rdp
        for story in response.data.raw["data"]:
            title = story["newsItem"]["itemMeta"]["title"][0]["$"]
            assert (
                keyword.lower() in title.lower()
            ), f"Keyword {keyword} is not included into title {title}"
    elif response.request_message.method == "POST":  # udf
        dataframe = response.data.df
        check_if_dataframe_is_not_none(dataframe)


def check_count_in_response_equal_to(count, response, session_type, expected_raw_count):
    headlines_sum = 0
    if session_type == "PLATFORM":  # rdp
        assert (
            len(response.data.headlines) == count
        ), f"Number of headlines in response is {len(response.data['headlines'])}, but expected {count}"
    elif session_type == "DESKTOP":  # udf
        for page in response.data.raw:
            headlines_sum += len(page["headlines"])
        assert (
            headlines_sum == expected_raw_count
        ), f"Count property in response {headlines_sum} differs from expected {expected_raw_count}"
        assert (
            len(response.data.headlines) == count
        ), f"Number of headlines in response is {len(response.data.headlines)}, but expected {count}"


def retrieve_dates_from_headlines_response(response):
    dataframe = response
    if not isinstance(response, pd.DataFrame):
        dataframe = response.data.df

    return [to_datetime(date) for date in dataframe.index.array]


def check_data_in_response_sorted_by_order(response, order):
    dates = retrieve_dates_from_headlines_response(response)

    if order == SortOrder.new_to_old:
        sorted_dates_descending = sorted(dates, reverse=True)
        assert (
            dates == sorted_dates_descending
        ), f"Retrieved dates from headlines are not sorted from new to old: {dates}"
    elif order == SortOrder.old_to_new:
        sorted_dates_ascending = sorted(dates, reverse=False)
        assert (
            dates == sorted_dates_ascending
        ), f"Retrieved dates from headlines are not sorted from old to new: {dates}"


def check_list_of_dates_are_in_interval(list_of_dates, date_from, date_to):
    date_to = to_datetime(date_to)
    date_from = to_datetime(date_from)

    for date in list_of_dates:
        assert (
            date.timestamp() >= date_from.timestamp()
        ), f"Found the date {date} which is  earlier than {date_from}"
        assert (
            date.timestamp() <= date_to.timestamp()
        ), f"Found the date {date} which is  later  than expected date_to {date_to}"


def check_dates_range_in_response(response, date_from, date_to):
    dates = retrieve_dates_from_headlines_response(response)
    check_list_of_dates_are_in_interval(dates, date_from, date_to)


def check_file_is_saved(filename: str, path: str = None):
    file_path = "./"
    if path:
        file_path=path
    list_of_files = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            list_of_files.append(file)

    assert filename in list_of_files, f"File {filename} not found"

    # removing a saved file after test
    if path:
        shutil.rmtree(path, ignore_errors=True)
    else:
        os.remove(filename)

def check_news_headlines_date_for_datetime_type(response):
    random_headline = response.data.headlines[0]
    check_if_news_headline_date_is_datetime64(random_headline)
    if hasattr(random_headline, "related_headlines"):
        random_headline = random_headline.related_headlines[0]
        check_if_news_headline_date_is_datetime64(random_headline)


def check_if_news_headline_date_is_datetime64(headline):
    if headline.first_created:
        assert isinstance(headline.first_created.asm8, np.datetime64)
    if headline.version_created:
        assert isinstance(headline.version_created.asm8, np.datetime64)