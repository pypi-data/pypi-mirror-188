import logging
import random

import pytest

from refinitiv.data.delivery import cfs
from tests.integration.constants_list import ISO_DATE_FORMAT
from tests.integration.delivery.cfs.conftest import (
    convert_string_to_date_format,
)


def get_random_file_name_from_fileset(fileset):
    response = cfs.files.Definition(fileset.id, page_size=10).get_data()
    random_file = random.choice(response.data.raw["value"])
    return random_file["filename"]


def check_single_file_received(response):
    files_count = len(response.data.raw["value"])
    assert (
        files_count == 1
    ), f"Response contains more than 1 file. Number of files: {files_count}, response:  \n {response.data.raw['value']}"


def check_all_files_contain_fileset_id(response, expected_fileset_id):
    files = response.data.raw["value"]
    for file in files:
        assert (
            file["filesetId"] == expected_fileset_id
        ), f"Found file which does not belong to defined fileset id {expected_fileset_id}: \n {file}"


def check_file_name_in_response(response, expected_file_name):
    files = response.data.raw["value"]
    for file in files:
        assert (
            file["filename"] == expected_file_name
        ), f"Found file with unexpected name: \n {file} \n expected name: {expected_file_name}"


def check_files_in_response_created_after_date(response, expected_date):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    files = response.data.raw["value"]
    for file in files:
        try:
            file_created_date = convert_string_to_date_format(
                file["created"], ISO_DATE_FORMAT
            )
            assert (
                file_created_date >= date
            ), f"found fileset modified before the required date {date}: \n {file}"
        except KeyError:
            logging.warning(f"The fileset does not have 'modified' field: {file}")


def check_files_in_response_modified_after_date(response, expected_date):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    files = response.data.raw["value"]
    for file in files:
        try:
            file_modified_date = convert_string_to_date_format(
                file["modified"], ISO_DATE_FORMAT
            )
            assert (
                file_modified_date >= date
            ), f"found fileset modified before the required date {date}: \n {file}"
        except KeyError:
            logging.warning(f"The fileset does not have 'modified' field: {file}")


def check_files_in_two_responses_are_not_the_same(response1, response2):
    for file in response1.data.raw["value"]:
        assert (
            file not in response2.data.raw["value"]
        ), f"Fileset from first request found in list of filesets in the second request: \n {file}"


@pytest.fixture(scope="function")
def get_random_fileset():
    filesets_response = cfs.file_sets.Definition("bulk-ESG", page_size=100).get_data()
    return random.choice(filesets_response.data.file_sets)
