import allure
import pytest

import refinitiv.data as rd
import tests.integration.conftest as global_conftest
from tests.integration.access.conftest import check_session_state


@allure.suite("FinCoder layer")
@allure.feature("FinCoder - Session")
@allure.severity(allure.severity_level.CRITICAL)
class TestSession:
    @allure.title("Open, close default session and check session status")
    @pytest.mark.caseid("36971083")
    def test_open_and_close_default_session(self, load_config):
        session = rd.open_session()
        check_session_state(session)

    @allure.title(
        "Open, close default session with specific config file and check session status"
    )
    @pytest.mark.caseid("36971084")
    def test_open_and_close_default_session_with_specific_config_file(self):
        session = rd.open_session(config_name=global_conftest.conf)
        check_session_state(session)

    @allure.title(
        "Open, close specific session with specific config file and check session status"
    )
    @pytest.mark.caseid("36971085")
    def test_open_and_close_specific_session_with_specific_config_file(self):
        session = rd.open_session(
            name="platform.my-session", config_name=global_conftest.conf
        )
        check_session_state(session)

    @allure.title("Open, close session when put only app key and check session status")
    @pytest.mark.caseid("36971346")
    def test_open_and_close_when_put_app_key(self):
        session = rd.open_session(app_key=global_conftest.desktop_app_key)
        check_session_state(session)

    @allure.title("Open, close session with all params and check session status")
    @pytest.mark.caseid("36971350")
    def test_open_and_close_with_all_params(self):
        session = rd.open_session(
            name="desktop.my-session",
            app_key=global_conftest.desktop_app_key,
            config_name=global_conftest.conf,
        )
        check_session_state(session)

    @allure.title(
        "Open, close session with specific session name and check session status"
    )
    @pytest.mark.caseid("36971570")
    def test_open_and_close_with_specific_session_name(self, load_config):
        session = rd.open_session("desktop.my-session")
        check_session_state(session)

    @allure.title("Open session with invalid session name")
    @pytest.mark.caseid("36971742")
    def test_open_with_invalid_session_name(self, load_config):
        with pytest.raises(
            NameError, match="Cannot open session desktop.custom-session"
        ):
            rd.open_session("desktop.custom-session")

    @allure.title("Open session with invalid config path")
    @pytest.mark.caseid("36971748")
    def test_open_with_invalid_config_path(self):
        with pytest.raises(FileNotFoundError, match="Can't find file:"):
            rd.open_session(config_name="./path/to/fin-coder-prod.json")
