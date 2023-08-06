import pandas as pd

from refinitiv.data._tools._dataframe import (
    convert_df_columns_to_datetime,
    convert_str_to_datetime,
)
from .conftest import TEST_CASES
from ..conftest import parametrize_with_test_case


@parametrize_with_test_case(
    "df,pattern,utc,delete_tz,expected_dtype,expected_df",
    TEST_CASES,
    "Simple DataFrame not valid datetime",
    "Simple DataFrame without timezone",
    "Simple DataFrame with timezone",
    "Simple DataFrame without timezone with flag utc=True",
    "Simple DataFrame with timezone with flag utc=True",
    "Simple DataFrame with timezone with flag utc=None, delete_tz=True",
    "Simple DataFrame without timezone with flag utc=True, delete_tz=True",
    "Simple DataFrame with timezone with flag utc=True, delete_tz=True",
)
def test_convert_df_columns_to_datetime(
    df, pattern, utc, delete_tz, expected_dtype, expected_df
):
    # when
    testing_df = convert_df_columns_to_datetime(df, pattern, utc, delete_tz)

    # then
    assert testing_df.Date.dtype == expected_dtype

    try:
        diff_df = testing_df.compare(expected_df)
    except ValueError as e:
        assert False, str(e)
    else:
        assert diff_df.empty is True, diff_df.to_string()


def test_not_valid_date_for_convert_str_to_datetime():
    # when
    testing = convert_str_to_datetime("1207")

    # then
    assert testing is pd.NaT
