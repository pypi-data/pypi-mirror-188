import pandas as pd
import pytest

from refinitiv.data.content.ipa.financial_contracts._contracts_data_provider import (
    Data,
    financial_contracts_build_df,
)


@pytest.mark.parametrize(
    "input_data,input_type,expected_data",
    [
        ([None], "Date", pd.NaT),
        (["2032-02-28"], "Date", pd.to_datetime("2032-02-28")),
        (["2032-02-28T00:00:00Z"], "DateTime", pd.to_datetime("2032-02-28")),
    ],
)
def test_build_df_with_datetime(input_data, input_type, expected_data):
    # given
    expected_df = pd.DataFrame({"IssueDate": {0: expected_data}})
    input_raw = {
        "headers": [
            {"type": input_type, "name": "IssueDate"},
        ],
        "data": [input_data],
    }

    # then
    testing = Data(raw=input_raw, dfbuilder=financial_contracts_build_df)

    # when
    try:
        diff_df = testing.df.compare(expected_df)
    except ValueError as e:
        assert False, str(e)
    else:
        assert diff_df.empty is True, diff_df.to_string()
