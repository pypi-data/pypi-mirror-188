from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FxForwardTurnFields,
)


def test_fx_forward_turn_fields():
    # given
    expected_dict = {"bid": 10.0, "ask": 10.0}

    # when
    testing_obj = FxForwardTurnFields(
        bid=10.0,
        ask=10.0,
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.bid == 10.0
    assert testing_obj.ask == 10.0
