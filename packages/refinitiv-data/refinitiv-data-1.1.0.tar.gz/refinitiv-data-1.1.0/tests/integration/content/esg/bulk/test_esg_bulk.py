import os

import allure
import pytest

import refinitiv.data as rd
from refinitiv.data.content import esg
from refinitiv.data.content.esg import bulk
from tests.integration.content.esg.bulk.helpers import (
    check_folder_contains_init_and_delta_files,
    check_log_file_has_success_download_lines,
    check_log_file_has_success_extract_lines,
    check_log_file_has_no_extract_lines,
    check_downloads_folder,
    check_sqlite_db_data,
    check_folder_cleaned_up,
    check_sqlite_db_is_empty,
)

path = rd.get_config().get("bulk.esg.standard_scores.package.download.path")


@allure.suite("ESG Bulk")
@allure.feature("ESG Bulk")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("esg")
class TestEsgBulk:
    @allure.title(
        "Download all files (init + delta) to folder which does not exist - relative path"
    )
    @pytest.mark.caseid("35564218")
    @pytest.mark.xdist_group(name="esg_group")
    def test_download_all_files_to_folder_which_does_not_exist_relative_path(
        self,
        load_config,
        prepare_file_manager_and_clean_old_files,
        open_platform_session,
    ):
        file_manager = prepare_file_manager_and_clean_old_files
        file_manager.update_files()
        check_downloads_folder(path)
        check_folder_contains_init_and_delta_files(path)
        check_log_file_has_success_download_lines(path)
        check_log_file_has_success_extract_lines(path)

    @allure.title(
        "Update db when local db is empty and init+delta files are already downloaded & unzipped"
    )
    @pytest.mark.caseid("35776180")
    @pytest.mark.dependency(
        depends=["test_download_all_files_to_folder_which_does_not_exist_relative_path"]
    )
    @pytest.mark.xdist_group(name="esg_group")
    def test_update_db_when_local_db_is_empty_and_init_and_delta_files_unzipped(
        self,
        load_config,
        open_platform_session,
    ):
        file_manager = bulk.PackageManager("esg.standard_scores")
        if not os.path.exists(path) or len(os.listdir(path)) == 0:
            file_manager.update_files()
        file_manager.update_db()
        check_sqlite_db_data()

    @allure.title("Get data from db when db is populated")
    @pytest.mark.caseid("35776180")
    @pytest.mark.dependency(
        depends=[
            "test_update_db_when_local_db_is_empty_and_init_and_delta_files_unzipped"
        ]
    )
    @pytest.mark.xdist_group(name="esg_group")
    def test_get_db_data_when_db_is_populated(self, load_config):
        response = esg.standard_scores.Definition(universe="5000268022").get_db_data()
        assert response.data.raw, f"Empty response.data.raw received"
        assert not response.data.df.empty, f"Empty response.data.df received"

    @allure.title("Cleanup db when db contains data")
    @pytest.mark.caseid("36865382")
    @pytest.mark.dependency(
        depends=[
            "test_update_db_when_local_db_is_empty_and_init_and_delta_files_unzipped"
        ]
    )
    @pytest.mark.xdist_group(name="esg_group")
    def test_clean_up_db_when_db_contains_data(self, load_config):
        file_manager = bulk.PackageManager("esg.standard_scores")
        file_manager.cleanup_db()
        check_sqlite_db_is_empty()

    @allure.title("Reset files when downloads folder contains previous files")
    @pytest.mark.caseid("36865099")
    @pytest.mark.dependency(
        depends=["test_download_all_files_to_folder_which_does_not_exist_relative_path"]
    )
    @pytest.mark.xdist_group(name="esg_group")
    def test_reset_files_when_downloads_folder_contains_previous_files(
        self,
        load_config,
        open_platform_session,
    ):
        file_manager = bulk.PackageManager("esg.standard_scores")
        file_manager.reset_files()
        check_downloads_folder(path)
        check_folder_contains_init_and_delta_files(path)
        check_log_file_has_success_download_lines(path)
        check_log_file_has_success_extract_lines(path)

    @allure.title("Download files with auto-extract = false")
    @pytest.mark.caseid("35565422")
    @pytest.mark.xdist_group(name="esg_group")
    def test_download_all_files_with_auto_extract_false(
        self,
        load_config,
        set_auto_extract_to_false,
        prepare_file_manager_and_clean_old_files,
        open_platform_session,
    ):
        file_manager = prepare_file_manager_and_clean_old_files
        file_manager.update_files()
        check_downloads_folder(path)
        check_folder_contains_init_and_delta_files(path)
        check_log_file_has_success_download_lines(path)
        check_log_file_has_no_extract_lines(path)

    @allure.title("Update db when no init file was downloaded -> exception raised")
    @pytest.mark.caseid("35776181")
    @pytest.mark.xdist_group(name="esg_group")
    def test_update_db_when_no_init_file_was_downloaded(
        self, load_config, prepare_file_manager_and_clean_old_files
    ):
        file_manager = prepare_file_manager_and_clean_old_files
        with pytest.raises(FileNotFoundError):
            file_manager.update_db()

    @allure.title("Clean-up files when files were downloaded")
    @pytest.mark.caseid("36397732")
    @pytest.mark.xdist_group(name="esg_group")
    def test_cleanup_files_when_files_were_downloaded(self):
        file_manager = bulk.PackageManager("esg.standard_scores")
        if not os.path.exists(path) or len(os.listdir(path)) == 0:
            file_manager.update_files()
        file_manager.cleanup_files()
        check_folder_cleaned_up(path)
