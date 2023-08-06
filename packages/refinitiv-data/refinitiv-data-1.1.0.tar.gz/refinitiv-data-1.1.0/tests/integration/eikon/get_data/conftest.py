def check_dataframe_contains_instruments(dataframe, expected_instruments):
    retrieved_rows_names = dataframe["Instrument"].tolist()
    for instrument in expected_instruments:
        assert (
            instrument in retrieved_rows_names
        ), f"Expected instrument '{instrument}' is not found in list of rows retrieved from dataframe: {retrieved_rows_names}"


def check_dataframe_contains_fields(dataframe, expected_fields):
    retrieved_column_names = dataframe.columns.array
    retrieved_column_names_lowercase = list(
        map(lambda x: x.lower(), retrieved_column_names)
    )
    for field in expected_fields:
        assert (
            field.lower() in retrieved_column_names_lowercase
        ), f"Expected field '{field}' is not found in list of columns retrieved from dataframe: {retrieved_column_names}"


def check_success_response(df, err):
    assert not df.empty, f"Empty dataframe received"
    assert not err, f"Error received in response: {err}"
