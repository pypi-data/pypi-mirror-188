import os
import sqlite3
from unittest.mock import mock_open
from unittest.mock import patch
from urllib.parse import unquote

import pytest

from refinitiv.data.content.esg.bulk._db_manager import (
    get_query,
    uri_to_path,
    prepare_insert_query,
    prepare_search_query,
)
from refinitiv.data.content.esg.bulk._errors import KeyNotFoundException


def test_db_manager_update_db_does_not_close_connection(db_manager):
    # when
    db_manager.update_db([("", [], {})])

    # then
    try:
        db_manager.commit()
    except sqlite3.ProgrammingError:
        pytest.fail("manager.update_db() closed db connection")


@pytest.mark.parametrize(
    ("test_value", "expected_result"),
    [
        ("filename", "filename"),
        ("file://", ""),
    ],
)
def test_get_query(test_value, expected_result):
    # given
    file_mock = patch("builtins.open", new=mock_open())

    # when
    file_mock.start()
    result = get_query(test_value)
    file_mock.stop()

    # then
    assert result == expected_result


@pytest.mark.parametrize(
    ("input_value", "expected_result"),
    [
        ("file://file.txt", "file.txt"),
        ("file:///file.txt", "/file.txt"),
        ("file:///dir1/file.txt", "/dir1/file.txt"),
        ("file://dir1/file.txt", "dir1/file.txt"),
        ("file://dir1/dir2/file.txt", "dir1/dir2/file.txt"),
        ("file://C:dir1/dir2//file.txt", "C:dir1/dir2/file.txt"),
        ("file://C:dir1//dir2//file.txt", "C:dir1/dir2/file.txt"),
    ],
)
def test_uri_to_path(input_value, expected_result):
    # given

    # when
    test_value = uri_to_path(input_value)

    test_value = os.path.normpath(unquote(test_value))
    expected_result = os.path.normpath(unquote(expected_result))

    # then
    assert test_value == expected_result, test_value


def test_db_manager_update_db_no_filesdata(db_manager):
    # given
    db_manager._actions.get_downloaded = lambda: [1, 2]

    # when
    result = db_manager.update_db("")

    # then
    assert result is None


def test_db_manager_update_db_no_init_file(db_manager):
    # given
    db_manager._actions.get_downloaded = lambda: []

    # when
    # then
    with pytest.raises(FileNotFoundError):
        db_manager.update_db("")


class TestPrepareInsertQuery:
    def test_basic(self):
        assert (
            prepare_insert_query(
                "text #File.attr #{Fields.attr}",
                {"attr": "a"},
                {"attr": "b"},
            )
            == "text b a"
        )

    def test_null(self):
        assert prepare_insert_query("a = #File.attr", {}) == "a = null"

    def test_multilevel_dicts(self):
        # issue with multilevel and nulls:
        # easy to make a typo in multilevel without any errors
        assert (
            prepare_insert_query(
                "text #File.a.b #Fields.c.d",
                {"c": {"d": "x"}},
                {"a": {"b": "y"}},
            )
            == "text y x"
        )

    def test_lists_inside(self):
        assert prepare_insert_query("#Fields.a.0.b", {"a": [{"b": "x"}]}) == "x"
        assert prepare_insert_query("#Fields.a.0", {"a": ["y"]}) == "y"

    def test_nonfile_nonfields(self):
        with pytest.raises(KeyNotFoundException):
            prepare_insert_query("#Filo.attr", {})

    def test_quote_escaping(self):
        # For some reason this applies to fields with 'Name' in it only
        assert (
            prepare_insert_query(
                "#Fields.Name #Fields.LastName #Fields.Address",
                {"Name": "A'b", "LastName": "C'd", "Address": "E'f"},
            )
            == "A''b C''d E'f"
        )


class TestPrepareSearchQuery:
    def test_basic(self):
        # replaces '*' and '#universe#'
        assert (
            prepare_search_query(
                "smth * from #smth# in #{universe}", ["u1", "u2"], ["col1", "col2"]
            )
            == "smth col1, col2 from #smth# in ('u1', 'u2')"
        )

    def test_one_instrument_in_universe(self):
        assert prepare_search_query("in #{universe}", ["u1"]) == "in ('u1')"
