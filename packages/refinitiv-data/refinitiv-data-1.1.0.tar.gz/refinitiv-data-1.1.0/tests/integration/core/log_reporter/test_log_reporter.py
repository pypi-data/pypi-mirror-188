import datetime
import logging
import logging.handlers
import os

import allure
import pytest

import refinitiv.data as rd
import refinitiv.data._log as rdp_logging


class Record(object):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


@allure.suite("Log reporter")
@allure.feature("Log reporter")
@allure.severity(allure.severity_level.CRITICAL)
class TestLogger:
    @allure.title("Total count of all rotated log files")
    @pytest.mark.caseid("")
    def test_total_count_of_all_rotated_log_files(
        self, enabled_log, open_desktop_session
    ):
        max_files = 2

        session = open_desktop_session
        rd.get_config().set_param(
            param=f"logs.transports.file.maxFiles", value=max_files
        )
        logger = session.logger()

        file_handler = None
        for hdlr in logger.handlers:
            if isinstance(hdlr, logging.handlers.RotatingFileHandler):
                file_handler = hdlr
                break

        for i in range(max_files):
            logger.error(f"error message {i}")
            file_handler.doRollover()

        filepath = rdp_logging._filenamer(file_handler.baseFilename + f".{max_files}")
        assert os.path.exists(filepath)

        filepath = rdp_logging._filenamer(
            file_handler.baseFilename + f".{max_files + 1}"
        )
        assert not os.path.exists(filepath)

    @allure.title("Logs are being written by the logger contain the module name")
    @pytest.mark.caseid("")
    def test_logs_are_being_written_by_the_logger_contain_the_module_name(
        self, enabled_log
    ):
        logger = rdp_logging.create_logger("session:desktop")
        logger.error("error message")
        logger.info("info message")
        now_ = datetime.datetime.now()
        date_ = now_.strftime("%Y-%m-%d")

        assert "session:desktop" in logger.name
        assert f"{date_}" in logger.root.root.handlers[2].records[0].asctime
        assert "ERROR" in logger.root.root.handlers[2].records[0].levelname
        assert "INFO" in logger.root.root.handlers[2].records[1].levelname

    @allure.title("All levels below or equal VALUE are logged")
    @pytest.mark.parametrize(
        "string_value,int_value",
        [
            ("trace", 5),
            ("debug", 10),
            ("info", 20),
            ("warn", 30),
            ("error", 40),
        ],
    )
    @pytest.mark.caseid(" ")
    def test_all_levels_below_or_equal_value_are_logged(
        self, string_value, int_value, enabled_log, open_desktop_session
    ):
        session = open_desktop_session
        session.set_log_level(int_value)

        log_levels = [(string_value, int_value)]
        value = rdp_logging.convert_log_level(string_value)

        logger = session.logger()
        levels_sum = 0
        target_levels_sum = 0
        start_to_sum = False
        for level_str, level_int in log_levels:
            log_level = rdp_logging.convert_log_level(level_int)
            logger.log(log_level, "log message")

            levels_sum += session.logger().level

            if log_level == value:
                start_to_sum = True

            if start_to_sum:
                target_levels_sum += log_level

        assert (
            target_levels_sum == levels_sum
        ), f"target: {target_levels_sum}, exists: {levels_sum}"

    @allure.title("Logs are not written at all")
    @pytest.mark.caseid("")
    def test_logs_are_not_written(self, enabled_log, open_platform_session):
        session = open_platform_session
        session.set_log_level("silent")
        logger = session.logger()
        logger.error("error message")

        assert len(logger.root.root.handlers[2].records) == 0

    @allure.title("Default log level is info")
    @pytest.mark.caseid("")
    def test_get_default_log_level(self, enabled_log, open_platform_session):
        session = open_platform_session
        logger = session.logger()
        logger.error("error message")
        logger.warning("warning message")
        logger.info("info message")
        logger.debug("debug message")

        assert logger.level == 20

    @allure.title("Date, time, and process ID are added to the log file name")
    @pytest.mark.caseid("")
    def test_date_time_process_id_are_added_to_the_log_file_name(
        self, enabled_log, open_desktop_session
    ):
        default_name = rd.get_config().get_param(param=f"logs.transports.file.name")
        logger = open_desktop_session.logger()
        logger.error("error message")

        filename = logger.handlers[0].filename
        date, time, process_id, *name = filename.split("-")
        name = "-".join(name)
        assert date and int(date)
        assert time and int(time)
        assert process_id and int(process_id)
        assert name == default_name

    @allure.title("Check log size")
    @pytest.mark.caseid("")
    def test_check_log_size(self, enabled_log, open_desktop_session):
        default_file_size = rd.get_config().get_param(
            param=f"logs.transports.file.size"
        )
        logger = open_desktop_session.logger()

        file_handler = None
        stream_handler = None
        for hdlr in logger.handlers:
            if isinstance(hdlr, logging.handlers.RotatingFileHandler):
                file_handler = hdlr
            if isinstance(hdlr, logging.StreamHandler):
                stream_handler = hdlr

        logger.removeHandler(stream_handler)

        expected_filesize = rdp_logging.convert_filesize(default_file_size)
        max_bytes = file_handler.maxBytes

        start = 0
        stop = expected_filesize // 100
        for i in range(start, stop + 1):
            logger.info("a" * 30)

        filepath = rdp_logging._filenamer(file_handler.baseFilename + ".1")
        filesize = os.path.getsize(filepath)

        assert expected_filesize == max_bytes, max_bytes
        assert filesize <= expected_filesize, f"Actual file size: {filesize}"
        assert default_file_size == "10M", default_file_size
        open_desktop_session.close()

    @allure.title("Only those logs that matched by filter are written")
    @pytest.mark.parametrize(
        "value,record",
        [
            ("session*,module:b,module:c", "module:c"),
            ("*,-module:a", "module:b"),
            ("module:*,-module:b,-module:c", "module:a"),
        ],
    )
    @pytest.mark.caseid("")
    def test_only_those_logs_that_matched_by_filter_are_written(
        self, value, record, enabled_log
    ):
        rd.get_config().set_param(param=f"logs.filter", value=value)
        filterer = rdp_logging.make_filter(value)
        record = Record(record)
        result = filterer(record)
        assert result, f"record={record.name}, filter_by={value}"
