from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FormulaParameterDescription,
)
from refinitiv.data.content.ipa._curves._enums import InstrumentType
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    BidAskFieldsFormulaDescription,
)


def test_formula_parameter_description():
    # given
    expected_dict = {
        "instrumentType": "Bond",
        "instrumentCode": "string",
        "fields": {},
        "name": "string",
    }

    # when
    testing_obj = FormulaParameterDescription(
        instrument_type=InstrumentType.BOND,
        instrument_code="string",
        fields=BidAskFieldsFormulaDescription(),
        name="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.instrument_type == InstrumentType.BOND
    assert testing_obj.instrument_code == "string"
    assert testing_obj.fields == BidAskFieldsFormulaDescription()
    assert testing_obj.name == "string"
