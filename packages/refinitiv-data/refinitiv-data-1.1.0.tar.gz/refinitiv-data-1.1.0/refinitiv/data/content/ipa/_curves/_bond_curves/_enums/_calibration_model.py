from enum import Enum, unique


@unique
class CalibrationModel(Enum):
    BASIS_SPLINE = "BasisSpline"
    BOOTSTRAP = "Bootstrap"
    NELSON_SIEGEL_SVENSSON = "NelsonSiegelSvensson"
