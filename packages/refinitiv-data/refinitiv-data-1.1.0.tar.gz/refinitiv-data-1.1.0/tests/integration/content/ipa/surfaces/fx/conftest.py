from refinitiv.data.content.ipa.surfaces import fx


def surface_fx_definition():
    definition = fx.Definition(
        underlying_definition={"fxCrossCode": "EURUSD"},
        surface_tag="FxVol-EURUSD",
        surface_layout=fx.SurfaceLayout(format=fx.Format.MATRIX),
        surface_parameters=fx.FxCalculationParams(
            x_axis=fx.Axis.DATE,
            y_axis=fx.Axis.STRIKE,
            calculation_date="2018-08-20T00:00:00Z",
        ),
    )
    return definition


def invalid_surface_fx_definition():
    definition = fx.Definition(
        underlying_definition={"fxCrossCode": "INVAL"},
        surface_tag="FxVol-EURUSD",
        surface_layout=fx.SurfaceLayout(format=fx.Format.MATRIX),
        surface_parameters=fx.FxCalculationParams(
            x_axis=fx.Axis.DATE,
            y_axis=fx.Axis.STRIKE,
            calculation_date="2018-08-20T00:00:00Z",
        ),
    )
    return definition
