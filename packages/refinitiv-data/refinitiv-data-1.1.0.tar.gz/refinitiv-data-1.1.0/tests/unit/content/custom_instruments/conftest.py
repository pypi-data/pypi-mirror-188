import datetime

from refinitiv.data.content import custom_instruments as ci

volume_based_udc = ci.manage.UDC(
    root="CC",
    months=ci.manage.Months(
        number_of_years=3,
        include_all_months=True,
        start_month=1,
    ),
    rollover=ci.manage.VolumeBasedRollover(
        method=ci.VolumeBasedRolloverMethod.VOLUME,
        number_of_days=1,
        join_at_day=1,
        roll_occurs_within_months=4,
        roll_on_expiry=True,
    ),
    spread_adjustment=ci.manage.SpreadAdjustment(
        adjustment="arithmetic",
        method=ci.SpreadAdjustmentMethod.CLOSE_TO_CLOSE,
        backwards=True,
    ),
)

ci_udc_response = {
    "id": "6b5d3003-622f-4a52-876e-ceb1ff2d773c",
    "symbol": "S)My_UDC_instrument.GEDTC-491962",
    "owner": "GEDTC-491962",
    "type": "udc",
    "udc": {
        "root": "CC",
        "months": {"numberOfYears": 3, "startMonth": 1, "includeAllMonths": True},
        "rollover": {
            "volumeBased": {
                "method": "volume",
                "numberOfDays": 1,
                "joinAtDay": 1,
                "rollOccursWithinMonths": 4,
                "rollOnExpiry": True,
            }
        },
        "spreadAdjustment": {
            "adjustment": "arithmetic",
            "method": "close-to-close",
            "backwards": True,
        },
    },
    "instrumentName": "9789",
    "holidays": [
        {"date": "1991-08-23", "reason": "Independence Day of Ukraine"},
        {"date": "2022-12-18", "reason": "Hanukkah"},
    ],
    "description": "fintech trading tool",
    "exchangeName": "5050",
    "currency": "GBP",
    "timeZone": "LON",
}

volume_based_dict_udc = ci_udc_response.get("udc")

day_based_udc = ci.manage.UDC(
    root="CL",
    months=ci.manage.Months(
        include_all_months=True,
        number_of_years=3,
    ),
    rollover=ci.manage.DayBasedRollover(
        method=ci.DayBasedRolloverMethod.DAYS_BEFORE_END_OF_MONTH,
        number_of_days=3,
        months_prior=1,
    ),
    spread_adjustment=ci.manage.SpreadAdjustment(
        adjustment="percentage",
        method=ci.SpreadAdjustmentMethod.CLOSE_TO_CLOSE,
        backwards=False,
    ),
)

day_based_dict_udc = {
    "root": "CL",
    "rollover": {
        "dayBased": {
            "method": "daysBeforeEndOfMonth",
            "numberOfDays": 3,
            "monthsPrior": 1,
        }
    },
    "spreadAdjustment": {
        "adjustment": "percentage",
        "method": "close-to-close",
        "backwards": False,
    },
    "months": {"numberOfYears": 3, "includeAllMonths": True},
}

manual_udc = ci.manage.UDC(
    root="CC",
    rollover=ci.manage.ManualRollover(
        ci.manage.ManualItem(month=7, year=2022, start_date="2022-02-01"),
        ci.manage.ManualItem(month=7, year=2021, start_date=datetime.date(2021, 3, 1)),
    ),
    spread_adjustment=ci.manage.SpreadAdjustment(
        adjustment="arithmetic",
        method=ci.SpreadAdjustmentMethod.CLOSE_TO_CLOSE,
        backwards=True,
    ),
)

manual_dict_udc = {
    "root": "CC",
    "rollover": {
        "manual": [
            {"month": 7, "year": 2022, "startDate": "2022-02-01T00:00:00.000000000Z"},
            {"month": 7, "year": 2021, "startDate": "2021-03-01T00:00:00.000000000Z"},
        ]
    },
    "spreadAdjustment": {
        "adjustment": "arithmetic",
        "method": "close-to-close",
        "backwards": True,
    },
}

basket_obj = ci.manage.Basket(
    constituents=[
        ci.manage.Constituent(ric="LSEG.L", weight=60),
        ci.manage.Constituent(ric="EPAM.N", weight=40),
    ],
    normalize_by_weight=True,
)

ci_basket_response = {
    "id": "c2d866ee-c8c7-4f0c-9391-789712e75436",
    "symbol": "S)My_Basket_instrument.GEDTC-491962",
    "owner": "GEDTC-491962",
    "type": "basket",
    "basket": {
        "constituents": [
            {"ric": "LSEG.L", "weight": 60.0},
            {"ric": "EPAM.N", "weight": 40.0},
        ],
        "normalizeByWeight": True,
    },
    "currency": "GBP",
    "instrumentName": "9789",
    "exchangeName": "5050",
    "holidays": [
        {"date": "1991-08-23", "reason": "Independence Day of Ukraine"},
        {"date": "2022-12-18", "reason": "Hanukkah"},
    ],
    "timeZone": "LON",
    "description": "fintech trading tool",
}

basket_dict = ci_basket_response.get("basket")

ci_create_formula_response = {
    "id": "6ded731a-24b4-4ab6-969f-9de4138b135b",
    "symbol": "S)My_formula_instrument.GEDTC-491962",
    "owner": "GEDTC-491962",
    "type": "formula",
    "formula": "GBP=*3",
    "currency": "GBP",
    "instrumentName": "9789",
    "exchangeName": "5050",
    "holidays": [
        {"date": "1991-08-23", "reason": "Independence Day of Ukraine"},
        {"date": "2022-12-18", "reason": "Hanukkah"},
    ],
    "timeZone": "LON",
    "description": "fintech trading tool",
}

ci_update_formula_response = {
    "id": "6ded731a-24b4-4ab6-969f-9de4138b135b",
    "symbol": "S)My_formula_instrument.GEDTC-491962",
    "owner": "GEDTC-491962",
    "type": "formula",
    "formula": "GBP=*3",
    "currency": "CAD",
    "instrumentName": "9789",
    "exchangeName": "5050",
    "holidays": [{"date": "2022-12-31", "reason": "New Year"}],
    "timeZone": "LON",
    "description": "fintech trading tool",
}
