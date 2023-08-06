from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    CrossCurrencyInstrumentDescription,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    BidAskFieldsDescription,
    FormulaParameterDescription,
    CrossCurrencyInstrumentDefinition,
)


def test_cross_currency_instrument_description():
    # given
    expected_dict = {
        "fields": {},
        "formula": "string",
        "formulaParameters": [{}],
        "instrumentDefinition": {},
    }

    # when
    testing_obj = CrossCurrencyInstrumentDescription(
        fields=BidAskFieldsDescription(),
        formula_parameters=[FormulaParameterDescription()],
        instrument_definition=CrossCurrencyInstrumentDefinition(),
        formula="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.fields == BidAskFieldsDescription()
    assert testing_obj.formula_parameters == [FormulaParameterDescription()]
    assert testing_obj.instrument_definition == CrossCurrencyInstrumentDefinition()
    assert testing_obj.formula == "string"
