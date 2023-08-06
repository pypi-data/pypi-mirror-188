import refinitiv.data.content.ipa.financial_contracts as rdf
from tests.integration.content.ipa.contracts.swap.conftest import swap_definition_01


def swaption_definition_01():
    definition = rdf.swaption.Definition(
        instrument_tag="BermudanEURswaption",
        settlement_type=rdf.swaption.SwaptionSettlementType.CASH,
        tenor="7Y",
        strike_percent=2.75,
        notional_amount=1000000,
        buy_sell=rdf.swaption.BuySell.BUY,
        swaption_type=rdf.swaption.SwaptionType.PAYER,
        exercise_style=rdf.swaption.ExerciseStyle.BERM,
        bermudan_swaption_definition=rdf.swaption.BermudanSwaptionDefinition(
            exercise_schedule_type=rdf.swaption.ExerciseScheduleType.FLOAT_LEG,
            notification_days=0,
        ),
        underlying_definition=rdf.swap.Definition(tenor="3Y", template="NOK_AB6O"),
        pricing_parameters=rdf.swaption.PricingParameters(
            valuation_date="2020-04-24", nb_iterations=80
        ),
    )

    return definition


def swaption_definition_02():
    definition = rdf.swaption.Definition(
        instrument_tag="myGBPswaption",
        settlement_type=rdf.swaption.SwaptionSettlementType.CASH,
        tenor="5Y",
        strike_percent=2,
        notional_amount=1000000,
        buy_sell=rdf.swaption.BuySell.BUY,
        exercise_style=rdf.swaption.ExerciseStyle.EURO,
        swaption_type=rdf.swaption.SwaptionType.PAYER,
        bermudan_swaption_definition=rdf.swaption.BermudanSwaptionDefinition(
            exercise_schedule_type=rdf.swaption.ExerciseScheduleType.FLOAT_LEG,
            notification_days=0,
        ),
        underlying_definition=rdf.swap.Definition(tenor="5Y", template="OIS_SONIA"),
        pricing_parameters=rdf.swaption.PricingParameters(valuation_date="2021-11-16"),
        fields=[
            "MarketValueInDealCcy",
            "MarketValueInReportCcy",
            "DeltaPercent",
            "GammaPercent",
            "ThetaPercent",
            "ErrorCode",
            "ErrorMessage",
        ],
    )

    return definition


swaption_universe = {
    "instrumentType": "Swaption",
    "instrumentDefinition": {
        "instrumentTag": "BermudanEURswaption",
        "tenor": "7Y",
        "notionalAmount": 1000000,
        "bermudanSwaptionDefinition": {
            "exerciseScheduleType": "FloatLeg",
            "notificationDays": 0,
        },
        "buySell": "Buy",
        "exerciseStyle": "BERM",
        "settlementType": "Cash",
        "swaptionType": "Payer",
        "underlyingDefinition": {"tenor": "3Y", "template": "NOK_AB6O"},
        "strikePercent": 2.75,
    },
    "pricingParameters": {"nbIterations": 80, "valuationDate": "2020-04-24"},
}
