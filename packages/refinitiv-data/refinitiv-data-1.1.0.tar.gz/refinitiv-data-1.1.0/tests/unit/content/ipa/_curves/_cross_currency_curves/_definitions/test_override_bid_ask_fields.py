from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    OverrideBidAskFields,
)


def test_override_bid_ask_fields():
    # given
    expected_dict = {"bid": 10.0, "ask": 10.0}

    # when
    testing_obj = OverrideBidAskFields(
        bid=10.0,
        ask=10.0,
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.bid == 10.0
    assert testing_obj.ask == 10.0
