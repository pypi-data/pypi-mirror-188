import pytest

import refinitiv.data as rd
import refinitiv.data.content.esg.bulk as bulk


@pytest.fixture(scope="function", autouse=False)
def prepare_file_manager_and_clean_old_files():
    file_manager = bulk.PackageManager("esg.standard_scores")
    file_manager.cleanup_files()
    yield file_manager


@pytest.fixture(scope="function", autouse=False)
def set_auto_extract_to_false():
    rd.get_config().set_param(
            param=f"bulk.esg.standard_scores.package.download.auto-extract",
            value=False,
            auto_create=True,
        )
