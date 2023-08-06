from enum import Enum, unique


@unique
class InterpolationMode(Enum):
    CUBIC_SPLINE = "CubicSpline"
    LINEAR = "Linear"
    LOG = "Log"
