from unittest.mock import patch, MagicMock

import pytest

from refinitiv.data.delivery._data._data_provider import ParsedData
from refinitiv.data.delivery.cfs._cfs_data_provider import (
    cfs_packages_data_provider,
    CFSRequestFactory,
    CFSStreamRequestFactory,
    CFSResponseFactory,
    CFSPackageRequestFactory,
    cfs_buckets_data_provider,
    cfs_file_sets_data_provider,
    cfs_files_data_provider,
)
from refinitiv.data.delivery.cfs._data_types import BaseData


@pytest.mark.parametrize(
    ("test_value", "expected"),
    [
        (
            {
                "url_root": "site.com",
                "url": "test_url",
                "path_parameters": [],
                "query_parameters": (("attributes", "size;depth"),),
            },
            "site.com/test_url?attributes=size;depth",
        ),
        (
            {
                "url_root": "site.com",
                "url": "test_url",
                "path_parameters": [],
                "query_parameters": tuple(),
            },
            "site.com/test_url",
        ),
    ],
)
def test_cfs_request_factory_update_url(test_value, expected):
    # given
    request_factory = CFSRequestFactory()

    # when
    result = request_factory.update_url(**test_value)

    # then
    assert result == expected


@pytest.mark.parametrize(
    ("test_value", "expected"),
    [
        (
            [..., "site.com/files"],
            "site.com/files/{id}/stream",
        ),
    ],
)
def test_cfs_stream_request_factory_get_url(test_value, expected):
    # given
    request_factory = CFSStreamRequestFactory()

    # when
    result = request_factory.get_url(*test_value)

    # then
    assert result == expected


@pytest.mark.parametrize(
    ("test_value", "expected"),
    [
        ({"_package_id": "5"}, "/file-store/v1/packages/5"),
        ({"_package_id": ""}, "/file-store/v1/packages/"),
        ({"_package_id": None}, "/file-store/v1/packages"),
        ({"package_id": "5"}, "/file-store/v1/packages"),
        ({"some_other": "5"}, "/file-store/v1/packages"),
    ],
)
def test_cfs_package_request_factory_get_url(test_value, expected):
    # given
    args = [..., "/file-store/v1/packages"]
    request_factory = CFSPackageRequestFactory()

    # when
    result = request_factory.get_url(*args, **test_value)

    # then
    assert result == expected


@pytest.mark.parametrize(
    "test_value",
    [
        {"_package_id": 5, "a": "aa"},
        {"_package_id": "5", "a": "aa"},
        {"_package_id": "", "a": "aa"},
    ],
)
def test_cfs_package_request_factory_get_query_parameters_with_id_argument(test_value):
    # given
    request_factory = CFSPackageRequestFactory()

    # when
    result = request_factory.get_query_parameters(**test_value)

    # then
    assert not result


@pytest.mark.parametrize(
    "test_value",
    [
        {"_package_id": None, "a": "aa"},
        {"package_id": "5", "a": "aa"},
    ],
)
def test_cfs_package_request_factory_get_query_parameters_not_valid_id_arg(test_value):
    # given
    request_factory = CFSPackageRequestFactory()

    # when
    result = request_factory.get_query_parameters(**test_value)

    # then
    assert result


@pytest.mark.parametrize(
    ("test_value", "expected"),
    [
        (
            {"path_parameters": {"par1": "val1", "par2": "val2"}},
            {"par1": "val1", "par2": "val2"},
        ),
        (
            {"path_parameters": {"par1": "val1", "par2": "val2"}, "id": "123"},
            {"par1": "val1", "par2": "val2", "id": "123"},
        ),
        (
            {"path_parameters": {"par1": "val1", "par2": "val2"}, "par": "123"},
            {"par1": "val1", "par2": "val2"},
        ),
        (
            {
                "path_parameters": {"par1": "val1", "par2": "val2", "id": "12"},
                "id": "123",
            },
            {"par1": "val1", "par2": "val2", "id": "123"},
        ),
    ],
)
def test_cfs_stream_request_factory_get_path_parameters(test_value, expected):
    # given
    request_factory = CFSStreamRequestFactory()

    # when
    result = request_factory.get_path_parameters(**test_value)

    # then
    assert result == expected


@pytest.mark.parametrize(
    ("test_value", "expected"),
    [
        (dict(), [("doNotRedirect", "true")]),
        (
            {"query_parameters": [("par1", "val1")]},
            [("par1", "val1"), ("doNotRedirect", "true")],
        ),
    ],
)
def test_cfs_stream_request_factory_get_query_parameters(test_value, expected):
    # given
    request_factory = CFSStreamRequestFactory()

    # when
    result = request_factory.get_query_parameters(**test_value)

    # then
    assert result == expected


@pytest.mark.parametrize(
    ("test_value", "expected"),
    [
        (
            ParsedData({}, {}, {}),
            {"content_data": {}},
        ),
        (
            ParsedData({}, {}, {"value": [dict()]}),
            {"content_data": {"value": [dict()]}},
        ),
    ],
)
def test_cfs_response_factory_create_success(test_value, expected):
    # given
    response_factory = CFSResponseFactory(data_class=MagicMock)

    mock_iter_obj = patch("refinitiv.data.delivery.cfs._cfs_data_provider.IterObj")

    # when
    mock_iter_obj.start()
    result = response_factory.create_success(test_value)
    mock_iter_obj.stop()

    # then
    assert result


def test_cfs_data_provider():
    # given
    # when
    for dp in (
        cfs_buckets_data_provider,
        cfs_file_sets_data_provider,
        cfs_files_data_provider,
    ):
        # then
        assert isinstance(dp.response, CFSResponseFactory)
        assert isinstance(dp.request, CFSRequestFactory)


def test_cfs_packages_data_provider():
    # when
    dp = cfs_packages_data_provider

    # then
    assert isinstance(dp.response, CFSResponseFactory)
    assert isinstance(dp.request, CFSPackageRequestFactory)


@pytest.mark.parametrize(
    "input_raw",
    [
        {"packageId": "0002-0002-00000002-0002-000000000002"},
        {
            "value": [
                {"packageId": "0002-0002-00000002-0002-000000000002"},
                {"packageId": "4000-0983-edb8b42c-8b72-a5aba64abb88"},
                {"packageId": "4000-0f0a-b1348f7c-b0a0-1203c3ee5a0f"},
            ]
        },
    ],
)
def test_cfs_build_df_raws(input_raw):
    # when
    data = BaseData(input_raw)

    # then
    assert not data.df.empty
