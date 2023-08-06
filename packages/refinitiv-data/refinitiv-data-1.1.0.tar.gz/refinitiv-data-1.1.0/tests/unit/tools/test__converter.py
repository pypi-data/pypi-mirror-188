from refinitiv.data._tools._converter import (
    try_copy_to_list,
    convert_dict_to_df,
    convert_content_data_to_df,
)
import pytest


def test_convert_dict_to_df_empty_data():
    # given
    data = []
    columns = ["a", "b"]

    # when
    df1 = convert_dict_to_df(data, columns)
    df2 = convert_dict_to_df(data, [])

    # then
    assert list(df1) == columns
    assert df1.empty
    assert df2.empty


def test_convert_dict_to_df_with_data():
    # given
    data = [[1, 2], [3, 4]]
    columns = ["a", "b"]

    # when
    df = convert_dict_to_df(data, columns)

    # then
    assert list(df) == columns
    assert df.size == 4
    assert (df.get("a") == [1, 3]).all()
    assert (df.get("b") == [2, 4]).all()


def test_content_data_to_df_empty():
    # given
    data = {}

    # when
    df = convert_content_data_to_df(data)

    # then
    assert df.empty


def test_content_data_to_df():
    # given
    data = {
        "headers": [{"name": "a", "title": "A1"}, {"name": "b", "title": "B1"}],
        "data": [[1, 2], [3, 4]],
    }

    # when
    df_name_as_headers = convert_content_data_to_df(
        data, use_field_names_in_headers=True
    )
    df_title_as_headers = convert_content_data_to_df(
        data, use_field_names_in_headers=False
    )

    df_default_headers = convert_content_data_to_df(data)

    # then
    assert list(df_name_as_headers) == ["a", "b"]
    assert df_name_as_headers.size == 4
    assert (df_name_as_headers.get("a") == [1, 3]).all()
    assert (df_name_as_headers.get("b") == [2, 4]).all()

    assert list(df_title_as_headers) == ["A1", "B1"]
    assert df_title_as_headers.size == 4
    assert (df_title_as_headers.get("A1") == [1, 3]).all()
    assert (df_title_as_headers.get("B1") == [2, 4]).all()

    assert list(df_default_headers) == ["a", "b"]
    assert df_default_headers.size == 4
    assert (df_default_headers.get("a") == [1, 3]).all()
    assert (df_default_headers.get("b") == [2, 4]).all()


@pytest.mark.parametrize(
    "input_arg",
    [[1, 2, 3], tuple([1, 2, 3]), {1, 2, 3}, {1: "1", 2: "2", 3: "3"}],
)
def test_convert_to_list_iterable_objects(input_arg):
    # given
    id_input_arg = id(input_arg)

    # when
    test_result = try_copy_to_list(input_arg)

    # then
    assert test_result == list(input_arg)
    assert id(test_result) != id_input_arg


@pytest.mark.parametrize(
    "input_arg",
    [None, 1, True, 1.1, "", "sdsads"],
)
def test_convert_to_list_not_iterable_objects(input_arg):
    # given
    id_input_arg = id(input_arg)

    # when
    test_result = try_copy_to_list(input_arg)

    # then
    assert test_result == input_arg
    assert id(test_result) == id_input_arg
