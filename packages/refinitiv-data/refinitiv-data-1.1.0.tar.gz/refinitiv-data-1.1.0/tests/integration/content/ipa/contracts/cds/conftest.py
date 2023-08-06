import refinitiv.data.content.ipa.financial_contracts as rdf

cds_universe = {
    "instrumentType": "Cds",
    "instrumentDefinition": {
        "instrumentTag": "Cds1_InstrumentCode",
        "instrumentCode": "BNPP5YEUAM=R",
        "cdsConvention": "ISDA",
        "endDateMovingConvention": "NoMoving",
        "adjustToIsdaEndDate": True,
    },
    "pricingParameters": {"marketDataDate": "2020-01-01"},
}


def cds_definition():
    definition = rdf.cds.Definition(
        instrument_tag="Cds1_InstrumentCode",
        instrument_code="BNPP5YEUAM=R",
        cds_convention=rdf.cds.CdsConvention.ISDA,
        end_date_moving_convention=rdf.cds.BusinessDayConvention.NO_MOVING,
        step_in_date="2020-01-02",
        adjust_to_isda_end_date=True,
        pricing_parameters=rdf.cds.PricingParameters(market_data_date="2020-01-01"),
        fields=[
            "InstrumentTag",
            "ValuationDate",
            "InstrumentDescription",
            "StartDate",
            "EndDate",
            "SettlementDate",
            "UpfrontAmountInDealCcy",
            "CashAmountInDealCcy",
            "AccruedAmountInDealCcy",
            "AccruedBeginDate",
            "NextCouponDate",
            "UpfrontPercent",
            "ConventionalSpreadBp",
            "ParSpreadBp",
            "AccruedDays",
            "ErrorCode",
            "ErrorMessage",
            "MarketDataDate",
        ],
    )
    return definition
