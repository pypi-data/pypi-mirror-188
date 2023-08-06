import os

import pytest

import refinitiv.data as rd
from refinitiv.data.delivery import cfs
from tests.integration.conftest import create_platform_session


def check_file_in_folder(file_name, path_to_folder):
    files_list = os.listdir(path_to_folder)
    assert len(files_list) == 1
    assert file_name in files_list
    size = os.stat(os.path.join(path_to_folder, files_list[0])).st_size
    assert size > 0, f"File size == 0 for file {file_name}"


def check_file_in_working_folder(file_name):
    files_list = os.listdir(r"./")
    assert file_name in files_list
    file = list(filter(lambda file: file == file_name, files_list))[0]
    assert os.stat(file).st_size > 0, f"File size == 0 for file {file_name}"


@pytest.fixture(scope="module", autouse=True)
def get_smallest_file_from_bucket():
    session = create_platform_session()
    session.open()
    rd.session.set_default(session)

    response = cfs.file_sets.Definition(bucket="bulk-ESG", page_size=5).get_data()
    result = []
    for fileset in response.data.file_sets:
        for file in fileset:
            result.append(file)
    sorted_files = list(sorted(result, key=lambda file: file.file_size_in_bytes))
    first_file_set_id = sorted_files[0].fileset_id

    first_smallest_files = cfs.files.Definition(first_file_set_id).get_data()
    session.close()

    return first_smallest_files.data.files[0]
