import fnmatch
import json
import logging
import os
import sqlite3

import refinitiv.data as rd


def find_all_files_by_pattern(pattern, path):
    results = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                results.append(os.path.join(root, name))
    return results


def delete_file_by_path(path):
    if os.path.exists(path):
        try:
            os.remove(path)
            logging.info("Deleted file: " + path)
        except PermissionError as err:
            logging.error("No permissions to delete the file: " + path)
            logging.error(err)
    else:
        logging.info("File does not exist: " + path)


def check_folder_contains_init_and_delta_files(path):
    files = find_all_files_by_pattern("*jsonl.gz", path)
    assert len(files) >= 2
    assert list_of_strings_contains_pattern(files, "*Init*")
    assert list_of_strings_contains_pattern(files, "*Delta*")


def list_of_strings_contains_pattern(strings_list, pattern):
    for string in strings_list:
        if fnmatch.fnmatch(string, pattern):
            return True
    return False


def parse_file_to_array_of_strings(filepath):
    text_file = open(filepath, "r")
    lines = text_file.readlines()
    text_file.close()
    return lines


def parse_file_to_array_of_dicts(filepath):
    list_of_strings = parse_file_to_array_of_strings(filepath)
    return list(map(lambda string: json.loads(string), list_of_strings))


def check_log_file_has_success_download_lines(path):
    files = find_all_files_by_pattern("*jsonl.gz", path)
    logfile_lines = parse_file_to_array_of_dicts(os.path.join(path, "log.txt"))
    downloaded_files_from_logfile = list(
        filter(lambda line: line["action"] == "DOWNLOAD", logfile_lines)
    )
    downloaded_filenames = list(
        map(lambda dict: dict["details"]["filename"], downloaded_files_from_logfile)
    )
    for file in files:
        assert (
            os.path.basename(file) in downloaded_filenames
        ), f"the line for file download not found in the logfile. {file}. Logfile lines: {logfile_lines}"


def check_log_file_has_success_extract_lines(path):
    files = find_all_files_by_pattern("*jsonl", path)
    logfile_lines = parse_file_to_array_of_dicts(os.path.join(path, "log.txt"))
    extracted_files_from_logfile = list(
        filter(lambda line: line["action"] == "EXTRACT", logfile_lines)
    )
    extracted_filenames = list(
        map(lambda dict: dict["details"]["filename"], extracted_files_from_logfile)
    )
    for file in files:
        assert (
            os.path.basename(file) in extracted_filenames
        ), f"the line for file extract not found in the logfile. {file}. Logfile lines: {logfile_lines}"


def check_downloads_folder(path):
    assert os.path.exists(path), f"The expected path {path} does not exist"
    assert os.path.isdir(path), f"Not a folder: {path}"
    assert len(os.listdir(path)) != 0, f"Folder is empty: {path}"


def check_log_file_has_no_extract_lines(path):
    logfile_lines = parse_file_to_array_of_dicts(os.path.join(path, "log.txt"))
    extracted_files_from_logfile = list(
        filter(lambda line: line["action"] == "EXTRACT", logfile_lines)
    )
    assert (
        len(extracted_files_from_logfile) == 0
    ), f"Found lines about file extraction in the logfile: {extracted_files_from_logfile}"


def check_sqlite_db_data():
    conn = sqlite3.connect("db.sqlite", uri=True)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()[0][0]
    expected_table_name = rd.get_config().get_param(
        "bulk.esg.standard_scores.db.create-table-queries"
    )[0]["table-name"]
    assert (
        table_name == expected_table_name
    ), f"Invalid table name was created in sqlite db: {table_name}, expected: {expected_table_name}"
    cursor.execute(f"SELECT * FROM {table_name};")
    table_lines = cursor.fetchall()
    assert len(table_lines) > 0, f"Empty data retrieved from sqlite table"


def check_sqlite_db_is_empty():
    conn = sqlite3.connect("db.sqlite", uri=True)
    cursor = conn.cursor()
    configured_table_name = rd.get_config().get_param(
        "bulk.esg.standard_scores.db.create-table-queries"
    )[0]["table-name"]
    cursor.execute(f"SELECT * FROM {configured_table_name};")
    table_lines = cursor.fetchall()
    assert len(table_lines) == 0, f"Sqlite table {configured_table_name} is not empty"


def check_folder_cleaned_up(path):
    JENKINS_SERVICE_FILES_PATTERN = ".nfs"
    list_of_files_in_folder = os.listdir(path)
    filtered_list = list(
        filter(
            lambda x: not x.startswith(JENKINS_SERVICE_FILES_PATTERN),
            list_of_files_in_folder,
        )
    )
    assert len(filtered_list) == 0 or (
        len(filtered_list) == 1 and filtered_list[0] == "log.txt"
    ), f"Folder {path} is not  empty: {list_of_files_in_folder}, list of filtered files is: {filtered_list}"
