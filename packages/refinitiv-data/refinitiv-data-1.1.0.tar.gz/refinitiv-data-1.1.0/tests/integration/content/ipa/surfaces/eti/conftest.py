from refinitiv.data.content.ipa.surfaces import eti


def surface_eti_definition():
    definition = eti.Definition(
        underlying_definition={"instrumentCode": "BNPP.PA@RIC"},
        surface_tag="1",
        surface_layout=eti.SurfaceLayout(
            format=eti.Format.MATRIX, y_point_count=10
        ),
        surface_parameters=eti.EtiCalculationParams(
            price_side=eti.PriceSide.MID,
            volatility_model=eti.VolatilityModel.SVI,
            x_axis=eti.Axis.DATE,
            y_axis=eti.Axis.STRIKE,
        ),
    )
    return definition


def invalid_surface_eti_definition():
    definition = eti.Definition(
        underlying_definition={"instrumentCode": "BNPP.PA@RIC1"},
        surface_tag="1",
        surface_layout=eti.SurfaceLayout(
            format=eti.Format.MATRIX, y_point_count=10
        ),
        surface_parameters=eti.EtiCalculationParams(
            price_side=eti.PriceSide.MID,
            volatility_model=eti.VolatilityModel.SVI,
            x_axis=eti.Axis.DATE,
            y_axis=eti.Axis.STRIKE,
        ),
    )
    return definition
