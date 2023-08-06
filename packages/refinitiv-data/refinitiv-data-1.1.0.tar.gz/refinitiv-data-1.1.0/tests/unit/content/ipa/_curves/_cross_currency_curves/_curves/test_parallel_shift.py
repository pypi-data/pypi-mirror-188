from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    ParallelShift,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves._enums import (
    ShiftType,
    ShiftUnit,
)


def test_parallel_shift():
    # given
    expected_dict = {"amount": 10.0, "shiftType": "Additive", "shiftUnit": "Absolute"}

    # when
    testing_obj = ParallelShift(
        amount=10.0,
        shift_type=ShiftType.ADDITIVE,
        shift_unit=ShiftUnit.ABSOLUTE,
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.amount == 10.0
    assert testing_obj.shift_type == ShiftType.ADDITIVE
    assert testing_obj.shift_unit == ShiftUnit.ABSOLUTE
