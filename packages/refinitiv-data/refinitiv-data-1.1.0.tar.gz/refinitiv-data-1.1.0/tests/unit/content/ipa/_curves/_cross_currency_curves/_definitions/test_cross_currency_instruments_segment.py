from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    CrossCurrencyInstrumentsSegment,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    CrossCurrencyConstituentsDescription,
    CrossCurrencyCurveParameters,
)


def test_cross_currency_instruments_segment():
    # given
    expected_dict = {"startDate": "string", "constituents": {}, "curveParameters": {}}

    # when
    testing_obj = CrossCurrencyInstrumentsSegment(
        start_date="string",
        constituents=CrossCurrencyConstituentsDescription(),
        curve_parameters=CrossCurrencyCurveParameters(),
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.start_date == "string"
    assert testing_obj.constituents == CrossCurrencyConstituentsDescription()
    assert testing_obj.curve_parameters == CrossCurrencyCurveParameters()
