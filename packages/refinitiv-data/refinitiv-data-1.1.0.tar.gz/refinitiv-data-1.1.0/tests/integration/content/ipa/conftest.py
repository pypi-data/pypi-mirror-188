from refinitiv.data.content.ipa._curves._models._curve import Curve
from refinitiv.data.content.ipa._surfaces._models import Surface, SurfacePoint


def check_surface_curve(curve):
    assert isinstance(curve, Curve)
    assert curve.x.size > 0, f"Empty curve.x received"
    assert curve.y.size > 0, f"Empty curve.y received"


def check_surface_point(point):
    assert isinstance(point, SurfacePoint)
    assert point.x, "Empty point.x received"
    assert point.y, "Empty point.y received"
    assert point.z, "Empty point.z received"


def check_surface(surface):
    assert isinstance(surface, Surface)
    assert surface.x.size > 0, f"Empty surface.x received"
    assert surface.y.size > 0, f"Empty surface.y received"
    assert surface.z.size > 0, f"Empty surface.z received"
