import os

from tests.integration.constants_list import HttpStatusCode


def check_file_downloaded_response(response, expected_file_name):
    actual_file_name = response.data.files[0].file_location
    status_code = response.data.files[0].raw["status_code"]
    is_success = response.data.files[0].is_success

    assert is_success
    assert status_code == HttpStatusCode.TWO_HUNDRED
    assert (
        expected_file_name in actual_file_name
    ), f"actual file name is {actual_file_name}"


def check_file_is_downloaded(filename):
    for root, dirs, files in os.walk("./"):
        for file in files:
            if file.startswith(filename):
                assert True, f"File {filename} not found"
                os.remove(file)
                break


def get_callback(callback_response):
    status_code = callback_response.data.files[0].raw["status_code"]
    assert status_code == HttpStatusCode.TWO_HUNDRED
