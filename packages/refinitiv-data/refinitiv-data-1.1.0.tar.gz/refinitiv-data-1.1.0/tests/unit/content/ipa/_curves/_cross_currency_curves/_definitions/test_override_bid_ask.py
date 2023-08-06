from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    OverrideBidAsk,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    OverrideBidAskFields,
)


def test_override_bid_ask():
    # given
    expected_dict = {"instrumentCode": "string", "fields": {}, "date": "string"}

    # when
    testing_obj = OverrideBidAsk(
        instrument_code="string",
        fields=OverrideBidAskFields(),
        date="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.instrument_code == "string"
    assert testing_obj.fields == OverrideBidAskFields()
    assert testing_obj.date == "string"
