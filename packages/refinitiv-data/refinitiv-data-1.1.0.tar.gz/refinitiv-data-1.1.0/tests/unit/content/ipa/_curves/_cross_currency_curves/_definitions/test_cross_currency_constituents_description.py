from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    CrossCurrencyConstituentsDescription,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FxForwardInstrumentDescription,
    FxSpotInstrumentDescription,
    CrossCurrencyInstrumentDescription,
)


def test_cross_currency_constituents_description():
    # given
    expected_dict = {
        "crossCurrencySwaps": [{}],
        "fxForwards": [{}],
        "fxSpot": {},
        "interestRateSwaps": [{}],
        "overnightIndexSwaps": [{}],
    }

    # when
    testing_obj = CrossCurrencyConstituentsDescription(
        cross_currency_swaps=[CrossCurrencyInstrumentDescription()],
        fx_forwards=[FxForwardInstrumentDescription()],
        fx_spot=FxSpotInstrumentDescription(),
        interest_rate_swaps=[CrossCurrencyInstrumentDescription()],
        overnight_index_swaps=[CrossCurrencyInstrumentDescription()],
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.cross_currency_swaps == [CrossCurrencyInstrumentDescription()]
    assert testing_obj.fx_forwards == [FxForwardInstrumentDescription()]
    assert testing_obj.fx_spot == FxSpotInstrumentDescription()
    assert testing_obj.interest_rate_swaps == [CrossCurrencyInstrumentDescription()]
    assert testing_obj.overnight_index_swaps == [CrossCurrencyInstrumentDescription()]
