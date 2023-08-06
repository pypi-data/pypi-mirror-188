import refinitiv.data.content.ipa.financial_contracts as rdf
from refinitiv.data.content.ipa.curves import (
    zc_curves,
    forward_curves,
)
from refinitiv.data.content.ipa.financial_contracts import cap_floor, cds, option
from refinitiv.data.content.ipa.surfaces import cap

ZC_CURVE_DEFINITION = zc_curves.Definition(
    curve_definition=zc_curves.ZcCurveDefinitions(
        currency="CHF",
        name="CHF LIBOR Swap ZC Curve",
        discounting_tenor="OIS",
    ),
    curve_parameters=zc_curves.ZcCurveParameters(use_steps="True"),
)

ZC_CURVE_RESPONSE = {
    "error": {
        "id": "3a42afe0-28c1-4eca-a158-7a20944e5059",
        "code": "400",
        "message": "Validation error",
        "status": "Bad Request",
        "errors": [
            {
                "key": "zcCurvesRequest",
                "reason": 'zcCurvesRequest.universe.curveParameters.useSteps in body must be of type boolean: "string"',
            }
        ],
    }
}

FORWARD_CURVE_DEFINITION = forward_curves.Definition(
    curve_definition=forward_curves.SwapZcCurveDefinition(
        currency="EUR123",
        index_name="EURIBOR",
        name="EUR EURIBOR Swap ZC Curve",
        discounting_tenor="OIS",
    ),
    forward_curve_definitions=[
        forward_curves.ForwardCurveDefinition(
            index_tenor="3M",
            forward_curve_tag="ForwardTag",
            forward_start_date="2021-02-01",
            forward_curve_tenors=[
                "0D",
                "1D",
                "2D",
                "3M",
                "6M",
                "9M",
                "1Y",
                "2Y",
                "3Y",
                "4Y",
                "5Y",
                "6Y",
                "7Y",
                "8Y",
                "9Y",
                "10Y",
                "15Y",
                "20Y",
                "25Y",
            ],
        )
    ],
)

FORWARD_CURVE_RESPONSE = {
    "data": [
        {
            "error": {
                "id": "8abfe7bd-4b66-4b6d-b994-47d0758759c6/8abfe7bd-4b66-4b6d-b994-47d0758759c6",
                "code": "QPS-Curves.10",
                "message": "The service failed to find the curve constituents",
            }
        }
    ]
}

ZC_CURVES_DEFINITION = zc_curves.Definitions(
    [
        zc_curves.Definition(
            constituents={},
            curve_parameters=zc_curves.ZcCurveParameters(
                valuation_date="1719-08-21",
                price_side="Mid",
                interpolation_mode=zc_curves.ZcInterpolationMode.CUBIC_DISCOUNT,
            ),
            curve_definition=zc_curves.ZcCurveDefinitions(
                currency="EUR",
                index_name="EURIBOR",
                source="Refinitiv",
                discounting_tenor="OIS",
            ),
            curve_tag="TAG",
        ),
        zc_curves.Definition(
            curve_definition=zc_curves.ZcCurveDefinitions(
                currency="EUR",
                index_name="EURIBOR",
                source="Refinitiv",
                discounting_tenor="OIS",
            )
        ),
    ]
)

ZC_CURVES_RESPONSE = {
    "data": [
        {
            "curveTag": "TAG",
            "error": {
                "id": "d25267cf-bbfc-4230-84a4-ad8c33914e68/d25267cf-bbfc-4230-84a4-ad8c33914e68",
                "code": "QPS-Curves.7",
                "message": "The service failed to find the curve definition",
            },
        },
    ]
}

SURFACE_CAP_DEFINITION = cap.Definition(
    surface_tag="USD_Strike__Tenor_",
    underlying_definition=cap.CapSurfaceDefinition(
        instrument_code="USD123",  # <<<----
        discounting_type=cap.DiscountingType.OIS_DISCOUNTING,
    ),
    surface_layout=cap.SurfaceLayout(format=cap.Format.MATRIX),
    surface_parameters=cap.CapCalculationParams(
        valuation_date="2020-03-20",
        x_axis=cap.Axis.STRIKE,
        y_axis=cap.Axis.TENOR,
    ),
)

SURFACE_CAP_RESPONSE = {
    "data": [
        {
            "surfaceTag": "",
            "error": {
                "id": "5ccf67af-badb-47c3-8d74-c9bb9e7e994c/fc4a1fb4-1e3b-43cc-9eeb-84bed950a926",
                "status": "Error",
                "message": "The service failed to build the volatility surface",
                "code": "VolSurf.10300",
            },
        }
    ]
}

CAP_FLOOR_DEFINITION = cap_floor.Definition(
    instrument_tag="CapOnCms",
    stub_rule=rdf.cap_floor.StubRule.MATURITY,
    notional_ccy="USD123",
    start_date="2018-06-15",
    end_date="2022-06-15",
    notional_amount=1000000,
    index_name="Composite",
    index_tenor="5Y",
    interest_calculation_method="Dcb_Actual_360",
    interest_payment_frequency=rdf.cap_floor.Frequency.QUARTERLY,
    buy_sell=rdf.cap_floor.BuySell.BUY,
    cap_strike_percent=1,
    pricing_parameters=rdf.cap_floor.PricingParameters(
        skip_first_cap_floorlet=False, valuation_date="2020-02-07"
    ),
    fields=[
        "InstrumentTag",
        "InstrumentDescription",
        "StartDate",
        "EndDate",
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

CAP_FLOOR_RESPONSE = {
    "headers": [
        {"type": "String", "name": "InstrumentTag"},
        {"type": "String", "name": "InstrumentDescription"},
        {"type": "DateTime", "name": "StartDate"},
        {"type": "DateTime", "name": "EndDate"},
        {"type": "String", "name": "InterestPaymentFrequency"},
        {"type": "String", "name": "IndexRic"},
        {"type": "Float", "name": "CapStrikePercent"},
        {"type": "Float", "name": "FloorStrikePercent"},
        {"type": "String", "name": "NotionalCcy"},
        {"type": "Float", "name": "NotionalAmount"},
        {"type": "Float", "name": "PremiumBp"},
        {"type": "Float", "name": "PremiumPercent"},
        {"type": "Float", "name": "MarketValueInDealCcy"},
        {"type": "Float", "name": "MarketValueInReportCcy"},
        {"type": "String", "name": "ErrorMessage"},
    ],
    "data": [
        [
            "CapOnCms",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "Market data error : an internal error occured. Failed to cast RateSurfaceInfoResponse.",
        ]
    ],
}

CDS_DEFINITION = cds.Definition(
    instrument_tag="Cds1_InstrumentCode",
    instrument_code="123BNPP5YEUAM=R",
    cds_convention=rdf.cds.CdsConvention.ISDA,
    end_date_moving_convention=rdf.cds.BusinessDayConvention.NO_MOVING,
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
    ],
)

CDS_RESPONSE = {
    "headers": [
        {"type": "String", "name": "InstrumentTag"},
        {"type": "DateTime", "name": "ValuationDate"},
        {"type": "String", "name": "InstrumentDescription"},
        {"type": "DateTime", "name": "StartDate"},
        {"type": "DateTime", "name": "EndDate"},
        {"type": "Date", "name": "SettlementDate"},
        {"type": "Float", "name": "UpfrontAmountInDealCcy"},
        {"type": "Float", "name": "CashAmountInDealCcy"},
        {"type": "Float", "name": "AccruedAmountInDealCcy"},
        {"type": "DateTime", "name": "AccruedBeginDate"},
        {"type": "Date", "name": "NextCouponDate"},
        {"type": "Float", "name": "UpfrontPercent"},
        {"type": "Float", "name": "ConventionalSpreadBp"},
        {"type": "Float", "name": "ParSpreadBp"},
        {"type": "Integer", "name": "AccruedDays"},
        {"type": "String", "name": "ErrorCode"},
        {"type": "String", "name": "ErrorMessage"},
    ],
    "data": [
        [
            "Cds1_InstrumentCode",
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            "QPS-DPS.1",
            "Technical error occured.",
        ]
    ],
}

OPTION_DEFINITION = option.Definition(
    instrument_code="123FCHI560000L1.p",
    underlying_type=rdf.option.UnderlyingType.ETI,
    fields=[
        "MarketValueInDealCcy",
        "DeltaPercent",
        "GammaPercent",
        "RhoPercent",
        "ThetaPercent",
        "VegaPercent",
        "ErrorCode",
        "ErrorMessage",
    ],
)

OPTION_RESPONSE = {
    "headers": [
        {"type": "Float", "name": "MarketValueInDealCcy"},
        {"type": "Float", "name": "DeltaPercent"},
        {"type": "Float", "name": "GammaPercent"},
        {"type": "Float", "name": "RhoPercent"},
        {"type": "Float", "name": "ThetaPercent"},
        {"type": "Float", "name": "VegaPercent"},
        {"type": "String", "name": "ErrorCode"},
        {"type": "String", "name": "ErrorMessage"},
    ],
    "data": [
        [
            None,
            None,
            None,
            None,
            None,
            None,
            "QPS-DPS.1",
            "Technical error occured. No Realtime Data retrieved by DAL. Instrument='FCHI560000L1.p' does not exist!",
        ]
    ],
}
