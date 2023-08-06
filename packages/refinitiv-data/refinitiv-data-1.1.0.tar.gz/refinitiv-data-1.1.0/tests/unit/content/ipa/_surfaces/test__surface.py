import pytest

from refinitiv.data.content.ipa._enums import Axis
from refinitiv.data.content.ipa._surfaces._models import SurfacePoint
from refinitiv.data.content.ipa._surfaces._surfaces_data_provider import (
    OneSurfaceData,
)
from tests.unit.content.ipa._surfaces.conftest import (
    one_surface_axis_params,
    one_surface_data_json,
)


@pytest.mark.parametrize(
    "value, axis",
    [
        ("24.955", Axis.X),
        ("2021-08-20", Axis.Y),
        (63.743918703207804, Axis.Z),
    ],
)
def test_get_curve_value_has_on_axis(value, axis):
    # given
    data = OneSurfaceData(one_surface_data_json, one_surface_axis_params)

    # when
    curve = data.surface.get_curve(value, axis)

    # then
    assert curve


@pytest.mark.parametrize(
    "value, axis",
    [
        ("25", Axis.X),
        ("2021-08-25", Axis.Y),
        (70, Axis.Z),
    ],
)
def test_get_curve_value_has_not_on_axis(value, axis):
    # given
    data = OneSurfaceData(one_surface_data_json, one_surface_axis_params)

    # when
    curve = data.surface.get_curve(value, axis)

    # then
    assert curve


@pytest.mark.parametrize(
    "x, y",
    [
        ("24.955", "2021-08-20"),
    ],
)
def test_get_point_x_and_y_are_on_axis(x, y):
    # given
    data = OneSurfaceData(one_surface_data_json, one_surface_axis_params)

    # when
    point = data.surface.get_point(x, y)

    # then
    assert point


@pytest.mark.parametrize(
    "x, y",
    [
        ("25", "2021-08-25"),
    ],
)
def test_get_point_x_and_y_are_not_on_axis(x, y):
    # given
    data = OneSurfaceData(one_surface_data_json, one_surface_axis_params)

    # when
    point = data.surface.get_point(x, y)

    # then
    assert point


def test_get_axis_removed():
    """get_axis removed in favor of direct x, y, z attributes access
    https://jira.refinitiv.com/browse/EAPI-2687
    """
    data = OneSurfaceData(one_surface_data_json, one_surface_axis_params)

    with pytest.raises(AttributeError):
        data.surface.get_axis()


def test_surface_point_to_string_using_str_dunder_method():
    # given
    point = SurfacePoint(0, 0, 0)

    # when
    s = str(point)

    # then
    assert s


def test_surface_point_to_string_using_repr_dunder_method():
    # given
    point = SurfacePoint(0, 0, 0)

    # when
    s = repr(point)

    # then
    assert s
