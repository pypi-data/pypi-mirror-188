from unittest.mock import patch, mock_open

import pytest

from refinitiv.data.content.esg.bulk._actions import parse_log_file
from .conftest import raise_


def test_actions_get_created_tables(actions):
    # when
    tables = actions.get_created_tables()

    # then
    assert tables is not None


def test_actions_add_pass_dict(actions):
    # given
    input_details = {"details": "details"}

    # when
    details = actions.add("action_name", **input_details)

    # then
    assert details == input_details


def test_actions_add_pass_kwargs(actions):
    # given
    expected_details = {"details": "details"}

    # when
    details = actions.add("action_name", details="details")

    # then
    assert details == expected_details


def test_actions_cleanup(actions):
    try:
        # when
        actions.cleanup()
    except Exception as e:
        assert False, str(e)


@pytest.mark.parametrize(
    "exception",
    [
        PermissionError,
        FileNotFoundError,
    ],
)
def test_actions_cleanup_when_error(actions, exception):
    # given
    remove_file_mock = patch("os.remove", new=lambda *_: raise_(exception))
    file_mock = patch("builtins.open", new=mock_open())

    # when
    file_mock.start()
    remove_file_mock.start()
    result = actions.cleanup()
    remove_file_mock.stop()
    file_mock.stop()

    # then
    assert result is None


def test_actions_details_by_action(actions):
    # when
    details_by_action = actions.details_by_action

    # then
    assert details_by_action is not None


def test_actions_downloaded(actions):
    # when
    downloaded = actions.downloaded()

    # then
    assert downloaded is not None


def test_actions_extracted(actions):
    # when
    extracted = actions.extracted()

    # then
    assert extracted is not None


def test_actions_get_downloaded(actions):
    # when
    downloaded = actions.get_downloaded()

    # then
    assert downloaded is not None


def test_actions_get_extracted(actions):
    # when
    extracted = actions.get_extracted()

    # then
    assert extracted is not None


def test_actions_get_not_updated_and_extracted(actions):
    # when
    not_updated, extracted = actions.get_not_updated_and_extracted()

    # then
    assert not_updated is not None and extracted is not None


def test_actions_table_created(actions):
    # when
    created = actions.table_created()

    # then
    assert created is not None


def test_actions_updated(actions):
    # when
    updated = actions.updated()

    # then
    assert updated is not None


def test_actions_cleaned_up_db(actions):
    # when
    cleaned_up = actions.cleaned_up_db()

    # then
    assert cleaned_up is not None


def test_parse_log_file():
    # given
    logpath = "./tests/unit/content/esg/bulk/test_log.txt"

    # when
    details_by_log_action = parse_log_file(logpath)

    # then
    assert details_by_log_action


def test_parse_log_file_catch_exception():
    # given
    logpath = "invalid_test_log.txt"

    # when
    details_by_log_action = parse_log_file(logpath)

    # then
    assert details_by_log_action is not None


def test_actions_update(actions):
    # given
    actions._details_by_action = ["1", "2ewf"]

    # when
    actions.update()

    # then
    assert actions._details_by_action is None
