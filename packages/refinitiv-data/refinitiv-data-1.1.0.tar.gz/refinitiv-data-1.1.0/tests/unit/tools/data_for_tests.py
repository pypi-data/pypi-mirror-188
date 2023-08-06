import pandas as pd


"""
      Date
0     1201
"""

INPUT_DF_NOT_VALID_DATETIME = pd.DataFrame({"Date": {0: "1201"}})
EXPECTED_DF_NOT_VALID_DATETIME = pd.DataFrame({"Date": {0: pd.NaT}})

"""
                Date
0     2020-11-28T00:00:00
1     2020-12-31T00:00:00
"""

INPUT_DF_WITHOUT_TIMEZONE = pd.DataFrame(
    {
        "Date": {0: "2020-11-28T00:00:00", 1: "2020-12-31T00:00:00"},
    }
)

EXPECTED_DF_WITHOUT_TIMEZONE = pd.DataFrame(
    {
        "Date": {
            0: pd.to_datetime("2020-11-28T00:00:00"),
            1: pd.to_datetime("2020-12-31T00:00:00"),
        },
    }
)


"""
                      Date
0     2020-11-28T00:00:00.000Z
1     2020-12-31T00:00:00.000Z
"""

INPUT_DF_WITH_TIMEZONE = pd.DataFrame(
    {
        "Date": {0: "2020-11-28T00:00:00.000Z", 1: "2020-12-31T00:00:00.000Z"},
    }
)

EXPECTED_DF_WITH_TIMEZONE = pd.DataFrame(
    {
        "Date": {
            0: pd.to_datetime("2020-11-28T00:00:00.000Z"),
            1: pd.to_datetime("2020-12-31T00:00:00.000Z"),
        },
    }
)
