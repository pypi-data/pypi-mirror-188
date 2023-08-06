import allure
import pytest

from refinitiv.data.content import custom_instruments as ci
from refinitiv.data.errors import RDError
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.content.custom_instruments.conftest import (
    instrument_data,
    new_instrument_data,
    get_holidays,
)
from tests.integration.helpers import (
    check_response_status,
    check_non_empty_response_data,
)


@allure.suite("Content object - Custom Instrument")
@allure.feature("Formula Custom Instrument")
@allure.severity(allure.severity_level.CRITICAL)
class TestFormulaCustomInstrument:
    @allure.title("Retrieve the data of created Custom Instrument objects")
    @pytest.mark.caseid("C42995813")
    def test_get_data_of_custom_instrument_objects(
        self, open_session_with_rdp_creds_for_ci, create_instrument
    ):
        symbol = create_instrument()
        response = ci.search.Definition().get_data()
        check_response_status(
            response,
            expected_status_code=HttpStatusCode.TWO_HUNDRED,
            expected_http_reason=HttpReason.OK,
        )
        check_non_empty_response_data(response)
        assert any(
            symbol in universe for universe in response.data.df.get("symbol")
        ), f"There is no created CI symbol on server"

    @allure.title("Create formula Custom Instrument object")
    @pytest.mark.caseid("")
    @pytest.mark.parametrize(
        "formula, expected_holidays",
        [
            (
                "VOD.L + LSEG.L",
                [
                    {"date": "2022-09-01", "reason": "Knowledge Day"},
                    {"date": "2022-12-18", "reason": "Hanukkah"},
                ],
            )
        ],
    )
    def test_create_formula_custom_instrument(
        self, open_session_with_rdp_creds_for_ci, symbol, formula, expected_holidays
    ):
        dates_and_calendars_holiday = get_holidays(
            session=open_session_with_rdp_creds_for_ci
        )
        expected_holidays.append(
            {
                "date": dates_and_calendars_holiday.date,
                "reason": dates_and_calendars_holiday.name,
            }
        )

        cust_inst = ci.manage.create_formula(
            **instrument_data,
            symbol=symbol,
            formula=formula,
            holidays=[
                ci.manage.Holiday(date="2022-09-01", name="Knowledge Day"),
                {"date": "2022-12-18", "reason": "Hanukkah"},
                dates_and_calendars_holiday,
            ],
        )

        for param, value in instrument_data.items():
            assert (
                cust_inst.__getattribute__(param) == value
            ), f"Attribute {param} was not created for {symbol}"
        assert (
            symbol in cust_inst.symbol
        ), f"Created symbol is not the same as requested"
        assert cust_inst.holidays == expected_holidays

        ci.manage.delete(symbol)

    @allure.title("Update formula Custom Instrument object with params")
    @pytest.mark.caseid("C42995815")
    @pytest.mark.parametrize(
        "formula, expected_holidays",
        [
            (
                "VOD.L + LSEG.L",
                [
                    {"date": "2022-09-01", "reason": "Knowledge Day"},
                    {"date": "2022-12-18", "reason": "Hanukkah"},
                ],
            )
        ],
    )
    def test_update_formula_custom_instrument_object_with_params(
        self,
        open_session_with_rdp_creds_for_ci,
        create_instrument,
        formula,
        expected_holidays,
    ):
        symbol = create_instrument()
        cust_inst = ci.manage.get(symbol)

        cust_inst.formula = formula
        cust_inst.holidays = expected_holidays

        for param, value in new_instrument_data.items():
            cust_inst.__setattr__(param, value)
        cust_inst.save()

        updated_instrument = ci.manage.get(universe=symbol)

        for param, value in new_instrument_data.items():
            assert (
                updated_instrument.__getattribute__(param) == value
            ), f"Attribute {param} was not updated  for {symbol}"
        assert updated_instrument.formula == formula
        assert updated_instrument.holidays == [
            {"date": "2022-09-01", "reason": "Knowledge Day"},
            {"date": "2022-12-18", "reason": "Hanukkah"},
        ]

    @allure.title(
        "Delete Custom Instrument object and get error for retrieving removed one"
    )
    @pytest.mark.caseid("C42995816")
    def test_delete_custom_instrument_object(
        self, open_session_with_rdp_creds_for_ci, create_instrument
    ):
        symbol = create_instrument()
        ci.manage.delete(symbol)
        with pytest.raises(RDError) as error:
            ci.manage.get(symbol)
        assert (
            str(error.value)
            == f'Error code 404 | CustomInstrument not found: CustomInstrument with "symbol":"{symbol}" not found'
        )

    @allure.title("Create Custom Instrument object with extended params")
    @pytest.mark.parametrize(
        "formula,instrument_params,extended_params",
        [
            (
                "GBP=*3",
                [
                    "description",
                    "exchange_name",
                    "instrument_name",
                    "time_zone",
                    "currency",
                ],
                {
                    "description": "Glory tale about instrument",
                    "exchangeName": "8080",
                    "instrumentName": "Trading St. tool",
                    "timeZone": "LON",
                    "currency": "GBP",
                },
            )
        ],
    )
    @pytest.mark.caseid("C43999085")
    def test_create_custom_instrument_with_extended_params(
        self,
        open_session_with_rdp_creds_for_ci,
        symbol,
        formula,
        instrument_params,
        extended_params,
    ):
        cust_inst = ci.manage.create(
            symbol=symbol, formula=formula, extended_params=extended_params
        )
        for param_key, extended_key in zip(instrument_params, extended_params):
            assert (
                cust_inst.__getattribute__(param_key) == extended_params[extended_key]
            ), f"Attribute {param_key} was not created  for {symbol}"
