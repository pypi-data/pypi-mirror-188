import pytest

from tests.unit.conftest import remove_dunder_methods, remove_private_attributes
import refinitiv.data.content.ipa as ipa


def test_surface_output():
    with pytest.raises(AttributeError):
        _ = ipa.SurfaceOutput


def test_fx_surface_scope():
    with pytest.raises(AttributeError):
        _ = ipa.Definition
    with pytest.raises(AttributeError):
        _ = ipa.PricingParameters

    with pytest.raises(AttributeError):
        _ = ipa.surface.Definition
    with pytest.raises(AttributeError):
        _ = ipa.surface.PricingParameters


def test_eti_surface_scope():
    with pytest.raises(AttributeError):
        _ = ipa.Definition
    with pytest.raises(AttributeError):
        _ = ipa.PricingParameters

    with pytest.raises(AttributeError):
        _ = ipa.surface.Definition
    with pytest.raises(AttributeError):
        _ = ipa.surface.PricingParameters


def test_ir_surface_scope():
    with pytest.raises(AttributeError):
        _ = ipa.Definition
    with pytest.raises(AttributeError):
        _ = ipa.PricingParameters

    with pytest.raises(AttributeError):
        _ = ipa.surface.Definition
    with pytest.raises(AttributeError):
        _ = ipa.surface.PricingParameters
