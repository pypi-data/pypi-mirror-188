import pytest

from refinitiv.data.content.symbol_conversion import AssetClass
from refinitiv.data.content.symbol_conversion import AssetState
from refinitiv.data.content.symbol_conversion._asset_class import (
    _transform_to_string,
    search_all_category_by_asset_class,
    rcsasset_category_genealogy_by_asset_class,
    create_asset_class_request_strings,
)
from refinitiv.data.content.symbol_conversion._definition import _prepare_filter


def test_symbology_transform_to_string_search_all_category():
    # when
    result = _transform_to_string(
        values=[AssetClass.COMMODITIES, AssetClass.EQUITIES],
        category=search_all_category_by_asset_class,
    )

    # then
    assert result == "'Commodities' 'Equities'"


def test_symbology_transform_to_string_search_all_category_rcsasset_category():
    # when
    result = _transform_to_string(
        values=[AssetClass.WARRANTS, AssetClass.CERTIFICATES],
        category=rcsasset_category_genealogy_by_asset_class,
    )

    # then
    assert result == "'A:AA' 'A:6N'"


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    (
        (
            [AssetClass.COMMODITIES, AssetClass.EQUITIES],
            ("SearchAllCategoryv3 in ('Commodities' 'Equities')", ""),
        ),
        (
            [AssetClass.COMMODITIES, AssetClass.WARRANTS],
            (
                "SearchAllCategoryv3 in ('Commodities')",
                "RCSAssetCategoryGenealogy in ('A:AA')",
            ),
        ),
        ([AssetClass.CERTIFICATES], ("", "RCSAssetCategoryGenealogy in ('A:6N')")),
    ),
)
def test_symbology_create_asset_class_request_string(input_data, expected_result):
    # when
    result = create_asset_class_request_strings(asset_class=input_data)

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("input_data", "expected_result"),
    (
        (
            [AssetState.ACTIVE, [AssetClass.COMMODITIES, AssetClass.EQUITIES]],
            "AssetState eq 'AC' and (SearchAllCategoryv3 in ('Commodities' 'Equities'))",
        ),
        (
            [None, AssetClass.COMMODITIES],
            ("AssetState eq 'AC' and (SearchAllCategoryv3 in ('Commodities'))"),
        ),
        ([AssetState.INACTIVE, None], ("(AssetState ne 'AC' and AssetState ne null)")),
    ),
)
def test_prepare_filter(input_data, expected_result):
    # when
    result = _prepare_filter(*input_data)

    # then
    assert result == expected_result
