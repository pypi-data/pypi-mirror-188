from enum import Enum, unique


@unique
class BasisSplineSmoothModel(Enum):
    ANDERSON_SMOOTHING_SPLINE_MODEL = "AndersonSmoothingSplineModel"
    MC_CULLOCH_LINEAR_REGRESSION = "McCullochLinearRegression"
    WAGGONER_SMOOTHING_SPLINE_MODEL = "WaggonerSmoothingSplineModel"
