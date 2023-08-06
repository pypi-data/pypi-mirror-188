from refinitiv.data import _configure as configure


def test_data_grid_underlying_platform_default_parameter():
    # given
    expected = "udf"
    actual = configure.get_param("apis.data.datagrid.underlying-platform")

    # then
    assert actual == expected
