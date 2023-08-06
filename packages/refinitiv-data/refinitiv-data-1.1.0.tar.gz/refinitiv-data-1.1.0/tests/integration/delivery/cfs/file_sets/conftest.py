import logging
import random

from refinitiv.data.delivery import cfs
from tests.integration.constants_list import ISO_DATE_FORMAT
from tests.integration.delivery.cfs.conftest import (
    convert_string_to_date_format,
)


def prepare_random_fileset_name(bucket_name):
    response = cfs.file_sets.Definition(bucket=bucket_name).get_data()
    random_fileset = random.choice(response.data.raw["value"])
    return random_fileset["name"]


def prepare_random_package_id(bucket_name):
    response = cfs.packages.Definition(bucket_name=bucket_name).get_data()
    random_package = random.choice(response.data.raw["value"])
    return random_package["packageId"]


def check_fileset_contains_all_attributes(fileset, expected_attributes_dict):
    def prepare_attribute_object(name, value):
        return {"name": name, "value": value}

    fileset_attributes = fileset["attributes"]
    for key in expected_attributes_dict:
        assert (
            prepare_attribute_object(key, expected_attributes_dict[key])
            in fileset_attributes
        ), f"Found fileset which does not contain expected attribute {key}: \n {fileset}"


def check_fileset_contains_package_id(fileset, expected_package_id):
    assert (
        fileset["packageId"].lower() == expected_package_id.lower()
    ), f"Found fileset which does not contain expected  package id {expected_package_id}: \n {fileset}"


def check_fileset_contains_status(fileset, expected_status):
    assert (
        fileset["status"].lower() == expected_status.lower()
    ), f"Found fileset which does not contain expected  package id {expected_status}: \n {fileset}"


def check_filesets_in_response_available_after_date(response, expected_date):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    filesets = response.data.raw["value"]
    for fileset in filesets:
        try:
            fileset_available_from_date = convert_string_to_date_format(
                fileset["availableFrom"], ISO_DATE_FORMAT
            )
            assert (
                fileset_available_from_date >= date
            ), f"found fileset available before the required date {date}: \n {fileset}"
        except KeyError:
            logging.warning(
                f"The fileset does not have 'availableFrom' field: {fileset}"
            )


def check_filesets_in_response_available_before_date(response, expected_date):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    filesets = response.data.raw["value"]
    for fileset in filesets:
        try:
            fileset_available_to_date = convert_string_to_date_format(
                fileset["availableTo"], ISO_DATE_FORMAT
            )
            assert (
                fileset_available_to_date <= date
            ), f"found fileset available after the required date {date}: \n {fileset}"
        except KeyError:
            logging.warning(f"The fileset does not have 'availableTo' field: {fileset}")


def check_filesets_in_response_have_content_to_param_before_date(
    response, expected_date
):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    filesets = response.data.raw["value"]
    for fileset in filesets:
        try:
            fileset_content_to_date = convert_string_to_date_format(
                fileset["contentTo"], ISO_DATE_FORMAT
            )
            assert (
                fileset_content_to_date <= date
            ), f"found fileset with contentTo property after the required date {date}: \n {fileset}"
        except KeyError:
            logging.warning(f"The fileset does not have 'contentTo' field: {fileset}")


def check_filesets_in_response_have_content_from_param_after_date(
    response, expected_date
):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    filesets = response.data.raw["value"]
    for fileset in filesets:
        try:
            fileset_content_from_date = convert_string_to_date_format(
                fileset["contentFrom"], ISO_DATE_FORMAT
            )
            assert (
                fileset_content_from_date >= date
            ), f"found fileset with contentFrom property before the required date {date}: \n {fileset}"
        except KeyError:
            logging.warning(f"The fileset does not have 'contentFrom' field: {fileset}")


def check_filesets_in_response_created_after_date(response, expected_date):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    filesets = response.data.raw["value"]
    for fileset in filesets:
        try:
            fileset_created_date = convert_string_to_date_format(
                fileset["created"], ISO_DATE_FORMAT
            )
            assert (
                fileset_created_date >= date
            ), f"found fileset created before the required date {date}: \n {fileset}"
        except KeyError:
            logging.warning(f"The fileset does not have 'created' field: {fileset}")


def check_filesets_in_response_modified_after_date(response, expected_date):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    filesets = response.data.raw["value"]
    for fileset in filesets:
        try:
            fileset_modified_date = convert_string_to_date_format(
                fileset["modified"], ISO_DATE_FORMAT
            )
            assert (
                fileset_modified_date >= date
            ), f"found fileset modified before the required date {date}: \n {fileset}"
        except KeyError:
            logging.warning(f"The fileset does not have 'modified' field: {fileset}")


def check_filesets_in_two_responses_are_not_the_same(response1, response2):
    for fileset in response1.data.raw["value"]:
        assert (
            fileset not in response2.data.raw["value"]
        ), f"Fileset from first request found in list of filesets in the second request: \n {fileset}"


def get_fileset_from_bucket_with_numfiles_bigger_than(bucket_name, num_files):
    response = cfs.file_sets.Definition(bucket_name, page_size=100).get_data()
    results = []
    for item in response.data.file_sets:
        if item["num_files"] > num_files:
            results.append(item)
    return random.choice(results)
