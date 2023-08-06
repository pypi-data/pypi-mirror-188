from refinitiv.data.content import symbol_conversion


def symbol_conversion_definition():
    definition = symbol_conversion.Definition(
        symbols=["60000008", "60003513"],
        from_symbol_type=symbol_conversion.SymbolTypes.LIPPER_ID,
        preferred_country_code=symbol_conversion.CountryCode.USA,
    )
    return definition


def invalid_symbol_conversion_definition():
    definition = symbol_conversion.Definition(
        symbols="invalid",
        from_symbol_type=symbol_conversion.SymbolTypes.LIPPER_ID,
        to_symbol_types=[symbol_conversion.SymbolTypes.CUSIP],
        preferred_country_code="UK",
    )
    return definition
