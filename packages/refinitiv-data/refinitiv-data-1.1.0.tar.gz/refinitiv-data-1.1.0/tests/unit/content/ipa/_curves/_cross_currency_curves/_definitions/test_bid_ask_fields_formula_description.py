from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    BidAskFieldsFormulaDescription,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FieldDescription,
)


def test_bid_ask_fields_formula_description():
    # given
    expected_dict = {"bid": {}, "ask": {}}

    # when
    testing_obj = BidAskFieldsFormulaDescription(
        bid=FieldDescription(),
        ask=FieldDescription(),
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.bid == FieldDescription()
    assert testing_obj.ask == FieldDescription()
