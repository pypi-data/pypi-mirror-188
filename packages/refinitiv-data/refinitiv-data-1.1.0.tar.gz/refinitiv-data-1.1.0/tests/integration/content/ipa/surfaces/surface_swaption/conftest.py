from refinitiv.data.content.ipa.surfaces import swaption


def surface_swaption_definition():
    return swaption.Definition(
        surface_tag="My EUR VolCube",
        underlying_definition=swaption.SwaptionSurfaceDefinition(
            instrument_code="EUR",
            discounting_type=swaption.DiscountingType.OIS_DISCOUNTING,
        ),
        surface_parameters=swaption.SwaptionCalculationParams(
            shift_percent=3,
            x_axis=swaption.Axis.STRIKE,
            y_axis=swaption.Axis.TENOR,
            z_axis=swaption.Axis.EXPIRY,
        ),
        surface_layout=swaption.SurfaceLayout(
            format=swaption.Format.N_DIMENSIONAL_ARRAY,
        ),
    )


def invalid_surface_swaption_definition():
    return swaption.Definition(
        surface_tag="My EUR VolCube",
        underlying_definition=swaption.SwaptionSurfaceDefinition(
            instrument_code="INVAL",
            discounting_type=swaption.DiscountingType.OIS_DISCOUNTING,
        ),
        surface_parameters=swaption.SwaptionCalculationParams(
            shift_percent=3,
            x_axis=swaption.Axis.STRIKE,
            y_axis=swaption.Axis.TENOR,
            z_axis=swaption.Axis.EXPIRY,
        ),
        surface_layout=swaption.SurfaceLayout(
            format=swaption.Format.N_DIMENSIONAL_ARRAY,
        ),
    )
