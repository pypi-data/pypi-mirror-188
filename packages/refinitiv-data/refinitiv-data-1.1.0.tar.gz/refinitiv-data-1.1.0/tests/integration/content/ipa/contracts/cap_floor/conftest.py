import refinitiv.data.content.ipa.financial_contracts as rdf


def cap_floor_on_cms_definition():
    definition = rdf.cap_floor.Definition(
        instrument_tag="CapOnCms",
        stub_rule=rdf.cap_floor.StubRule.MATURITY,
        notional_ccy="USD",
        start_date="2018-06-15",
        end_date="2022-06-15",
        notional_amount=1000000,
        index_name="Composite",
        index_tenor="5Y",
        cms_template="USD_SB3L",
        interest_calculation_method="Dcb_Actual_360",
        interest_payment_frequency=rdf.cap_floor.Frequency.QUARTERLY,
        buy_sell=rdf.cap_floor.BuySell.BUY,
        cap_strike_percent=1,
        pricing_parameters=rdf.cap_floor.PricingParameters(
            skip_first_cap_floorlet=True, valuation_date="2020-02-07"
        ),
        fields=[
            "InstrumentTag",
            "InstrumentDescription",
            "StartDate",
            "EndDate",
            "MarketDataDate",
            "InterestPaymentFrequency",
            "IndexRic",
            "CapStrikePercent",
            "FloorStrikePercent",
            "NotionalCcy",
            "NotionalAmount",
            "PremiumBp",
            "PremiumPercent",
            "MarketValueInDealCcy",
            "MarketValueInReportCcy",
            "ErrorMessage",
        ],
    )
    return definition


def cap_floor_coller_pos_definition():
    definition = rdf.cap_floor.Definition(
        notional_ccy="EUR",
        start_date="2018-02-11",
        index_reset_type=rdf.cap_floor.IndexResetType.IN_ARREARS,
        tenor="5Y",
        buy_sell=rdf.cap_floor.BuySell.BUY,
        notional_amount=10000000,
        interest_payment_frequency=rdf.cap_floor.Frequency.QUARTERLY,
        cap_strike_percent=1,
        floor_strike_percent=-1,
        pricing_parameters=rdf.cap_floor.PricingParameters(
            skip_first_cap_floorlet=False, valuation_date="2020-02-07"
        ),
        fields=[
            "InstrumentTag",
            "InstrumentDescription",
            "OptionType",
            "StartDate",
            "EndDate",
            "MarketDataDate",
            "InterestPaymentFrequency",
            "IndexResetFrequency",
            "IndexRic",
            "CapStrikePercent",
            "FloorStrikePercent",
            "NotionalCcy",
            "NotionalAmount",
            "PremiumBp",
            "PremiumPercent",
            "MarketValueInDealCcy",
            "MarketValueInReportCcy",
            "ImpliedVolatilityBp",
            "ImpliedVolatilityPercent",
            "Legs",
            "DeltaPercent",
            "ForwardDeltaPercent",
            "DeltaAmountInDealCcy",
            "DeltaAmountInReportCcy",
            "VegaAmountInDealCcy",
            "VegaAmountInReportCcy",
            "ThetaAmountInDealCcy",
            "ThetaAmountInReportCcy",
            "ErrorCode",
            "ErrorMessage",
        ],
    )
    return definition


def cap_floor_amortized_definition():
    definition = rdf.cap_floor.Definition(
        instrument_tag="CapGBP",
        notional_ccy="GBP",
        start_date="2021-06-11",
        amortization_schedule=[
            rdf.cap_floor.AmortizationItem(
                start_date="2023-06-12",
                end_date="2024-06-12",
                amount=100000,
                amortization_type="Schedule",
                amortization_frequency=rdf.cap_floor.AmortizationFrequency.EVERY_COUPON,
            ),
            rdf.cap_floor.AmortizationItem(
                start_date="2024-06-11",
                end_date="2025-06-11",
                amount=-100000,
                amortization_type="Schedule",
                amortization_frequency=rdf.cap_floor.AmortizationFrequency.EVERY_COUPON,
            ),
        ],
        tenor="10Y",
        buy_sell="Buy",
        notional_amount=10000000,
        interest_payment_frequency="Quarterly",
        cap_strike_percent=0.25,
        pricing_parameters=rdf.cap_floor.PricingParameters(
            skip_first_cap_floorlet=False,
            valuation_date="2021-10-07",
            market_data_date="2020-10-07",
        ),
        fields=[
            "InstrumentTag",
            "InstrumentDescription",
            "FixedRate",
            "MarketDataDate",
            "MarketValueInDealCcy",
            "MarketValueInReportCcy",
            "ErrorMessage",
            "MarketDataDate",
        ],
    )
    return definition


def invalid_cap_floor_definition():
    definition = rdf.cap_floor.Definition(
        notional_ccy="INVAL",
        start_date="2019-02-11",
        amortization_schedule=[
            rdf.cap_floor.AmortizationItem(
                start_date="2021-02-12",
                end_date="2021-02-12",
                amount=100000,
                amortization_type="Schedule",
            ),
            rdf.cap_floor.AmortizationItem(
                start_date="2021-02-11",
                end_date="2021-02-11",
                amount=-100000,
                amortization_type="Schedule",
            ),
        ],
        tenor="5Y",
        buy_sell="Sell",
        notional_amount=10000000,
        interest_payment_frequency="Monthly",
        cap_strike_percent=1,
        pricing_parameters=rdf.cap_floor.PricingParameters(
            skip_first_cap_floorlet=True, valuation_date="2020-02-07"
        ),
        fields=[
            "InstrumentTag",
            "InstrumentDescription",
            "FixedRate",
            "MarketValueInDealCcy",
            "MarketValueInReportCcy",
            "ErrorMessage",
            "MarketDataDate",
        ],
    )
    return definition


cap_floor_universe = {
    "instrumentType": "CapFloor",
    "instrumentDefinition": {
        "instrumentTag": "CapGBP",
        "startDate": "2021-06-11",
        "tenor": "10Y",
        "notionalCcy": "GBP",
        "notionalAmount": 10000000,
        "interestPaymentFrequency": "Quarterly",
        "amortizationSchedule": [
            {
                "startDate": "2023-06-12",
                "endDate": "2024-06-12",
                "amortizationFrequency": "EveryCoupon",
                "amortizationType": "Schedule",
                "amount": 100000,
            },
            {
                "startDate": "2024-06-11",
                "endDate": "2025-06-11",
                "amortizationFrequency": "EveryCoupon",
                "amortizationType": "Schedule",
                "amount": -100000,
            },
        ],
        "buySell": "Buy",
        "capStrikePercent": 0.25,
    },
    "pricingParameters": {
        "marketDataDate": "2020-10-07",
        "skipFirstCapFloorlet": False,
        "valuationDate": "2021-10-07",
    },
}
