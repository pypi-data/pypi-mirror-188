import pytest

import refinitiv.data.content as rdc
from refinitiv.data.content.ipa.curves import zc_curve_definitions
from refinitiv.data.content.ipa.surfaces import cap, eti, fx
from refinitiv.data.delivery._data._data_provider_factory import make_provider
from tests.unit.conftest import StubSession


@pytest.mark.parametrize(
    "definition, expected_value",
    [
        (
            rdc.ipa.curves.forward_curves.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {"universe": [{"my_test_param": "test_value"}]},
        ),
        (
            rdc.ipa.curves.forward_curves.Definitions(
                [
                    rdc.ipa.curves.forward_curves.Definition(
                        extended_params={"my_test_param1": "test_value1"}
                    )
                ],
            ),
            {
                "universe": [{"my_test_param1": "test_value1"}],
            },
        ),
        (
            rdc.ipa.curves.zc_curves.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {"universe": [{"my_test_param": "test_value"}]},
        ),
        (
            rdc.ipa.curves.zc_curve_definitions.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {"universe": [{"my_test_param": "test_value"}]},
        ),
        (
            rdc.ipa.curves.zc_curve_definitions.Definitions(
                [
                    zc_curve_definitions.Definition(
                        source="Refinitiv",
                        extended_params={"my_test_param1": "test_value1"},
                    ),
                ],
            ),
            {
                "universe": [{"source": "Refinitiv", "my_test_param1": "test_value1"}],
            },
        ),
        (
            rdc.ipa.curves.zc_curves.Definitions(
                [
                    rdc.ipa.curves.zc_curve_definitions.Definition(
                        extended_params={"my_test_param1": "test_value1"}
                    )
                ],
            ),
            {
                "universe": [{"my_test_param1": "test_value1"}],
            },
        ),
        (
            rdc.ipa.financial_contracts.bond.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {
                "universe": [
                    {
                        "instrumentDefinition": {},
                        "instrumentType": "Bond",
                        "my_test_param": "test_value",
                    }
                ]
            },
        ),
        (
            rdc.ipa.financial_contracts.cap_floor.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {
                "universe": [
                    {
                        "instrumentDefinition": {},
                        "instrumentType": "CapFloor",
                        "my_test_param": "test_value",
                    }
                ]
            },
        ),
        (
            rdc.ipa.financial_contracts.cds.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {
                "universe": [
                    {
                        "instrumentDefinition": {},
                        "instrumentType": "Cds",
                        "my_test_param": "test_value",
                    }
                ]
            },
        ),
        (
            rdc.ipa.financial_contracts.cross.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {
                "universe": [
                    {
                        "instrumentDefinition": {},
                        "instrumentType": "FxCross",
                        "my_test_param": "test_value",
                    }
                ]
            },
        ),
        (
            rdc.ipa.financial_contracts.option.Definition(extended_params={}),
            {
                "universe": [
                    {
                        "instrumentDefinition": {},
                        "instrumentType": "Option",
                    }
                ]
            },
        ),
        (
            rdc.ipa.financial_contracts.repo.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {
                "universe": [
                    {
                        "instrumentDefinition": {},
                        "instrumentType": "Repo",
                        "my_test_param": "test_value",
                    }
                ]
            },
        ),
        (
            rdc.ipa.financial_contracts.swap.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {
                "universe": [
                    {
                        "instrumentDefinition": {},
                        "instrumentType": "Swap",
                        "my_test_param": "test_value",
                    }
                ]
            },
        ),
        (
            rdc.ipa.financial_contracts.swaption.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {
                "universe": [
                    {
                        "instrumentDefinition": {},
                        "instrumentType": "Swaption",
                        "my_test_param": "test_value",
                    }
                ]
            },
        ),
        (
            rdc.ipa.financial_contracts.term_deposit.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {
                "universe": [
                    {
                        "instrumentDefinition": {},
                        "instrumentType": "TermDeposit",
                        "my_test_param": "test_value",
                    }
                ]
            },
        ),
        (
            rdc.ipa.surfaces.cap.Definition(
                surface_layout=cap.SurfaceLayout(format=cap.Format.MATRIX),
                surface_parameters=cap.CapCalculationParams(
                    valuation_date="2020-03-20",
                    x_axis=cap.Axis.STRIKE,
                    y_axis=cap.Axis.TENOR,
                ),
                underlying_definition=cap.CapSurfaceDefinition(
                    instrument_code="USD123",
                    discounting_type=cap.DiscountingType.OIS_DISCOUNTING,
                ),
                surface_tag="USD_Strike__Tenor_",
                extended_params={"my_test_param": "test_value"},
            ),
            {
                "universe": [
                    {
                        "my_test_param": "test_value",
                        "surfaceLayout": {"format": "Matrix"},
                        "surfaceParameters": {
                            "valuationDate": "2020-03-20",
                            "xAxis": "Strike",
                            "yAxis": "Tenor",
                        },
                        "surfaceTag": "USD_Strike__Tenor_",
                        "underlyingDefinition": {
                            "discountingType": "OisDiscounting",
                            "instrumentCode": "USD123",
                        },
                        "underlyingType": "Cap",
                    }
                ]
            },
        ),
        (
            rdc.ipa.surfaces.eti.Definition(
                surface_layout=eti.SurfaceLayout(
                    format=eti.Format.MATRIX, y_point_count=10
                ),
                surface_parameters=eti.EtiCalculationParams(
                    price_side=eti.PriceSide.MID,
                    volatility_model=eti.VolatilityModel.SVI,
                    x_axis=eti.Axis.DATE,
                    y_axis=eti.Axis.STRIKE,
                ),
                underlying_definition={"instrumentCode": "BNPP.PA@RIC"},
                surface_tag="1",
                extended_params={"my_test_param": "test_value"},
            ),
            {
                "universe": [
                    {
                        "my_test_param": "test_value",
                        "surfaceLayout": {"format": "Matrix", "yPointCount": 10},
                        "surfaceParameters": {
                            "priceSide": "Mid",
                            "volatilityModel": "SVI",
                            "xAxis": "Date",
                            "yAxis": "Strike",
                        },
                        "surfaceTag": "1",
                        "underlyingDefinition": {"instrumentCode": "BNPP.PA@RIC"},
                        "underlyingType": "Eti",
                    }
                ]
            },
        ),
        (
            rdc.ipa.surfaces.fx.Definition(
                surface_layout=fx.SurfaceLayout(format=fx.Format.MATRIX),
                surface_parameters=fx.FxCalculationParams(
                    x_axis=fx.Axis.DATE,
                    y_axis=fx.Axis.STRIKE,
                    calculation_date="2018-08-20T00:00:00Z",
                ),
                underlying_definition={"fxCrossCode": "EURUSD"},
                extended_params={"my_test_param": "test_value"},
            ),
            {
                "universe": [
                    {
                        "my_test_param": "test_value",
                        "surfaceLayout": {"format": "Matrix"},
                        "surfaceParameters": {
                            "calculationDate": "2018-08-20T00:00:00Z",
                            "xAxis": "Date",
                            "yAxis": "Strike",
                        },
                        "underlyingDefinition": {"fxCrossCode": "EURUSD"},
                        "underlyingType": "Fx",
                    }
                ]
            },
        ),
        (
            rdc.ipa.surfaces.swaption.Definition(
                extended_params={"my_test_param": "test_value"}
            ),
            {
                "universe": [
                    {"my_test_param": "test_value", "underlyingType": "Swaption"}
                ]
            },
        ),
    ],
    ids=[
        "rdc.ipa.curves.forward_curves.Definition",
        "rdc.ipa.curves.forward_curves.Definitions",
        "rdc.ipa.curves.zc_curves.Definition",
        "rdc.ipa.curves.zc_curve_definitions.Definition",
        "rdc.ipa.curves.zc_curve_definitions.Definitions",
        "rdc.ipa.curves.zc_curves.Definitions",
        "rdc.ipa.financial_contracts.bond.Definition",
        "rdc.ipa.financial_contracts.cap_floor.Definition",
        "rdc.ipa.financial_contracts.cds.Definition",
        "rdc.ipa.financial_contracts.cross.Definition",
        "rdc.ipa.financial_contracts.option.Definition",
        "rdc.ipa.financial_contracts.repo.Definition",
        "rdc.ipa.financial_contracts.swap.Definition",
        "rdc.ipa.financial_contracts.swaption.Definition",
        "rdc.ipa.financial_contracts.term_deposit.Definition",
        "rdc.ipa.surfaces.cap.Definition",
        "rdc.ipa.surfaces.eti.Definition",
        "rdc.ipa.surfaces.fx.Definition",
        "rdc.ipa.surfaces.swaption.Definition",
    ],
)
def test_extended_params(definition, expected_value):
    content_type = definition._kwargs["__content_type__"]
    provider = make_provider(content_type)

    # when
    request = provider.request.create(StubSession(), "url", **definition._kwargs)

    # then
    testing_value = request.json
    assert testing_value == expected_value, definition
