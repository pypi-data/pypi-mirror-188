import allure
import pytest

from refinitiv.data.content import custom_instruments as ci
from tests.integration.content.custom_instruments.conftest import (
    instrument_data,
    new_instrument_data,
    get_holidays,
)

basket_dict = {
    "constituents": [
        {"ric": "IBM.N", "weight": 20},
        {"ric": "EPAM.N", "weight": 80},
    ],
    "normalizeByWeight": True,
}

basket_obj = ci.manage.Basket(
    constituents=[
        ci.manage.Constituent(ric="IBM.N", weight=20),
        ci.manage.Constituent(ric="EPAM.N", weight=80),
    ],
    normalize_by_weight=True,
)

new_basket_obj = ci.manage.Basket(
    constituents=[
        ci.manage.Constituent(ric="LSEG.L", weight=50),
        ci.manage.Constituent(ric="VOD.L", weight=30),
        ci.manage.Constituent(ric="MSFT.O", weight=20),
    ],
    normalize_by_weight=False,
)


@allure.suite("Content object - Custom Instrument")
@allure.feature("Basket Custom Instrument")
@allure.severity(allure.severity_level.CRITICAL)
class TestBasketCustomInstrument:
    @allure.title("Create basket Custom Instrument object")
    @pytest.mark.caseid("")
    @pytest.mark.parametrize(
        "basket",
        [
            (basket_dict),
            (basket_obj),
        ],
    )
    def test_create_basket_custom_instrument(
        self, open_session_with_rdp_creds_for_ci, symbol, basket
    ):
        dates_and_calendars_holiday = get_holidays(
            session=open_session_with_rdp_creds_for_ci
        )
        expected_holidays = [
            {"date": "2022-09-01", "reason": "Knowledge Day"},
            {"date": "2022-12-18", "reason": "Hanukkah"},
            {
                "date": dates_and_calendars_holiday.date,
                "reason": dates_and_calendars_holiday.name,
            },
        ]

        cust_inst = ci.manage.create_basket(
            **instrument_data,
            symbol=symbol,
            basket=basket,
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
        assert cust_inst.basket == basket_obj

        ci.manage.delete(symbol)

    @allure.title("Update Basket Custom Instrument object with params")
    @pytest.mark.caseid("")
    def test_update_basket_custom_instrument(
        self, open_session_with_rdp_creds_for_ci, symbol
    ):
        cust_inst = ci.manage.create_basket(
            **instrument_data, symbol=symbol, basket=basket_dict
        )

        for param, value in new_instrument_data.items():
            cust_inst.__setattr__(param, value)
        cust_inst.basket = new_basket_obj
        cust_inst.save()

        updated_instrument = ci.manage.get(universe=symbol)

        for param, value in new_instrument_data.items():
            assert (
                updated_instrument.__getattribute__(param) == value
            ), f"Attribute {param} was not updated  for {symbol}"
        assert (
            cust_inst.basket == new_basket_obj
        ), f"Changes to Basket obj is not updated"

        ci.manage.delete(symbol)
