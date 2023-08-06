import pandas as pd


INPUT_DF_WITHOUT_DATE = pd.DataFrame(
    {
        "IssuerCountry": {0: "ConstantIndex"},
    }
)
EXPECTED_DF_WITHOUT_DATE = INPUT_DF_WITHOUT_DATE


INPUT_DF_WITH_DATE = pd.DataFrame(
    {
        "IssuerCountry": {0: "ConstantIndex"},
        "IssueDate": {0: "2032-02-28 00:00:00+0000"},
    }
)
EXPECTED_DF_WITH_DATE = pd.DataFrame(
    {
        "IssuerCountry": {0: "ConstantIndex"},
        "IssueDate": {0: pd.to_datetime("2032-02-28 00:00:00")},
    }
)
