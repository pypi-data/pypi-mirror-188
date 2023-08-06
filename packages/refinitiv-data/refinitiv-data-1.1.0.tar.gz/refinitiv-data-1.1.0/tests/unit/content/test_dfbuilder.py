import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data.content._df_build_type import DFBuildType
from refinitiv.data.content._df_builder_factory import (
    get_dfbuilder,
    content_type_by_build_type,
)
from refinitiv.data.delivery._data._data_provider_factory import (
    data_provider_by_data_type,
)


@pytest.mark.parametrize(
    "content_type,build_type",
    [
        (ContentType.DATA_GRID_RDP, DFBuildType.INDEX),
        (ContentType.DATA_GRID_RDP, DFBuildType.DATE_AS_INDEX),
        (ContentType.DATA_GRID_UDF, DFBuildType.INDEX),
        (ContentType.DATA_GRID_UDF, DFBuildType.DATE_AS_INDEX),
    ],
)
def test_get_df_builder(content_type, build_type):
    # when
    dfbuilder = get_dfbuilder(content_type, build_type)

    # then
    assert callable(dfbuilder) is True


def test_get_df_builder_raise_error_if_not_found_content_type():
    content_type = "__test_content_type__"
    # then
    with pytest.raises(
        ValueError, match="Cannot find mapping for content_type=__test_content_type__"
    ):
        # when
        get_dfbuilder(content_type, DFBuildType.INDEX)


def test_get_df_builder_raise_error_if_not_found_build_type():
    build_type = "__test_build_type__"
    # then
    with pytest.raises(
        ValueError, match="Cannot find mapping for dfbuild_type=__test_build_type__"
    ):
        # when
        get_dfbuilder(ContentType.DATA_GRID_UDF, build_type)
