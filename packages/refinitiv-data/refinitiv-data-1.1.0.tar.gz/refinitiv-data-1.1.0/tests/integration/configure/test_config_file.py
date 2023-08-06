import os

import allure
import pytest

import refinitiv.data as rd
from refinitiv.data import _configure as configure
from tests.integration.configure.conftest import open_session_and_get_base_url
from tests.integration.helpers import compare_list

BASE_URL_BETA = "https://api.ppe.refinitiv.com"
BASE_URL_PROD = "https://api.refinitiv.com"
ENV_NAME = os.environ.get("ENV_NAME")


@allure.suite("Configuration file")
@allure.feature("Configuration file")
@allure.severity(allure.severity_level.CRITICAL)
class TestConfigFile:
    @allure.title("Check default base url for desktop session")
    @pytest.mark.caseid("37655144")
    def test_default_base_url_for_desktop_session(self, open_desktop_session):
        session = open_desktop_session
        base_url = session._get_base_url()
        expected_url = ["http://localhost:9000", "http://localhost:9001", "http://localhost:9060"]
        assert base_url in expected_url, f"Actual url: {base_url}"

    @allure.title("Check default base url for platform session")
    @pytest.mark.caseid("37655149")
    def test_default_base_url_for_platform_session(self, open_platform_session):
        session = open_platform_session
        base_url = session._base_url

        expected_url = None
        if ENV_NAME == "PROD":
            expected_url = BASE_URL_PROD
        elif ENV_NAME == "BETA":
            expected_url = BASE_URL_BETA

        assert expected_url == base_url, f"Actual url: {base_url}"

    @allure.title("Override default pricing endpoint")
    @pytest.mark.caseid("37655231")
    def test_override_default_pricing_endpoint(self):
        test_endpoint = "/test"
        rd.get_config().set_param(
            param=f"apis.data.pricing.endpoints", value=test_endpoint
        )
        actual_endpoint = rd.get_config().get_param(
            param=f"apis.data.pricing.endpoints"
        )

        assert actual_endpoint == test_endpoint, f"{actual_endpoint} != {test_endpoint}"

    @allure.title("Check default ownership Fund Top-n-Concentration url")
    @pytest.mark.caseid("37655273")
    def test_default_ownership_fund_top_n_concentration_url(
        self, open_platform_session
    ):
        response = rd.content.ownership.fund.top_n_concentration.Definition(
            universe="ONEX.CCP", count=5
        ).get_data()
        url = response.request_message.url.path
        expected_url = rd.get_config().get_param(
            param=f"apis.data.ownership.endpoints.fund.top-n-concentration"
        )
        assert expected_url in url, f"Actual url: {url}"

    @allure.title("Check keys from config file at first level")
    @pytest.mark.caseid("37655346")
    def test_keys_from_config_file_on_first_level(self):
        configure.reload()
        actual_keys = rd.get_config().keys(1)
        expected_keys = [
            "raise_exception_on_error",
            "apis",
            "http",
            "config-change-notifications-enabled",
            "sessions",
            "logs",
            "bulk",
            'usage_logger'
        ]

        compare_list(actual_keys, expected_keys)

    @allure.title("Open two sessions and load different config file for every session")
    @pytest.mark.caseid("37691516")
    def test_open_two_session_and_load_diff_config_file_for_every_session(self):
        rd.load_config("./tests/integration/configure/beta-config.json")
        session = rd.session.platform.Definition(name="my-session").get_session()
        base_url = open_session_and_get_base_url(session)
        expected_url = BASE_URL_BETA

        assert expected_url == base_url, f"Actual url: {base_url}"

        rd.load_config("./tests/integration/configure/refinitiv-data.config.json")
        session = rd.session.platform.Definition(name="my-test-session").get_session()
        base_url = open_session_and_get_base_url(session)
        expected_url = BASE_URL_PROD

        assert expected_url == base_url, f"Actual url: {base_url}"
