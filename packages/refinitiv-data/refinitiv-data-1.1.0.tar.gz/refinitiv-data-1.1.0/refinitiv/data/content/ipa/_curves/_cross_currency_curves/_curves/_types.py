from typing import Optional, List

from ._fx_forward_curve_definition import FxForwardCurveDefinition
from ._fx_forward_curve_parameters import FxForwardCurveParameters
from ._fx_shift_scenario import FxShiftScenario


CurveDefinition = Optional[FxForwardCurveDefinition]
CurveParameters = Optional[FxForwardCurveParameters]
ShiftScenarios = Optional[List[FxShiftScenario]]
