from refinitiv.data.content.ipa._curves._models._curve import Curve
from refinitiv.data.content.ipa.curves import forward_curves, zc_curves


def forward_curve_definition_01():
    definition = forward_curves.Definition(
        forward_curve_definitions=[
            forward_curves.ForwardCurveDefinition(
                index_tenor="3M",
                forward_curve_tag="ForwardTag",
                forward_start_date="2021-02-01",
                forward_curve_tenors=["0D", "1D"],
                forward_start_tenor="some_start_tenor",
            )
        ],
        curve_definition=forward_curves.SwapZcCurveDefinition(
            currency="EUR",
            index_name="EURIBOR",
            discounting_tenor="OIS",
            name="EUR EURIBOR Swap ZC Curve",
        ),
        curve_parameters=forward_curves.SwapZcCurveParameters(
            calendar_adjustment=forward_curves.CalendarAdjustment.CALENDAR
        ),
        curve_tag="test_curve",
    )

    return definition


def forward_curve_definition_02():
    definition = forward_curves.Definition(
        forward_curve_definitions=[
            forward_curves.ForwardCurveDefinition(
                index_tenor="3M",
                forward_curve_tag="ForwardTag",
                forward_start_date="2021-02-01",
                forward_curve_tenors=["0D", "1D"],
                forward_start_tenor="some_start_tenor",
            )
        ],
        curve_definition=forward_curves.SwapZcCurveDefinition(
            currency="EUR",
            index_name="EURIBOR",
            discounting_tenor="OIS",
            name="EUR EURIBOR Swap ZC Curve",
        ),
        curve_parameters=forward_curves.SwapZcCurveParameters(),
        curve_tag="test_curve",
    )

    return definition


def forward_curve_definition_03():
    definition = forward_curves.Definition()

    return definition


def zc_curves_01():
    definition = zc_curves.Definition(
        curve_definition=zc_curves.ZcCurveDefinitions(
            currency="CHF",
            name="CHF LIBOR Swap ZC Curve",
            discounting_tenor="OIS",
        ),
        curve_parameters=zc_curves.ZcCurveParameters(
            valuation_date="2019-08-21", use_steps=True
        ),
    )

    return definition


def zc_curves_02():
    definition = zc_curves.Definition(
        constituents={},
        curve_parameters=zc_curves.ZcCurveParameters(
            valuation_date="2019-08-21",
            price_side="Mid",
            interpolation_mode=zc_curves.ZcInterpolationMode.CUBIC_DISCOUNT,
        ),
        curve_definition=zc_curves.ZcCurveDefinitions(
            currency="EUR",
            index_name="EURIBOR",
            source="Refinitiv",
            discounting_tenor="OIS",
            name="EUR EURIBOR Swap ZC Curve",
        ),
        curve_tag="TAG",
    )
    return definition


def check_curve(curve):
    assert isinstance(curve, Curve)
    assert curve.x.size > 0, f"Empty curve.x received"
    assert curve.y.size > 0, f"Empty curve.y received"


def check_curves(response):
    curves = response.data.curves
    for curve in curves:
        check_curve(curve)


def on_response(response, definition, session):
    print(response.data.df.to_string())


def check_curve_response(response, expected_currency):
    actual_currency = response.data.raw["data"][0]["curveDefinition"]["currency"]
    assert actual_currency == expected_currency, f"{actual_currency}"
    assert not response.data.df.empty
