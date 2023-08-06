from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    TimeBucketShift,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves._enums import (
    ShiftType,
    ShiftUnit,
)


def test_time_bucket_shift():
    # given
    expected_dict = {
        "amount": 10.0,
        "shiftType": "Additive",
        "shiftUnit": "Absolute",
        "endTenor": "string",
        "startTenor": "string",
    }

    # when
    testing_obj = TimeBucketShift(
        amount=10.0,
        shift_type=ShiftType.ADDITIVE,
        shift_unit=ShiftUnit.ABSOLUTE,
        end_tenor="string",
        start_tenor="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.amount == 10.0
    assert testing_obj.shift_type == ShiftType.ADDITIVE
    assert testing_obj.shift_unit == ShiftUnit.ABSOLUTE
    assert testing_obj.end_tenor == "string"
    assert testing_obj.start_tenor == "string"
