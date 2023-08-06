import logging

from tests.integration.constants_list import ISO_DATE_FORMAT
from tests.integration.delivery.cfs.conftest import (
    convert_string_to_date_format,
)


def check_buckets_in_response_created_after_date(expected_date, response):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    buckets = response.data.raw["value"]
    for bucket in buckets:
        bucket_created_date = convert_string_to_date_format(
            bucket["created"], ISO_DATE_FORMAT
        )
        assert (
            bucket_created_date > date
        ), f"found bucket created before the required date {date}: \n {bucket}"


def check_buckets_in_response_modified_after_date(expected_date, response):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    buckets = response.data.raw["value"]
    for bucket in buckets:
        bucket_modified_date = convert_string_to_date_format(
            bucket["modified"], ISO_DATE_FORMAT
        )
        assert (
            bucket_modified_date > date
        ), f"found bucket modified before the required date {date}: \n {bucket}"


def check_buckets_in_response_available_before_date(expected_date, response):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    buckets = response.data.raw["value"]
    for bucket in buckets:
        try:
            bucket_available_from_date = convert_string_to_date_format(
                bucket["availableFrom"], ISO_DATE_FORMAT
            )
            assert (
                bucket_available_from_date <= date
            ), f"found bucket available only after the required date {date}: \n {bucket}"
        except KeyError:
            logging.warning(f"The bucket does not have 'availableFrom' field: {bucket}")


def check_buckets_in_response_available_after_date(expected_date, response):
    date = convert_string_to_date_format(expected_date, ISO_DATE_FORMAT)
    buckets = response.data.raw["value"]
    for bucket in buckets:
        try:
            bucket_available_to_date = convert_string_to_date_format(
                bucket["availableTo"], ISO_DATE_FORMAT
            )
            assert (
                bucket_available_to_date >= date
            ), f"found bucket available before  the required date {date}: \n {bucket}"
        except KeyError:
            logging.warning(f"The bucket does not have 'availableFrom' field: {bucket}")


def check_all_attributes_found_in_bucket(bucket, expected_attributes_list):
    if isinstance(expected_attributes_list, str):
        expected_attributes_list = [expected_attributes_list]
    for attribute in expected_attributes_list:
        assert (
            attribute in map(str.lower, bucket["attributes"])
        ), f"Found bucket which does not contain expected attribute {attribute}: {bucket} "


def check_all_buckets_contain_attributes(response, expected_attributes_list):
    for bucket in response.data.raw["value"]:
        check_all_attributes_found_in_bucket(bucket, expected_attributes_list)


def check_buckets_in_two_responses_are_not_the_same(response1, response2):
    for bucket in response1.data.raw["value"]:
        assert (
            bucket not in response2.data.raw["value"]
        ), f"Bucket from first request found in list of buckets in the second request: \n {bucket}"
