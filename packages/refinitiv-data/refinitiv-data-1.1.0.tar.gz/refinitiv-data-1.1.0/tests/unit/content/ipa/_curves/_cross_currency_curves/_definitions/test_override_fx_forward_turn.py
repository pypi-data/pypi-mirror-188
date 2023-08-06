from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    OverrideFxForwardTurn,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FxForwardTurnFields,
)


def test_override_fx_forward_turn():
    # given
    expected_dict = {
        "startDate": "string",
        "endDate": "string",
        "fields": {},
        "date": "string",
        "turnTag": "string",
    }

    # when
    testing_obj = OverrideFxForwardTurn(
        start_date="string",
        end_date="string",
        fields=FxForwardTurnFields(),
        date="string",
        turn_tag="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.start_date == "string"
    assert testing_obj.end_date == "string"
    assert testing_obj.fields == FxForwardTurnFields()
    assert testing_obj.date == "string"
    assert testing_obj.turn_tag == "string"
