import refinitiv.data.content.ipa.financial_contracts as rdf


def term_deposit_definition():
    definition = rdf.term_deposit.Definition(
        instrument_tag="AED_AM1A",
        tenor="5Y",
        notional_ccy="GBP",
        fixed_rate_percent=1,
        pricing_parameters=rdf.term_deposit.PricingParameters(
            valuation_date="2018-01-10T00:00:00Z"
        ),
        fields=[
            "InstrumentTag",
            "InstrumentDescription",
            "InterestAmountInDealCcy",
            "FixedRate",
            "MarketValueInDealCcy",
            "MarketValueInReportCcy",
            "ErrorMessage",
        ],
    )

    return definition


term_deposit_universe = {
    "instrumentType": "TermDeposit",
    "instrumentDefinition": {
        "instrumentTag": "my tag AED_AM1A",
        "tenor": "5Y",
        "notionalCcy": "GBP",
        "fixedRatePercent": 1,
    },
    "pricingParameters": {"valuationDate": "2018-01-10T00:00:00Z"},
}
