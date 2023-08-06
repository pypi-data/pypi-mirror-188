from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    BidAskFieldsDescription,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FieldFormulaDescription,
)


def test_bid_ask_fields_description():
    # given
    expected_dict = {"bid": {}, "ask": {}}

    # when
    testing_obj = BidAskFieldsDescription(
        bid=FieldFormulaDescription(),
        ask=FieldFormulaDescription(),
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.bid == FieldFormulaDescription()
    assert testing_obj.ask == FieldFormulaDescription()
