from datetime import datetime

import refinitiv.data.content.ipa.financial_contracts as rdf


def repo_definition_01():
    definition = rdf.repo.Definition(
        start_date="2019-11-27",
        tenor="1M",
        underlying_instruments=[
            rdf.repo.UnderlyingContract(
                instrument_type="Bond",
                instrument_definition=rdf.bond.Definition(
                    instrument_code="US191450264="
                ),
            )
        ],
        pricing_parameters=rdf.repo.PricingParameters(
            market_data_date="2019-11-25",
        ),
        fields=["MarketDataDate", "ErrorMessage"],
    )

    return definition


def repo_definition_02():
    definition = rdf.repo.Definition(
        start_date="2020-08-17T00:00:00Z",
        end_date="2020-08-22T00:00:00Z",
        underlying_instruments=[
            rdf.repo.UnderlyingContract(
                instrument_type="Bond",
                instrument_definition=rdf.bond.Definition(
                    instrument_code="US191450264="
                ),
                pricing_parameters=rdf.repo.UnderlyingPricingParameters(
                    repo_parameters=rdf.repo.RepoParameters(initial_margin_percent=50)
                ),
            )
        ],
        pricing_parameters=rdf.repo.PricingParameters(
            market_data_date="2020-08-19T00:00:00Z"
        ),
    )

    return definition


def on_response(response, session, events_list=None):
    current_time = datetime.now().time()
    if events_list is not None:
        events_list.append("Response received for")
    print(current_time, "- Response received for", response.data.raw)


repo_universe = {
    "instrumentType": "Repo",
    "instrumentDefinition": {
        "InstrumentTag": "my tag",
        "startDate": "2020-08-17T00:00:00Z",
        "endDate": "2020-08-22T00:00:00Z",
        "underlyingInstruments": [
            {
                "instrumentType": "Bond",
                "instrumentDefinition": {"instrumentCode": "US191450264="},
                "pricingParameters": {"repoParameters": {"initialMarginPercent": 50}},
            }
        ],
    },
    "pricingParameters": {"marketDataDate": "2020-08-19T00:00:00Z"},
}
