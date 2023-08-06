from refinitiv.data.content.ipa._curves._cross_currency_curves._triangulate_definitions import (
    RequestItem,
)


def test_definitions_triangulate_request_item():
    # given
    expected_dict = {
        "baseCurrency": "string",
        "baseIndexName": "string",
        "curveTag": "string",
        "quotedCurrency": "string",
        "quotedIndexName": "string",
        "valuationDate": "string",
    }

    # when
    testing_obj = RequestItem(
        base_currency="string",
        base_index_name="string",
        curve_tag="string",
        quoted_currency="string",
        quoted_index_name="string",
        valuation_date="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.base_currency == "string"
    assert testing_obj.base_index_name == "string"
    assert testing_obj.curve_tag == "string"
    assert testing_obj.quoted_currency == "string"
    assert testing_obj.quoted_index_name == "string"
    assert testing_obj.valuation_date == "string"
