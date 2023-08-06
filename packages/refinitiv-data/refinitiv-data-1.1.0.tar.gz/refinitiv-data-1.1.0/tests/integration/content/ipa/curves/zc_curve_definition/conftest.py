from refinitiv.data.content.ipa.curves import zc_curve_definitions


def zc_curve_definition_01():
    definition = zc_curve_definitions.Definition(
        source="Refinitiv",
        index_name="EURIBOR",
        valuation_date="2020-07-01",
    )
    return definition


def zc_curve_definition_02():
    return zc_curve_definitions.Definition()


def invalid_zc_curve_definition():
    definition = zc_curve_definitions.Definition(
        source="Invalid",
        index_name="EURIBOR",
        valuation_date="2020-07-01",
    )
    return definition


def check_sc_curve_definitions_response(response, expected_currency):
    actual_currency = response.data.raw["data"][0]["curveDefinitions"][0]["currency"]
    assert actual_currency == expected_currency, f"{actual_currency}"
    assert not response.data.df.isnull().values.all()


zc_curve_definition_universe = {
    "indexName": "EURIBOR",
    "source": "Refinitiv",
    "valuationDate": "2020-07-01",
}
