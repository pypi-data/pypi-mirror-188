from typing import TYPE_CHECKING

from ._serializer import Serializer

if TYPE_CHECKING:
    from .._types import OptFloat


class BidAsk(Serializer):
    def __init__(
        self,
        ask: "OptFloat" = None,
        bid: "OptFloat" = None,
    ) -> None:
        super().__init__()
        self.ask = ask
        self.bid = bid

    @property
    def ask(self):
        return self._get_param("ask")

    @ask.setter
    def ask(self, value):
        self._set_param("ask", value)

    @property
    def bid(self):
        return self._get_param("bid")

    @bid.setter
    def bid(self, value):
        self._set_param("bid", value)
