from refinitiv.data._tools._converter import convert_content_data_to_df
import pandas as pd


def test_dataframe_requirements():
    content_data = {
        "headers": [
            {"name": "instrument"},
            {"name": "investorid"},
        ],
        "data": [["VOD.L", ""], ["JPN.M", None], ["IBM.N", "2004260"]],
    }
    df = convert_content_data_to_df(content_data)
    for row in df.itertuples():
        if row.instrument == "VOD.L":
            assert row.investorid == ""
        if row.instrument == "JPN.M":
            assert row.investorid is pd.NA
        if row.instrument == "IBM.N":
            assert isinstance(row.investorid, str)
