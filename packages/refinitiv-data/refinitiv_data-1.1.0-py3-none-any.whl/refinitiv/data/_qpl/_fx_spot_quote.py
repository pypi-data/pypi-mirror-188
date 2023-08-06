from typing import TYPE_CHECKING

from ._bid_ask import BidAsk

if TYPE_CHECKING:
    from .._types import OptStr, OptFloat


class FxSpotQuote(BidAsk):
    """
    An object that describes a fx spot quote

    Parameters
    ----------
    source : str, optional
        Contributor id (cid)
    ask : float, optional
        Ask value
    bid : float, optional
        Bid value
    """

    def __init__(
        self,
        source: "OptStr" = None,
        ask: "OptFloat" = None,
        bid: "OptFloat" = None,
    ) -> None:
        super().__init__(ask, bid)
        self.source = source

    @property
    def source(self):
        return self._get_param("source")

    @source.setter
    def source(self, value):
        self._set_param("source", value)
