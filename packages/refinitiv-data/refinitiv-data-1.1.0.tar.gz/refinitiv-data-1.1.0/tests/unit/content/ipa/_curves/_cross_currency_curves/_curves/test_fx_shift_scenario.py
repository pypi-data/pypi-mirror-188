from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    FxShiftScenario,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    ShiftDefinition,
)


def test_fx_shift_scenario():
    # given
    expected_dict = {"fxCurveShift": {}, "shiftTag": "string"}

    # when
    testing_obj = FxShiftScenario(
        fx_curve_shift=ShiftDefinition(),
        shift_tag="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.fx_curve_shift == ShiftDefinition()
    assert testing_obj.shift_tag == "string"
