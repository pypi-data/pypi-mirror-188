from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FxSpotInstrumentDescription,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    BidAskFieldsDescription,
    FormulaParameterDescription,
    FxSpotInstrumentDefinition,
)


def test_fx_forward_instrument_description():
    # given
    expected_dict = {
        "fields": {},
        "formula": "string",
        "formulaParameters": [{}],
        "instrumentDefinition": {},
    }

    # when
    testing_obj = FxSpotInstrumentDescription(
        fields=BidAskFieldsDescription(),
        formula_parameters=[FormulaParameterDescription()],
        instrument_definition=FxSpotInstrumentDefinition(),
        formula="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.fields == BidAskFieldsDescription()
    assert testing_obj.formula_parameters == [FormulaParameterDescription()]
    assert testing_obj.instrument_definition == FxSpotInstrumentDefinition()
    assert testing_obj.formula == "string"
