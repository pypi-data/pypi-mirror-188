import numpy as np


def check_response_dataframe_instrument_contains_expected_universes(
    response, expected_universes
):
    dataframe = response.data.df
    try:
        retrieved_universes = dataframe["instrument"].tolist()
    except KeyError:
        retrieved_universes = dataframe["Instrument"].tolist()
    retrieved_universes = set(retrieved_universes)

    if all([isinstance(item, np.int64) for item in retrieved_universes]):
        retrieved_universes = list(map(str, retrieved_universes))

    if isinstance(expected_universes, str):
        assert (
            expected_universes in retrieved_universes
        ), f"Expected universe {expected_universes} is not found in list of instruments retrieved from dataframe: {retrieved_universes}"
    elif isinstance(expected_universes, list):
        for universe in expected_universes:
            assert (
                universe in retrieved_universes
            ), f"Expected universe {universe} is not found in list of instruments retrieved from dataframe: {retrieved_universes}"
    else:
        print(f"Unexpected universe type provided: {type(expected_universes)}")


def get_expected_column(use_field_names_in_headers, expected_titles, expected_names):
    expected_column = expected_titles
    if use_field_names_in_headers:
        expected_column = expected_names

    return expected_column
