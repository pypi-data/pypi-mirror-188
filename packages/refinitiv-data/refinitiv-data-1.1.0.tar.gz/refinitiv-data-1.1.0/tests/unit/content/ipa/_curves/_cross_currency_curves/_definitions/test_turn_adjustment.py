from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    TurnAdjustment,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions._enums import (
    StandardTurnPeriod,
)


def test_turn_adjustment():
    # given
    expected_dict = {"standardTurnPeriod": "None"}

    # when
    testing_obj = TurnAdjustment(
        standard_turn_period=StandardTurnPeriod.NONE,
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.standard_turn_period == StandardTurnPeriod.NONE
