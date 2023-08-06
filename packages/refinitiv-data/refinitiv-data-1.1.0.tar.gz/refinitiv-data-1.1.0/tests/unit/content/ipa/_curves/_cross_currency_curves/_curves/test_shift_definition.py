from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    ShiftDefinition,
)
from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    ButterflyShift,
    CombinedShift,
    FlatteningShift,
    LongEndShift,
    ParallelShift,
    ShortEndShift,
    TimeBucketShift,
    TwistShift,
)


def test_shift_definition():
    # given
    expected_dict = {
        "butterflyShift": {},
        "combinedShifts": [{}],
        "flatteningShift": {},
        "longEndShift": {},
        "parallelShift": {},
        "shortEndShift": {},
        "timeBucketShifts": [{}],
        "twistShift": {},
    }

    # when
    testing_obj = ShiftDefinition(
        butterfly_shift=ButterflyShift(),
        combined_shifts=[CombinedShift()],
        flattening_shift=FlatteningShift(),
        long_end_shift=LongEndShift(),
        parallel_shift=ParallelShift(),
        short_end_shift=ShortEndShift(),
        time_bucket_shifts=[TimeBucketShift()],
        twist_shift=TwistShift(),
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.butterfly_shift == ButterflyShift()
    assert testing_obj.combined_shifts == [CombinedShift()]
    assert testing_obj.flattening_shift == FlatteningShift()
    assert testing_obj.long_end_shift == LongEndShift()
    assert testing_obj.parallel_shift == ParallelShift()
    assert testing_obj.short_end_shift == ShortEndShift()
    assert testing_obj.time_bucket_shifts == [TimeBucketShift()]
    assert testing_obj.twist_shift == TwistShift()
