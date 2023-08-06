from typing import Any, Callable, Dict, TYPE_CHECKING

from ..delivery._data._endpoint_data import EndpointData

if TYPE_CHECKING:
    import pandas as pd


class Data(EndpointData):
    _dataframe = None

    def __init__(
        self,
        raw: Any,
        dfbuilder: Callable[[Any, Dict[str, Any]], "pd.DataFrame"],
        **kwargs,
    ):
        EndpointData.__init__(self, raw, **kwargs)
        self._dfbuilder = dfbuilder

    @property
    def df(self):
        if self._dataframe is None:
            self._dataframe = self._dfbuilder(self.raw, **self._kwargs)

        return self._dataframe
