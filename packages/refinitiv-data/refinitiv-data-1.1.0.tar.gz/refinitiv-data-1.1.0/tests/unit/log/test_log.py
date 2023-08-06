import logging
import os
from importlib import reload

import pytest

import refinitiv.data._log as session_logging
from refinitiv.data import _log as log
from refinitiv.data._core.session import DesktopSession
from .conftest import Record, stub_datetime
from ..conftest import args


@pytest.mark.parametrize(
    "input_log_level,expected_log_level",
    [
        ("", logging.INFO),
        ("DEBUG", logging.DEBUG),
        ("debug", logging.DEBUG),
        ("warn", logging.WARN),
        ("silent", logging.CRITICAL),
    ],
)
def test_convert_log_level(input_log_level, expected_log_level):
    # given

    # when
    testing_log_level = session_logging.convert_log_level(input_log_level)

    # then
    assert testing_log_level == expected_log_level


@pytest.mark.parametrize(
    "testing_data",
    [
        (Record("module:awesome"), "", False),
        (Record("module"), "*", True),
        (Record("session:module:a"), "session*", True),
        (Record("session:module:a"), "session:mod*", True),
        (Record("module:a:session"), "session*", False),
        (Record("module:a:session"), "module:a:*", True),
        (Record("module:b"), "session*, module:b, module:c", True),
        (Record("session:a"), "session*,module:b,module:c", True),
        (Record("module:a"), "*,-module:a", False),
        (Record("module:g"), "module:*, -module:b, -module:c", True),
        (Record("module:c"), "module:*, -module:b, -module:c", False),
        (Record("module:session"), "-module:*", False),
    ],
)
def test_make_filter(testing_data):
    # given
    record, filter_by, expected_result = testing_data

    # when
    filterer = log.make_filter(filter_by)
    testing_result = filterer(record)

    # then
    assert (
        testing_result == expected_result
    ), f"record={record.name}, filter_by={filter_by}"


def test_session_logger_and_logger_from_get_logger_is_same():
    # given
    session = DesktopSession("", name="test")
    expected_logger = session._logger

    # when
    testing_logger = log.get_logger(f"sessions.desktop.test.{session.session_id}")

    # then
    assert testing_logger == expected_logger


def test_get_logger_works_normal():
    try:
        logger = log.get_logger("test_get_logger")
    except Exception as e:
        assert False, e

    assert logger


def test_after_logger_disposed_handlers_are_empty():
    # given
    logger = log.get_logger("test_dispose_logger")

    # when
    log.dispose_logger(logger)

    # then
    assert logger.handlers == []


def test_dispose_logger_method_can_dispose_by_name():
    # given
    logger_name = "test_dispose_logger_name"
    logger = log.get_logger(logger_name)

    # when
    log.dispose_logger(logger_name)

    # then
    assert logger.handlers == []


def test_dispose_logger_method_can_dispose_by_logger_object():
    # given
    logger = log.get_logger("test_dispose_logger_name")

    # when
    log.dispose_logger(logger)

    # then
    assert logger.handlers == []


def test_existing_loggers_increase_after_call_create_logger_method():
    # given
    loggers_names = log.existing_loggers()
    before = len(loggers_names)

    # when
    log.create_logger("test_existing_loggers")
    loggers_names = log.existing_loggers()
    after = len(loggers_names)

    # then
    assert after - before == 1


def test_set_log_level_can_works_with_logger_name():
    # given
    logger_name = "test_set_log_level"
    logger = log.get_logger(logger_name)
    expected_value = 1
    input_value = 1

    # when
    log.set_log_level(logger_name, input_value)

    # then
    testing_value = logger.level
    assert testing_value == expected_value


def test_set_log_level_can_works_with_logger_object():
    # given
    logger = log.get_logger("test_set_log_level")
    expected_value = 5
    input_value = 5

    # when
    log.set_log_level(logger, input_value)

    # then
    testing_value = logger.level
    assert testing_value == expected_value


@pytest.mark.parametrize(
    "input_value,expected_value",
    (
        args(
            input="\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib.artem.9",
            expected="\\tests\\sandbox\\20210106-1715-9-24124-refinitiv-data-platform-lib.artem",
        ),
        args(
            input="\\tests\\sandbox\\20210106-1715-24124-refinitiv.data.platform.lib.9",
            expected="\\tests\\sandbox\\20210106-1715-9-24124-refinitiv.data.platform.lib",
        ),
        args(
            input="\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib.9",
            expected="\\tests\\sandbox\\20210106-1715-9-24124-refinitiv-data-platform-lib",
        ),
        args(
            input="\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib..9",
            expected="\\tests\\sandbox\\20210106-1715-9-24124-refinitiv-data-platform-lib.",
        ),
        args(
            input="\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib-.9",
            expected="\\tests\\sandbox\\20210106-1715-9-24124-refinitiv-data-platform-lib-",
        ),
        args(
            input="\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib.",
            expected="\\tests\\sandbox\\20210106-1715--24124-refinitiv-data-platform-lib",
        ),
        args(
            input="\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib-",
            expected="\\tests\\sandbox\\20210106-1715--24124-refinitiv-data-platform-lib-",
        ),
        args(
            input="\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib.-",
            expected="\\tests\\sandbox\\20210106-1715--24124-refinitiv-data-platform-lib.-",
        ),
        args(
            input="\\tests\\sandbox\\20210106-1715-24124-refinitiv-data-platform-lib-.",
            expected="\\tests\\sandbox\\20210106-1715--24124-refinitiv-data-platform-lib-",
        ),
    ),
)
def test_filenamer(input_value, expected_value):
    # when
    testing_value = log._filenamer(input_value)

    # then
    assert testing_value == expected_value, testing_value


sep = os.path.sep


@pytest.mark.parametrize(
    "input_value,expected_value",
    (
        args(
            input="\\refinitiv-data-lib.log",
            expected=f"{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input=".\\refinitiv-data-lib.log",
            expected="datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="..\\refinitiv-data-lib.log",
            expected=f"..{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="..\\..\\refinitiv-data-lib.log",
            expected=f"..{sep}..{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="\\..\\refinitiv-data-lib.log",
            expected=f"{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="path\\to\\refinitiv-data-lib.log",
            expected=f"path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input=".\\path\\to\\refinitiv-data-lib.log",
            expected=f"path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="..\\path\\to\\refinitiv-data-lib.log",
            expected=f"..{sep}path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="..\\..\\path\\to\\refinitiv-data-lib.log",
            expected=f"..{sep}..{sep}path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="\\..\\path\\to\\refinitiv-data-lib.log",
            expected=f"{sep}path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="C:\\path\\to\\refinitiv-data-lib.log",
            expected=f"C:{sep}path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="/refinitiv-data-lib.log",
            expected=f"{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="./refinitiv-data-lib.log",
            expected="datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="../refinitiv-data-lib.log",
            expected=f"..{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="../../refinitiv-data-lib.log",
            expected=f"..{sep}..{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="/../refinitiv-data-lib.log",
            expected=f"{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="path/to/refinitiv-data-lib.log",
            expected=f"path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="./path/to/refinitiv-data-lib.log",
            expected=f"path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="../path/to/refinitiv-data-lib.log",
            expected=f"..{sep}path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="../../path/to/refinitiv-data-lib.log",
            expected=f"..{sep}..{sep}path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="/../path/to/refinitiv-data-lib.log",
            expected=f"{sep}path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
        args(
            input="C:/path/to/refinitiv-data-lib.log",
            expected=f"C:{sep}path{sep}to{sep}datetime-datetime-pid-refinitiv-data-lib.log",
        ),
    ),
)
def test__get_filename(input_value, expected_value):
    # when
    testing_value = log._get_filename(input_value, stub_datetime, "pid")

    # then
    assert testing_value == expected_value, testing_value


def test_change_location_in_filename_for_log_file(tmp_path):
    import json

    # given
    test_message = "This is the test message."
    config = {
        "logs": {
            "transports": {
                "file": {
                    "enabled": True,
                    "name": f'{tmp_path / "refinitiv-data-lib.log"}',
                }
            }
        }
    }
    configpath = "refinitiv-data.config.json"
    with open(configpath, "w") as f:
        f.write(json.dumps(config))
        f.flush()

    from refinitiv.data import _configure as configure

    configure.reload()
    reload(log)

    # when
    logger = log.get_logger("location.logfile")
    logfilepath = logger.handlers[0].filename
    logger.warning(test_message)

    # then
    with open(logfilepath, "r") as f:
        logline = f.readline()

    assert test_message in logline

    # teardown
    log.dispose_logger(logger)
    os.remove(configpath)
