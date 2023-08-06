from refinitiv.data.content.custom_instruments import summaries


def get_summaries_definition_with_one_universe(create_instrument, interval):
    instrument_01 = create_instrument()
    response = summaries.Definition(universe=instrument_01, interval=interval)
    return response, instrument_01


def get_summaries_definition_with_list_universes(create_instrument, interval):
    instrument_01 = create_instrument(
        type_="basket",
        basket={
            "constituents": [
                {"ric": "IBM.N", "weight": 20},
                {"ric": "EPAM.N", "weight": 80},
            ],
            "normalizeByWeight": True,
        },
    )
    instrument_02 = create_instrument()
    response = summaries.Definition(
        universe=[instrument_01, instrument_02], interval=interval
    )
    return response, [instrument_01, instrument_02]
