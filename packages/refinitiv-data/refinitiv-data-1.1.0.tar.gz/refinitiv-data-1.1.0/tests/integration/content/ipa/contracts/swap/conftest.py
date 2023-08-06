import refinitiv.data.content.ipa.financial_contracts as rdf
from tests.integration.conftest import is_open
from tests.integration.constants_list import HttpStatusCode


def swap_definition_01():
    definition = rdf.swap.Definition(
        instrument_tag="user-defined GBP IRS",
        start_date="2019-05-21T00:00:00Z",
        tenor="10Y",
        legs=[
            rdf.swap.LegDefinition(
                direction=rdf.swap.Direction.PAID,
                notional_amount=10000000,
                notional_ccy="GBP",
                interest_type=rdf.swap.InterestType.FIXED,
                interest_payment_frequency=rdf.swap.Frequency.ANNUAL,
                interest_calculation_method=rdf.swap.DayCountBasis.DCB_30_360,
                payment_business_day_convention=rdf.swap.BusinessDayConvention.MODIFIED_FOLLOWING,
                payment_roll_convention=rdf.swap.DateRollingConvention.SAME,
                payment_business_days="UKG",
                amortization_schedule=[
                    rdf.swap.AmortizationItem(
                        remaining_notional=200000,
                        amortization_frequency=rdf.swap.AmortizationFrequency.EVERY_COUPON,
                        amortization_type=rdf.swap.AmortizationType.LINEAR,
                    )
                ],
            ),
            rdf.swap.LegDefinition(
                direction=rdf.swap.Direction.RECEIVED,
                notional_amount=10000000,
                notional_ccy="GBP",
                interest_type=rdf.swap.InterestType.FLOAT,
                interest_payment_frequency=rdf.swap.Frequency.SEMI_ANNUAL,
                index_reset_frequency=rdf.swap.Frequency.SEMI_ANNUAL,
                interest_calculation_method=rdf.swap.DayCountBasis.DCB_ACTUAL_360,
                payment_business_day_convention=rdf.swap.BusinessDayConvention.MODIFIED_FOLLOWING,
                payment_roll_convention=rdf.swap.DateRollingConvention.SAME,
                payment_business_days="UKG",
                spread_bp=20,
                index_name="SONIA",
                index_tenor="ON",
                index_reset_type=rdf.swap.IndexResetType.IN_ARREARS,
                amortization_schedule=[
                    rdf.swap.AmortizationItem(
                        remaining_notional=200000,
                        amortization_frequency=rdf.swap.AmortizationFrequency.EVERY2ND_COUPON,
                        amortization_type=rdf.swap.AmortizationType.LINEAR,
                    )
                ],
            ),
        ],
        pricing_parameters=rdf.swap.PricingParameters(discounting_tenor="ON"),
        fields=[
            "InstrumentTag",
            "InstrumentDescription",
            "FixedRatePercent",
            "MarketValueInDealCcy",
            "PV01Bp",
            "DiscountCurveName",
            "ForwardCurveName",
            "CashFlows",
            "ErrorMessage",
        ],
    )

    return definition


def swap_definition_02():
    definition = rdf.swap.Definition(
        instrument_tag="NOK_AB6O 5Y swap",
        template="NOK_AB6O",
        tenor="5Y",
        pricing_parameters=rdf.swap.PricingParameters(
            valuation_date="2018-01-10T00:00:00Z", report_ccy="JPY"
        ),
    )

    return definition


def swap_definition_03():
    definition = rdf.swap.Definition(
        tenor="2Y",
        legs=[
            rdf.swap.LegDefinition(
                interest_type=rdf.swap.InterestType.FLOAT,
                interest_payment_frequency=rdf.swap.Frequency.QUARTERLY,
                direction=rdf.swap.Direction.PAID,
                notional_amount=1,
                notional_ccy="EUR",
            ),
            rdf.swap.LegDefinition(
                index_tenor="5Y",
                interest_type=rdf.swap.InterestType.FLOAT,
                interest_payment_frequency=rdf.swap.Frequency.QUARTERLY,
                direction=rdf.swap.Direction.RECEIVED,
                notional_ccy="EUR",
            ),
        ],
        pricing_parameters=rdf.swap.PricingParameters(
            index_convexity_adjustment_integration_method=rdf.swap.IndexConvexityAdjustmentIntegrationMethod.RIEMANN_SUM,
            index_convexity_adjustment_method=rdf.swap.IndexConvexityAdjustmentMethod.BLACK_SCHOLES,
            valuation_date="2020-06-01",
        ),
        fields=[
            "InstrumentDescription",
            "Structure",
            "SettlementCcy",
            "InstrumentTag",
            "LegTag",
            "ValuationDate",
            "Calendar",
            "IndexRic",
            "IndexTenor",
            "EndDate",
            "StartDate",
            "Tenor",
            "InterestType",
            "NotionalCcy",
            "NotionalAmount",
            "MarketValueInDealCcy",
            "MarketValueInLegCcy",
            "CleanMarketValueInDealCcy",
            "CleanMarketValueInLegCcy",
            "AccruedAmountInDealCcy",
            "MarketValueInReportCcy",
            "CleanMarketValueInReportCcy",
            "AccruedAmountInReportCcy",
            "CleanPricePercent",
            "DirtyPricePercent",
            "AccruedPercent",
            "FixedRatePercent",
            "FixedRate",
            "SpreadBp",
            "ModifiedDuration",
            "Duration",
            "AnnuityAmountInDealCcy",
            "AnnuityAmountInReportCcy",
            "AnnuityBp",
            "DV01AmountInDealCcy",
            "DV01AmountInReportCcy",
            "DV01Bp",
            "PV01AmountInDealCcy",
            "PV01AmountInReportCcy",
            "PV01Bp",
            "DiscountCurveName",
            "ForwardCurveName",
            "ErrorMessage",
        ],
    )
    return definition


def check_http_status_is_success_and_df_value_not_empty(response):
    status = response.http_status
    df = response.data.df
    assert status["http_status_code"] == HttpStatusCode.TWO_HUNDRED, (
        f"Actual status code is {status['http_status_code']}, "
        f"Error: {response.http_status['error']}"
    )

    assert response.data.raw is not None, f"raw is {response.data.raw}"
    assert df is not None, f"DataFrame is {df}"
    assert not df.empty, f"DataFrame is empty: {df}"
    assert not bool(df.ErrorMessage[0]), f"{df.ErrorMessage[0]}"
    assert df.MarketValueInDealCcy is not None, f"{df.MarketValueInDealCcy}"


def check_stream_state_and_df_from_stream(stream):
    df = stream.get_snapshot()

    assert is_open(stream), f"Stream is not open"
    assert df is not None, f"DataFrame is {df}"
    assert not df.empty, f"DataFrame is empty: {df}"
    assert df.MarketValueInDealCcy is not None, f"{df.MarketValueInDealCcy}"
    assert not bool(df.ErrorMessage[0]), f"{df.ErrorMessage[0]}"

    stream.close()


swap_universe = {
    "instrumentType": "Swap",
    "instrumentDefinition": {
        "InstrumentTag": "my tag",
        "tenor": "2Y",
        "legs": [
            {
                "direction": "Paid",
                "interestType": "Float",
                "notionalCcy": "EUR",
                "notionalAmount": 1,
                "interestPaymentFrequency": "Quarterly",
            },
            {
                "direction": "Received",
                "interestType": "Float",
                "notionalCcy": "EUR",
                "indexTenor": "5Y",
                "interestPaymentFrequency": "Quarterly",
            },
        ],
    },
    "pricingParameters": {
        "indexConvexityAdjustmentIntegrationMethod": "RiemannSum",
        "indexConvexityAdjustmentMethod": "BlackScholes",
        "valuationDate": "2020-06-01",
    },
}