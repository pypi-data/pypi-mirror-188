import refinitiv.data.content.ipa.financial_contracts as rdf


def bond_definition_fixed_rate():
    definition = rdf.bond.Definition(
        instrument_code="US10YT=RR",
        instrument_tag="TreasuryBond_10Y",
        fields=[
            "InstrumentCode",
            "BondType",
            "IssueDate",
            "MarketDataDate",
            "EndDate",
            "CouponRatePercent",
            "Accrued",
            "YieldPercent",
            "RedemptionDate",
            "ModifiedDuration",
            "Duration",
            "DV01Bp",
            "AverageLife",
            "Convexity",
            "ErrorMessage",
        ],
    )

    return definition


def bond_definition_floating_rate():
    definition = rdf.bond.Definition(
        instrument_code="61760LCZ6=",
        instrument_tag="TreasuryBond_10Y",
        pricing_parameters=rdf.bond.PricingParameters(market_data_date="2020-02-05"),
        fields=[
            "InstrumentCode",
            "BondType",
            "MarketDataDate",
            "ValuationDate",
            "IndexRic",
            "IborRatePercent",
            "Price",
            "AdjustedPrice",
            "NeutralPrice",
            "DiscountMarginBp",
            "SimpleMarginBp",
            "NeutralYieldPercent",
            "AccruedDays",
            "Accrued",
            "ErrorMessage",
        ],
    )

    return definition


def bond_definition_user_defined():
    definition = rdf.bond.Definition(
        issue_date="2002-02-28",
        end_date="2032-02-28",
        notional_ccy="USD",
        interest_payment_frequency="Annual",
        fixed_rate_percent=7,
        interest_calculation_method=rdf.bond.DayCountBasis.DCB_ACTUAL_ACTUAL,
        pricing_parameters=rdf.bond.PricingParameters(clean_price=122),
    )

    return definition


def invalid_bond_definition():
    definition = rdf.bond.Definition(
        instrument_code="INVALID_INSTRUMENT_CODE",
        instrument_tag="TreasuryBond_10Y",
        fields=["InstrumentCode", "IssueDate", "DirtyPrice", "DV01Bp", "ErrorMessage"],
    )

    return definition


bond_universe = {
    "instrumentType": "Bond",
    "instrumentDefinition": {
        "endDate": "2032-02-28",
        "notionalCcy": "USD",
        "fixedRatePercent": 9,
        "interestPaymentFrequency": "Annual",
        "interestCalculationMethod": "Dcb_Actual_Actual",
        "issueDate": "2002-02-28",
    },
    "pricingParameters": {"cleanPrice": 122},
}
