from typing import Optional, TYPE_CHECKING

from ._shift_definition import ShiftDefinition
from ...._object_definition import ObjectDefinition


if TYPE_CHECKING:
    from ......_types import OptStr


class FxShiftScenario(ObjectDefinition):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    fx_curve_shift : ShiftDefinition, optional
        Collection of shift parameters tenor. "all" selector supported as well.
    shift_tag : str, optional
        User defined string to identify the shift scenario tag. it can be used to link
        output curve to the shift scenario. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
    """

    def __init__(
        self,
        fx_curve_shift: Optional[ShiftDefinition] = None,
        shift_tag: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.fx_curve_shift = fx_curve_shift
        self.shift_tag = shift_tag

    @property
    def fx_curve_shift(self):
        """
        Collection of shift parameters tenor. "all" selector supported as well.
        :return: object ShiftDefinition
        """
        return self._get_object_parameter(ShiftDefinition, "fxCurveShift")

    @fx_curve_shift.setter
    def fx_curve_shift(self, value):
        self._set_object_parameter(ShiftDefinition, "fxCurveShift", value)

    @property
    def shift_tag(self):
        """
        User defined string to identify the shift scenario tag. it can be used to link
        output curve to the shift scenario. only alphabetic, numeric and '- _.#=@'
        characters are supported. optional.
        :return: str
        """
        return self._get_parameter("shiftTag")

    @shift_tag.setter
    def shift_tag(self, value):
        self._set_parameter("shiftTag", value)
