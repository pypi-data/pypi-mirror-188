from os.path import normpath

import pytest

from refinitiv.data.delivery.cfs._tools import (
    _convert_name,
    _get_query_parameter,
    _get_query_params,
    _convert_date_time,
    path_join,
    remove_one_ext,
)


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        ("name", "name"),
        ("created_since", "createdSince"),
        ("modified_since", "modifiedSince"),
        ("available_from", "availableFrom"),
        ("available_to", "availableTo"),
        ("attributes", "attributes"),
        ("page_size", "pageSize"),
        ("skip_token", "skipToken"),
        ("bucket", "bucket"),
        ("package_id", "packageId"),
        ("status", "status"),
        ("content_from", "contentFrom"),
        ("content_to", "contentTo"),
        ("fileset_id", "filesetId"),
        ("filesetId", "filesetId"),
        ("filename", "filename"),
        ("package_name", "packageName"),
        ("package_type", "packageType"),
        ("bucket_name", "bucketName"),
        ("page", "page"),
        ("included_total_result", "includedTotalResult"),
        ("included_entitlement_result", "includedEntitlementResult"),
    ],
)
def test__convert_name(test_value, expected_result):
    # given

    # when
    result = _convert_name(test_value)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        ({}, []),
        ({"x": 1, "y": None}, [("x", 1)]),
        (
            {"fileset_id": "wef32", "some_value": True},
            [("filesetId", "wef32"), ("someValue", True)],
        ),
    ],
)
def test_get_query_params(test_value, expected_result):
    assert expected_result == _get_query_params(**test_value)


def test__get_query_parameter():
    # given
    test_values = (
        "doNotRedirect",
        "https://api.refinitiv.com/file-store/v1/files/{fileId}/stream?doNotRedirect=true",
    )
    expected_result = "true"

    # when
    result = _get_query_parameter(*test_values)

    # then
    assert result == expected_result


def test__convert_date_time():
    # given
    test_value = "05-20-2021"

    # when
    result = _convert_date_time(test_value)
    expected_result = "2021-05-20T00:00:00Z"

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    (
        (("test_folder", "filename"), normpath("test_folder/filename")),
        (("/test_folder", "filename"), normpath("/test_folder/filename")),
        (("test_folder/", "filename"), normpath("test_folder/filename")),
        (("test_folder", "filename/"), normpath("test_folder/filename")),
        (("/test_folder/", "filename"), normpath("/test_folder/filename")),
        (("/test_folder", "filename/"), normpath("/test_folder/filename")),
        (("/test_folder/", "filename/"), normpath("/test_folder/filename")),
    ),
)
def test_path_join(test_value, expected_result):
    assert path_join(*test_value) == expected_result


@pytest.mark.parametrize(
    "input_value, expected_value",
    [
        ("filename.ext_1.ext_2", "filename.ext_1"),
        ("filename.ext_1", "filename"),
        ("filename", "filename"),
    ],
)
def test_remove_one_ext(input_value, expected_value):
    # when
    testing_value = remove_one_ext(input_value)

    # then
    assert testing_value == expected_value
