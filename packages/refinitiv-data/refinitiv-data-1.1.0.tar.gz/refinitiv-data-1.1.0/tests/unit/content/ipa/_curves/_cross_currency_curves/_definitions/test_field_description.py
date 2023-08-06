from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FieldDescription,
)


def test_field_description():
    # given
    expected_dict = {
        "historicalFidPriority": ["string1", "string2"],
        "realTimeFidPriority": ["string1", "string2"],
    }

    # when
    testing_obj = FieldDescription(
        historical_fid_priority=["string1", "string2"],
        real_time_fid_priority=["string1", "string2"],
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.historical_fid_priority == ["string1", "string2"]
    assert testing_obj.real_time_fid_priority == ["string1", "string2"]
