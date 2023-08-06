import allure
import pytest

import refinitiv.data as rd
from refinitiv.data.delivery import cfs
from tests.integration.delivery.cfs.file_downloader.conftest import (
    check_file_in_folder,
    check_file_in_working_folder,
)


@allure.suite("Delivery object - CFS File downloader")
@allure.feature("Delivery object - CFS File downloader")
@allure.severity(allure.severity_level.CRITICAL)
class TestCfsFileDownloader:
    @allure.title("Download and unzip file by specific path")
    @pytest.mark.caseid("36636830")
    @pytest.mark.parametrize(
        "download_path,unzip_path",
        [
            (r"linux_path_type/download_here", r"linux_path_type/unzip_here"),
            (r"windows_path_type\download_here", r"windows_path_type\unzip_here"),
        ],
    )
    def test_download_and_unzip_file_by_specific_path(
        self,
        get_smallest_file_from_bucket,
        open_platform_session,
        download_path,
        unzip_path,
    ):
        file = get_smallest_file_from_bucket

        file_downloader = cfs.file_downloader.Definition(file).retrieve()
        file_downloader.download(path=download_path)
        file_downloader.extract(path=unzip_path)

        check_file_in_folder(file["filename"].replace(":", ""), download_path)
        check_file_in_folder(file["filename"][:-3].replace(":", ""), unzip_path)

    @allure.title("Download file with closed session")
    @pytest.mark.caseid("36636833")
    def test_download_file_with_closed_session(self, get_smallest_file_from_bucket):
        file = get_smallest_file_from_bucket
        session = rd.session.desktop.Definition(app_key=" ").get_session()
        rd.session.set_default(session)

        with pytest.raises(
            ValueError, match="Session is not opened. Can't send any request"
        ):
            cfs.file_downloader.Definition(file).retrieve()

    @allure.title("Download and unzip file without path")
    @pytest.mark.caseid("36636832")
    def test_download_and_unzip_file_without_path(
        self, get_smallest_file_from_bucket, open_platform_session
    ):
        file = get_smallest_file_from_bucket

        file_downloader = cfs.file_downloader.Definition(file).retrieve()
        file_downloader.download()
        file_downloader.extract()

        check_file_in_working_folder(file["filename"].replace(":", ""))
