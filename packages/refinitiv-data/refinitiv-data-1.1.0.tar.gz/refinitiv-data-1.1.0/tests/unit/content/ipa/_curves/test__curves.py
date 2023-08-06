from inspect import signature

import numpy as np
import pytest

from refinitiv.data.content.ipa._curves._models._instrument import Instrument
from refinitiv.data.content.ipa._curves._forward_curve_definition import (
    ForwardCurveDefinition,
)
from refinitiv.data.content.ipa._curves._forward_curve_request_item import (
    ForwardCurveRequestItem,
)
from refinitiv.data.content.ipa._curves._models import CurvePoint
from refinitiv.data.content.ipa._curves._models._curve import (
    ZcCurve,
    ForwardCurve,
    Curve,
)
from refinitiv.data.content.ipa._curves._swap_zc_curve_definition import (
    SwapZcCurveDefinition,
)
from refinitiv.data.content.ipa._curves._swap_zc_curve_parameters import (
    SwapZcCurveParameters,
)
from refinitiv.data.content.ipa._enums import Axis
from refinitiv.data.content.ipa import curves as public_curves
from refinitiv.data.content.ipa.curves import (
    zc_curves,
    forward_curves,
)
from tests.unit.conftest import (
    remove_dunder_methods,
    remove_private_attributes,
    has_property_names_in_class,
    get_property_names,
    StubSession,
    StubResponse,
)
from tests.unit.content.ipa._curves.conftest import (
    create_swap_zc_curve_def,
    create_forward_curve_def,
    zc_curves_definitions_json,
)


def test_surfaces_version():
    # given
    expected = "1.0.59"

    # when
    from refinitiv.data.content.ipa import _curves

    testing_version = _curves.__version__

    # then
    assert testing_version == expected, testing_version


def test_zc_curve():
    # given
    kwargs = {"isDiscountCurve": True}
    curve = ZcCurve(x=np.array([]), y=np.array([]), index_tenor="index_tenor", **kwargs)

    # when
    s = str(curve)

    # then
    assert s


def test_forward_curve():
    # given
    kwargs = {
        "forwardCurveTag": "forward_curve_tag",
        "forwardStart": "forward_start",
        "indexTenor": "index_tenor",
    }
    curve = ForwardCurve(x=np.array([]), y=np.array([]), **kwargs)

    # then
    assert curve.x is not None and curve.y is not None


def test_get_axis_removed():
    """get_axis removed in favor of direct access to x, y attributes
    https://jira.refinitiv.com/browse/EAPI-2687
    """
    curve = ForwardCurve(x=np.array([]), y=np.array([]))

    with pytest.raises(AttributeError):
        curve.get_axis()


@pytest.mark.skip(reason="Scipy 1.9.x has different float result")
def test_curve_get_point_by_axis_x():
    # given
    # array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    x = np.arange(0, 10)
    # array([1.        , 0.71653131, 0.51341712, 0.36787944, 0.26359714,
    #        0.1888756 , 0.13533528, 0.09697197, 0.06948345, 0.04978707])
    y = np.exp(-x / 3.0)
    curve = Curve(x=x, y=y)

    # when
    point = curve.get_point(5.5, Axis.X)

    # then
    assert point.x == 5.5 and point.y == 0.16210544303708727, point


@pytest.mark.skip(reason="Scipy 1.9.x has different float result")
def test_curve_get_point_by_axis_y():
    # given
    # array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    x = np.arange(0, 10)
    # array([1.        , 0.71653131, 0.51341712, 0.36787944, 0.26359714,
    #        0.1888756 , 0.13533528, 0.09697197, 0.06948345, 0.04978707])
    y = np.exp(-x / 3.0)
    curve = Curve(x=x, y=y)

    # when
    point = curve.get_point(0.5, Axis.Y)

    # then
    assert point.x == 2.0921900035081817 and point.y == 0.5, point


def test_curve_point_to_string_using_str_dunder_method():
    # given
    point = CurvePoint(0, 0)

    # when
    s = str(point)

    # then
    assert s


def test_curve_point_to_string_using_repr_dunder_method():
    # given
    point = CurvePoint(0, 0)

    # when
    s = repr(point)

    # then
    assert s


def test_curve_get_point_raise_error_if_axis_is_invalid():
    # given
    curve = Curve(x=np.array([]), y=np.array([]))

    # then
    with pytest.raises(ValueError):
        # when
        curve.get_point(0.5, Axis.Z)


def test_parameters_forward_curve_definition():
    """
    ipa.forward_curves.ForwardCurveDefinition(
        index_tenor='3M',  # required
        forward_curve_tag='ForwardTag',  # required
        forward_start_date='2021-02-01',  # optional
        forward_curve_tenors=['0D', '1D'],  # optional
        forward_start_tenor='some_start_tenor'  # optional
        )
    """
    try:
        forward_curves.ForwardCurveDefinition(
            index_tenor="3M",
            forward_curve_tag="ForwardTag",
            forward_start_date="2021-02-01",
            forward_curve_tenors=["0D", "1D"],
            forward_start_tenor="some_start_tenor",
        )
    except Exception as e:
        assert False, e


def test_parameters_swap_zc_curve_definition():
    """
    ipa.forward_curves.SwapZcCurveDefinition(
        currency='EUR',  # all fields are optional
        indexName='EURIBOR',
        discountingTenor='OIS',
        )
    """
    try:
        forward_curves.SwapZcCurveDefinition(
            currency="EUR",
            index_name="EURIBOR",
            discounting_tenor="OIS",
        )
    except Exception as e:
        assert False, e


def test_parameters_swap_zc_curve_definition_all_optional():
    try:
        forward_curves.SwapZcCurveDefinition()
    except Exception as e:
        assert False, e


def test_definitions_single_forward_curve_full_definition():
    """
    ipa.forward_curves.Definition(
        curve_definition=swap_sc_curve_def,  # required
        forward_curve_definitions=[forward_curve_def],  # required
        curveParameters=...,  # optional (SwapZcCurveParameters),
        curveTag='some_tag'  # optional (string)
        )
    """
    try:
        forward_curves.Definition(
            curve_definition=create_swap_zc_curve_def(),
            forward_curve_definitions=[create_forward_curve_def()],
            curve_parameters=forward_curves.SwapZcCurveParameters(),
            curve_tag="some_tag",
        )
    except Exception as e:
        assert False, e


def test_forward_curves_scope():
    expected_attributes = [
        "AssetClass",
        "CalendarAdjustment",
        "CompoundingType",
        "ConvexityAdjustment",
        "DayCountBasis",
        "Definition",
        "Definitions",
        "ExtrapolationMode",
        "ForwardCurveDefinition",
        "InterpolationMode",
        "Outputs",
        "PriceSide",
        "RiskType",
        "Step",
        "SwapZcCurveDefinition",
        "SwapZcCurveParameters",
        "Turn",
    ]
    testing_attributes = dir(forward_curves)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes, set(expected_attributes) - set(
        testing_attributes
    )


def test_zc_curves_scope():
    expected_attributes = [
        "AssetClass",
        "CalendarAdjustment",
        "CompoundingType",
        "DayCountBasis",
        "Definition",
        "Definitions",
        "ExtrapolationMode",
        "MarketDataAccessDeniedFallback",
        "Outputs",
        "PriceSide",
        "RiskType",
        "ZcCurveDefinitions",
        "ZcCurveParameters",
        "ZcInterpolationMode",
    ]
    testing_attributes = dir(zc_curves)
    testing_attributes = remove_dunder_methods(testing_attributes)
    testing_attributes = remove_private_attributes(testing_attributes)
    assert expected_attributes == testing_attributes


@pytest.mark.parametrize(
    argnames="input_data",
    ids=[
        "ForwardCurveRequestItem",
        "ForwardCurveDefinition",
        "SwapZcCurveDefinition",
        "Instrument",
    ],
    argvalues=[
        (
            ForwardCurveRequestItem,
            {
                "curve_definition": SwapZcCurveDefinition(
                    currency="EUR",
                    index_name="EURIBOR",
                    discounting_tenor="OIS",
                ),
                "forward_curve_definitions": [ForwardCurveDefinition(index_tenor="3M")],
                "curve_parameters": SwapZcCurveParameters(),
                "curve_tag": "curve_tag",
            },
        ),
        (
            ForwardCurveDefinition,
            {
                "index_tenor": "3M",
                "forward_curve_tag": "ForwardTag",
                "forward_start_date": "2021-02-01",
                "forward_curve_tenors": ["0D", "1D"],
                "forward_start_tenor": "some_start_tenor",
            },
        ),
        (
            SwapZcCurveDefinition,
            {
                "currency": "EUR",
                "index_name": "EURIBOR",
                "index_tenors": ["3M"],
                "discounting_tenor": "OIS",
                "main_constituent_asset_class": forward_curves.AssetClass.SWAP,
                "risk_type": forward_curves.RiskType.INTEREST_RATE,
                "market_data_location": "market_data_location",
                "name": "name",
                "source": "Refinitiv",
                "id": "id",
            },
        ),
        (
            Instrument,
            {
                "instrument_code": "EUR",
                "value": "EURIBOR",
            },
        ),
    ],
)
def test_forward_curve_request_item_parameter(input_data):
    cls, kwargs = input_data
    args_names = list(kwargs.keys())
    inst = cls(**kwargs)

    s = signature(cls.__init__)
    assert len(s.parameters) == (len(args_names) + 1)  # +1 for (self)

    assert has_property_names_in_class(cls, args_names), set(args_names) - set(
        get_property_names(cls)
    )

    for k, v in kwargs.items():
        attr = getattr(inst, k)
        assert attr == v, k


@pytest.mark.parametrize(
    "esg_definition, expected_repr",
    [
        (
            public_curves.zc_curves.ZcCurveDefinitions(),
            "<refinitiv.data.content.ipa.curves.zc_curves.ZcCurveDefinitions object at {0}>",
        ),
        (
            public_curves.zc_curves.ZcCurveParameters(),
            "<refinitiv.data.content.ipa.curves.zc_curves.ZcCurveParameters object at {0}>",
        ),
        (
            public_curves.zc_curves.Definitions(public_curves.zc_curves.Definition()),
            "<refinitiv.data.content.ipa.curves.zc_curves.Definitions object at {0}>",
        ),
        (
            public_curves.zc_curves.Definition(),
            "<refinitiv.data.content.ipa.curves.zc_curves.Definition object at {0}>",
        ),
        (
            public_curves.forward_curves.SwapZcCurveParameters(),
            "<refinitiv.data.content.ipa.curves.forward_curves.SwapZcCurveParameters object at {0}>",
        ),
        (
            public_curves.forward_curves.SwapZcCurveDefinition(),
            "<refinitiv.data.content.ipa.curves.forward_curves.SwapZcCurveDefinition object at {0}>",
        ),
        (
            public_curves.forward_curves.Definitions(
                public_curves.forward_curves.Definition()
            ),
            "<refinitiv.data.content.ipa.curves.forward_curves.Definitions object at {0}>",
        ),
        (
            public_curves.forward_curves.Definition(),
            "<refinitiv.data.content.ipa.curves.forward_curves.Definition object at {0}>",
        ),
    ],
)
def test_esg_content_repr(esg_definition, expected_repr):
    # given
    obj_id = hex(id(esg_definition))

    # when
    s = repr(esg_definition)

    # then
    assert s == expected_repr.format(obj_id)


def test_zc_curves_definition_attribute_error():
    # given
    response = StubResponse(zc_curves_definitions_json)
    session = StubSession(is_open=True, response=response)
    zc_curve_definition = zc_curves.Definition(
        curve_definition=zc_curves.ZcCurveDefinitions(
            currency="CHF",
            name="CHF LIBOR Swap ZC Curve",
            discounting_tenor="OIS",
        ),
        curve_parameters=zc_curves.ZcCurveParameters(
            valuation_date="2019-08-21", use_steps=True
        ),
    )
    definition = zc_curves.Definitions([zc_curve_definition, zc_curves.Definition()])
    response = definition.get_data(session)

    try:
        # when
        response.data.curves
    except Exception as e:
        assert False, str(e)
    else:
        # then
        assert True
