import allure
import numpy
import pytest

from refinitiv.data.content import custom_instruments as ci
from refinitiv.data.content.custom_instruments import SpreadAdjustmentMethod
from tests.integration.content.custom_instruments.conftest import (
    instrument_data,
    new_instrument_data,
    volume_based_udc,
    day_based_udc,
    manual_udc,
    new_day_based_udc,
)


@allure.suite("Content object - Custom Instrument")
@allure.feature("UDC Custom Instrument")
@allure.severity(allure.severity_level.CRITICAL)
class TestUDCCustomInstrument:
    @allure.title("Create UDC Custom Instrument")
    @pytest.mark.caseid("")
    @pytest.mark.parametrize(
        "udc",
        [volume_based_udc, day_based_udc, manual_udc],
        ids=["volume_based_udc", "day_based_udc", "manual_udc"],
    )
    def test_create_udc_custom_instrument(
        self,
        request,
        open_session_with_rdp_creds_for_ci,
        symbol,
        udc,
    ):
        cust_inst = ci.manage.create_udc(**instrument_data, symbol=symbol, udc=udc)

        for param, value in instrument_data.items():
            assert (
                cust_inst.__getattribute__(param) == value
            ), f"Attribute {param} was not created for {symbol}"
        assert (
            symbol in cust_inst.symbol
        ), f"Created symbol is not the same as requested"

        if "manual_udc" in request.node.callspec.id:
            for item in cust_inst.udc.rollover.manual_items:
                assert isinstance(item.year, int)
                assert isinstance(item.month, int)
                assert isinstance(item.start_date, numpy.datetime64)
            assert (
                cust_inst.udc.spread_adjustment.method
                == SpreadAdjustmentMethod.CLOSE_TO_CLOSE
            )
        else:
            assert (
                cust_inst.__getattribute__("udc") == udc
            ), "There is difference with UDC parameters"

        ci.manage.delete(symbol)

    @allure.title("Update UDC Custom Instrument objects with params")
    @pytest.mark.caseid("C42995815")
    @pytest.mark.parametrize(
        "udc,new_udc",
        [(day_based_udc, new_day_based_udc)],
    )
    def test_update_udc_custom_instrument(
        self, open_session_with_rdp_creds_for_ci, symbol, udc, new_udc
    ):
        cust_inst = ci.manage.create_udc(**instrument_data, symbol=symbol, udc=udc)

        for param, value in new_instrument_data.items():
            cust_inst.__setattr__(param, value)
        cust_inst.udc = new_udc
        cust_inst.save()

        updated_instrument = ci.manage.get(universe=symbol)

        for param, value in new_instrument_data.items():
            assert (
                updated_instrument.__getattribute__(param) == value
            ), f"Attribute {param} was not updated  for {symbol}"
        assert cust_inst.udc == new_udc, f"UDC object isn't updated"
        ci.manage.delete(symbol)
