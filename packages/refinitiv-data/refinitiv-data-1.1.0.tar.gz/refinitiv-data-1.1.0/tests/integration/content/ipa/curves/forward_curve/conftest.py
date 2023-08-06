forward_curve_universe = {
    "curveDefinition": {
        "indexName": "EURIBOR",
        "currency": "EUR",
        "discountingTenor": "OIS",
        "name": "EUR EURIBOR Swap ZC Curve",
    },
    "curveParameters": {"calendarAdjustment": "Calendar"},
    "forwardCurveDefinitions": [
        {
            "indexTenor": "3M",
            "forwardCurveTenors": ["0D", "1D"],
            "forwardCurveTag": "MyForwardTag",
            "forwardStartDate": "2021-02-01",
            "forwardStartTenor": "some_start_tenor",
        }
    ],
    "curveTag": "my_test_curve",
}
