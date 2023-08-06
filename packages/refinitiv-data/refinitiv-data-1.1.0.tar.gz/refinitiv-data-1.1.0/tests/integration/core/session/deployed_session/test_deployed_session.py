import os

import allure
import pytest

import refinitiv.data as rd
import tests.integration.conftest as conf
from refinitiv.data._core.session import set_default
from refinitiv.data.session import platform
from tests.integration.core.session.conftest import assert_session_open_state

deployed_platform_host = os.getenv("DEPLOYED_PLATFORM_HOST")
deployed_platform_user_name = os.getenv("DEPLOYED_PLATFORM_USER_NAME")


@allure.suite("Session layer - Deployed session")
@allure.feature("Session layer - Deployed session")
@allure.severity(allure.severity_level.CRITICAL)
class TestDeployedSession:
    @allure.title(
        "Verify that Deployed Platform session opens with valid credentials and valid host"
    )
    @pytest.mark.caseid("C37691450")
    @pytest.mark.smoke
    def test_session_is_opened_and_is_closed_using_valid_credentials(self):
        session = platform.Definition(
            app_key=conf.desktop_app_key,
            deployed_platform_host=deployed_platform_host,
            deployed_platform_username=deployed_platform_user_name,
            dacs_application_id="256",
        ).get_session()
        set_default(session)
        session.open()

        assert_session_open_state(session)

    @allure.title(
        "Verify that deployed session is opened using config file and is closed after close"
    )
    @pytest.mark.caseid("C43104144")
    def test_session_opened_using_config_file_and_valid_credentials(
        self, load_config
    ):
        session = platform.Definition(name="deployed-cipsnylab2").get_session()
        set_default(session)
        session.open()

        assert_session_open_state(session)

    @allure.title(
        "Verify that deployed session is opened using config file on access layer"
    )
    @pytest.mark.caseid("C43104147")
    def test_session_opened_using_config_file_in_rd_open_session(
        self, load_config
    ):
        session = rd.open_session(name="platform.deployed-cipsnylab2")

        assert_session_open_state(session)
