from typing import Optional, List, Union, TYPE_CHECKING

from ._serializer import Serializer
from ._tenor_bid_ask import TenorBidAsk
from ._tenor_types import TenorTypes

if TYPE_CHECKING:
    from .._types import OptStr, StrStrings


class FxSwapPoints(Serializer):
    """
    An object that contains data about the source (contributor)
    of the cross currency forward, the tenor types used in the valuation and
    the possible swap points override

    Parameters
    ----------
    additional_tenor_types : list of str, TenorTypes, list of TenorTypes, optional
        An array of tenor types used in the valuation
    source : str, optional
        The Refinitiv code of the contributor (e.g., ‘ICAP’).
        For the Refinitiv composite source, use ‘Composite’, or ignore the property
    overrides : dict, TenorBidAsk, list of TenorBidAsk, optional
        An array of tenors and corresponding swap bid, ask prices
    """

    def __init__(
        self,
        additional_tenor_types: Optional[
            Union["StrStrings", TenorTypes, List[TenorTypes]]
        ] = None,
        source: "OptStr" = None,
        overrides: Optional[
            Union[dict, List[dict], TenorBidAsk, List[TenorBidAsk]]
        ] = None,
    ) -> None:
        super().__init__()
        self.additional_tenor_types = additional_tenor_types
        self.source = source
        self.overrides = overrides

    @property
    def additional_tenor_types(self):
        return self._get_list_of_enums("additionalTenorTypes")

    @additional_tenor_types.setter
    def additional_tenor_types(self, value):
        self._set_list_of_enums(TenorTypes, "additionalTenorTypes", value)

    @property
    def overrides(self):
        return self._get_list_param("overrides")

    @overrides.setter
    def overrides(self, value):
        self._set_list_param("overrides", value)

    @property
    def source(self):
        return self._get_param("source")

    @source.setter
    def source(self, value):
        self._set_param("source", value)
