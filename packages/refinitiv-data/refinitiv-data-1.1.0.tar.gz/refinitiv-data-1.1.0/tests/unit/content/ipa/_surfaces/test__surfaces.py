import pytest

from refinitiv.data.content.ipa import _surfaces
from refinitiv.data.content.ipa._surfaces._models import Surface
from refinitiv.data.content.ipa._surfaces._surfaces_data_provider import (
    OneSurfaceData,
    SurfacesData,
    BaseData,
    SurfaceResponseFactory,
)
from refinitiv.data.content.ipa.surfaces import eti
from refinitiv.data.delivery._data._data_provider import ParsedData
from tests.unit.content.ipa._surfaces.conftest import (
    one_surface_data_json,
    surfaces_data_json,
    one_surface_axis_params,
    surfaces_axis_params,
)


def test_surfaces_version():
    # given
    expected = "1.0.59"

    # when
    testing_version = _surfaces.__version__

    # then
    assert testing_version == expected, testing_version


def test_one_surface_data_has_one_surface():
    # given
    data = OneSurfaceData(one_surface_data_json, one_surface_axis_params)

    # when
    surface = data.surface

    # then
    assert isinstance(surface, Surface) is True


def test_one_surface_data_does_not_have_surfaces():
    # given
    data = OneSurfaceData(one_surface_data_json, one_surface_axis_params)

    # then
    with pytest.raises(AttributeError):
        # when
        data.surfaces


def test_surfaces_data_has_many_surfaces():
    # given
    data = SurfacesData(surfaces_data_json, surfaces_axis_params)

    # when
    surfaces = data.surfaces

    # then
    assert len(surfaces) > 1


def test_one_surface_data_does_not_have_surface():
    # given
    data = SurfacesData(surfaces_data_json, surfaces_axis_params)

    # then
    with pytest.raises(AttributeError):
        # when
        data.surface


def test_base_data_has_df_property():
    # given
    data = BaseData(one_surface_data_json)

    # when
    df = data.df

    # then
    assert not df.empty


def test_base_data_has_df_if_data_raw_is_empty():
    # given
    data = BaseData({"data": {}})

    # when
    df = data.df

    # then
    assert df.empty is True


def test_base_data_does_not_have_surface_property():
    # given
    data = BaseData(one_surface_data_json)

    # then
    with pytest.raises(AttributeError):
        # when
        data.surface


def test_base_data_does_not_have_surfaces_property():
    # given
    data = BaseData(one_surface_data_json)

    # then
    with pytest.raises(AttributeError):
        # when
        data.surfaces


def test_surface_response_factory_can_create_response_from_one_universe():
    # given
    definition = eti.Definition(
        underlying_definition=eti.EtiSurfaceDefinition(instrument_code="BNPP.PA@RIC"),
        surface_parameters=eti.EtiCalculationParams(
            price_side=eti.PriceSide.MID,
            volatility_model=eti.VolatilityModel.SVI,
            x_axis=eti.Axis.STRIKE,
            y_axis=eti.Axis.DATE,
        ),
        surface_tag="1_MATRIX",
        surface_layout=eti.SurfaceLayout(format=eti.Format.MATRIX, y_point_count=10),
    )
    response_factory = SurfaceResponseFactory()

    # when
    response = response_factory.create_success(
        ParsedData({}, {}, one_surface_data_json),
        universe=definition,
    )

    # then
    assert isinstance(response.data.surface, Surface) is True


def test_surface_response_factory_can_create_response_from_many_universes():
    # given
    universe = [
        eti.Definition(
            underlying_definition=eti.EtiSurfaceDefinition(
                instrument_code="BNPP.PA@RIC"
            ),
            surface_parameters=eti.EtiCalculationParams(
                price_side=eti.PriceSide.MID,
                volatility_model=eti.VolatilityModel.SVI,
                x_axis=eti.Axis.STRIKE,
                y_axis=eti.Axis.DATE,
            ),
            surface_tag="1_MATRIX",
            surface_layout=eti.SurfaceLayout(
                format=eti.Format.MATRIX, y_point_count=10
            ),
        ),
        eti.Definition(
            underlying_definition=eti.EtiSurfaceDefinition(
                instrument_code="BNPP.PA@RIC"
            ),
            surface_parameters=eti.EtiCalculationParams(
                price_side=eti.PriceSide.MID,
                volatility_model=eti.VolatilityModel.SVI,
                x_axis=eti.Axis.DATE,
                y_axis=eti.Axis.STRIKE,
            ),
            surface_tag="1_1",
            surface_layout=eti.SurfaceLayout(
                format=eti.Format.MATRIX, y_point_count=10
            ),
        ),
    ]
    response_factory = SurfaceResponseFactory()

    # when
    response = response_factory.create_success(
        ParsedData({}, {}, surfaces_data_json),
        universe=universe,
    )

    # then
    assert len(response.data.surfaces) > 1


def test_surface_response_factory_can_create_response_with_base_data():
    # given
    response_factory = SurfaceResponseFactory()

    # when
    response = response_factory.create_success(
        ParsedData({}, {}, surfaces_data_json),
    )
    data = response.data

    # then
    assert isinstance(data, BaseData)
