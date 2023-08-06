from datetime import datetime, timedelta

import allure
import pytest

import refinitiv.data.eikon as ek
from refinitiv.data.errors import RDError
from tests.integration.eikon.time_series.conftest import (
    check_dataframe_contains_ohlc_columns_and_rics,
)


@allure.suite("Eikon Legacy module - Timeseries")
@allure.feature("Eikon Legacy module - Timeseries")
@allure.severity(allure.severity_level.NORMAL)
class TestTimeSeries:
    @allure.title("Get timeseries with single ric")
    @pytest.mark.caseid("38427366")
    @pytest.mark.parametrize("ric", ["VOD.L"])
    @pytest.mark.smoke
    def test_get_timeseries_with_single_ric(self, setup_app_key, ric):
        df = ek.get_timeseries(ric)
        assert not df.empty, "Empty dataframe received"
        assert df.columns.name == ric
        assert df.columns.array == ["HIGH", "LOW", "OPEN", "CLOSE", "COUNT", "VOLUME"]

    @allure.title("Get timeseries with optional parameters")
    @pytest.mark.caseid("38427367")
    @pytest.mark.parametrize(
        "ric,start_date,end_date,interval",
        [
            (
                ["VOD.L", "LSEG.L"],
                timedelta(-10),
                timedelta(0),
                "daily",
            ),
            (
                "VOD.L",
                timedelta(-180),
                datetime.now(),
                "monthly",
            ),
        ],
    )
    def test_get_timeseries_with_optional_parameters(
        self, setup_app_key, ric, start_date, end_date, interval
    ):
        df = ek.get_timeseries(
            ric, start_date=start_date, end_date=end_date, interval=interval
        )
        assert not df.empty, "Empty dataframe received"
        check_dataframe_contains_ohlc_columns_and_rics(df, ric)

    @allure.title("Get timeseries with invalid ric")
    @pytest.mark.caseid("38427368")
    @pytest.mark.parametrize("ric", ["invalid_ric"])
    def test_get_timeseries_with_invalid_ric(self, setup_app_key, ric):
        with pytest.raises(RDError, match="Error code Error | INVALID: Invalid RIC |"):
            ek.get_timeseries(ric)
