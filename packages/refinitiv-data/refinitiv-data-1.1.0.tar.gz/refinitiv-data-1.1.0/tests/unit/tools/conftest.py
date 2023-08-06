from ..conftest import args
from . import data_for_tests as dt


TEST_CASES = {
    "Simple DataFrame not valid datetime": args(
        df=dt.INPUT_DF_NOT_VALID_DATETIME,
        pattern="Date",
        utc=None,
        delete_tz=False,
        expected_dtype="datetime64[ns]",
        expected_df=dt.EXPECTED_DF_NOT_VALID_DATETIME,
    ),
    "Simple DataFrame without timezone": args(
        df=dt.INPUT_DF_WITHOUT_TIMEZONE,
        pattern="Date",
        utc=None,
        delete_tz=False,
        expected_dtype="datetime64[ns]",
        expected_df=dt.EXPECTED_DF_WITHOUT_TIMEZONE,
    ),
    "Simple DataFrame with timezone": args(
        df=dt.INPUT_DF_WITH_TIMEZONE,
        pattern="Date",
        utc=None,
        delete_tz=False,
        expected_dtype="datetime64[ns, UTC]",
        expected_df=dt.EXPECTED_DF_WITH_TIMEZONE,
    ),
    "Simple DataFrame without timezone with flag utc=True": args(
        df=dt.INPUT_DF_WITHOUT_TIMEZONE,
        pattern="Date",
        utc=True,
        delete_tz=False,
        expected_dtype="datetime64[ns, UTC]",
        expected_df=dt.EXPECTED_DF_WITH_TIMEZONE,
    ),
    "Simple DataFrame with timezone with flag utc=True": args(
        df=dt.INPUT_DF_WITH_TIMEZONE,
        pattern="Date",
        utc=True,
        delete_tz=False,
        expected_dtype="datetime64[ns, UTC]",
        expected_df=dt.EXPECTED_DF_WITH_TIMEZONE,
    ),
    "Simple DataFrame without timezone with flag utc=None, delete_tz=True": args(
        df=dt.INPUT_DF_WITHOUT_TIMEZONE,
        pattern="Date",
        utc=None,
        delete_tz=True,
        expected_dtype="datetime64[ns]",
        expected_df=dt.EXPECTED_DF_WITHOUT_TIMEZONE,
    ),
    "Simple DataFrame with timezone with flag utc=None, delete_tz=True": args(
        df=dt.INPUT_DF_WITH_TIMEZONE,
        pattern="Date",
        utc=None,
        delete_tz=True,
        expected_dtype="datetime64[ns]",
        expected_df=dt.EXPECTED_DF_WITHOUT_TIMEZONE,
    ),
    "Simple DataFrame without timezone with flag utc=True, delete_tz=True": args(
        df=dt.INPUT_DF_WITHOUT_TIMEZONE,
        pattern="Date",
        utc=True,
        delete_tz=True,
        expected_dtype="datetime64[ns]",
        expected_df=dt.EXPECTED_DF_WITHOUT_TIMEZONE,
    ),
    "Simple DataFrame with timezone with flag utc=True, delete_tz=True": args(
        df=dt.INPUT_DF_WITH_TIMEZONE,
        pattern="Date",
        utc=True,
        delete_tz=True,
        expected_dtype="datetime64[ns]",
        expected_df=dt.EXPECTED_DF_WITHOUT_TIMEZONE,
    ),
}


TEST_CASES_1 = {
    "Simple DataFrame without timezone": args(
        df=dt.INPUT_DF_WITHOUT_TIMEZONE,
        column_name="Date",
        expected_df=dt.EXPECTED_DF_WITHOUT_TIMEZONE,
    ),
    "Simple DataFrame with timezone": args(
        df=dt.INPUT_DF_WITH_TIMEZONE,
        column_name="Date",
        expected_df=dt.EXPECTED_DF_WITHOUT_TIMEZONE,
    ),
}
