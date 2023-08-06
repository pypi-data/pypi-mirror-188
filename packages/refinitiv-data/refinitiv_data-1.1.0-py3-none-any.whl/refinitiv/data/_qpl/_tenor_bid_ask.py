from ._bid_ask import BidAsk
from .._types import OptFloat


class TenorBidAsk(BidAsk):
    """
    A tenor and corresponding swap bid, ask prices

    Parameters
    ----------
    tenor : str
        The code indicating the period between start date and end date
        of the instrument (e.g., '6M', '1Y').
    ask : float, optional
        Ask value
    bid : float, optional
        Bid value
    """

    def __init__(
        self,
        tenor: str,
        ask: OptFloat = None,
        bid: OptFloat = None,
    ) -> None:
        super().__init__(ask, bid)
        self.tenor = tenor

    @property
    def tenor(self):
        return self._get_param("tenor")

    @tenor.setter
    def tenor(self, value):
        self._set_param("tenor", value)
