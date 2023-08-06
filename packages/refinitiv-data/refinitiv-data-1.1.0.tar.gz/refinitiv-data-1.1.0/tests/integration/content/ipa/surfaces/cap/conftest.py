from refinitiv.data.content.ipa.surfaces import cap


def surface_cap_definition():
    definition = cap.Definition(
        surface_tag="USD_Strike__Tenor_",
        underlying_definition=cap.CapSurfaceDefinition(
            instrument_code="USD",
            discounting_type=cap.DiscountingType.OIS_DISCOUNTING,
        ),
        surface_layout=cap.SurfaceLayout(format=cap.Format.MATRIX),
        surface_parameters=cap.CapCalculationParams(
            valuation_date="2020-03-20",
            x_axis=cap.Axis.STRIKE,
            y_axis=cap.Axis.TENOR,
        ),
    )
    return definition


def invalid_surface_cap_definition():
    definition = cap.Definition(
        surface_tag="USD_Strike__Tenor_",
        underlying_definition=cap.CapSurfaceDefinition(
            instrument_code="USD",
            discounting_type=cap.DiscountingType.OIS_DISCOUNTING,
        ),
        surface_layout=cap.SurfaceLayout(format=cap.Format.MATRIX),
        surface_parameters=cap.CapCalculationParams(
            valuation_date="2020-03-201",
            x_axis=cap.Axis.STRIKE,
            y_axis=cap.Axis.TENOR,
        ),
    )

    return definition
