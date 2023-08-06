from refinitiv.data.content.ipa._curves._cross_currency_curves._definitions._delete import (
    DeleteRequest,
)


def test_curve_definition_delete_request():
    # given
    expected_dict = {"id": "string"}

    # when
    testing_obj = DeleteRequest(
        id="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.id == "string"
