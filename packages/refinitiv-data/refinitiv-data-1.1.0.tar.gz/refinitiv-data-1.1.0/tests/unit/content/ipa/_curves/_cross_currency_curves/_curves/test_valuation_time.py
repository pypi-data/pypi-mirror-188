from refinitiv.data.content.ipa._curves._cross_currency_curves._curves import (
    ValuationTime,
)


def test_valuation_time():
    # given
    expected_dict = {
        "cityName": "string",
        "localTime": "string",
        "marketIdentifierCode": "string",
        "timeZoneOffset": "string",
    }

    # when
    testing_obj = ValuationTime(
        city_name="string",
        local_time="string",
        market_identifier_code="string",
        time_zone_offset="string",
    )

    # then
    assert testing_obj.get_dict() == expected_dict

    assert testing_obj.city_name == "string"
    assert testing_obj.local_time == "string"
    assert testing_obj.market_identifier_code == "string"
    assert testing_obj.time_zone_offset == "string"
