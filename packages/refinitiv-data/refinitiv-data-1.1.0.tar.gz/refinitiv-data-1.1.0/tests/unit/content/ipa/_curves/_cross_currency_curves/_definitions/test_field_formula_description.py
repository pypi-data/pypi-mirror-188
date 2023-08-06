from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions import (
    FieldFormulaDescription,
)


def test_field_formula_description():
    # given
    expected_dict = {
        "historicalFidPriority": ["string1", "string2"],
        "realTimeFidPriority": ["string1", "string2"],
        "formula": "string",
    }

    # when
    testing_obj = FieldFormulaDescription(
        historical_fid_priority=["string1", "string2"],
        real_time_fid_priority=["string1", "string2"],
        formula="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.historical_fid_priority == ["string1", "string2"]
    assert testing_obj.real_time_fid_priority == ["string1", "string2"]
    assert testing_obj.formula == "string"
