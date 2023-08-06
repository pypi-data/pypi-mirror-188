OHLC_COLUMNNS_NAMES = ["CLOSE", "COUNT", "HIGH", "LOW", "OPEN", "VOLUME"]


def check_dataframe_contains_ohlc_columns_and_rics(df, expected_rics):
    column_names = list(df.columns.values)
    rics = df.columns.name
    if isinstance(expected_rics, list):
        rics, column_names = df.axes[1].levels
    compare_arrays(OHLC_COLUMNNS_NAMES, column_names)
    compare_arrays(rics, expected_rics)


def compare_arrays(array1, array2):
    assert len(array1) == len(array2)
    for item in array1:
        assert item in array2
