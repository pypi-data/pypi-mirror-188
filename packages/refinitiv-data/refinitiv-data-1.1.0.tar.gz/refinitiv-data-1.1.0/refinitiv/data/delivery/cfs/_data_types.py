from pandas import DataFrame

from ._tools import _get_query_parameter
from .._data._endpoint_data import EndpointData


class BaseData(EndpointData):
    def __init__(self, raw, iter_object=None, **kwargs):
        EndpointData.__init__(self, raw, **kwargs)
        self._raw["skip_token"] = _get_query_parameter(
            "skipToken", self._raw.get("@nextLink", None)
        )
        self._iter_object = iter_object
        self._dataframe = None

    @property
    def df(self):
        if self._dataframe is None:
            value = self.raw.get("value") or [self.raw]
            columns = set()
            for i in value:
                columns = columns | i.keys()
            columns = tuple(columns)
            data = [
                [value[key] if key in value else None for key in columns]
                for value in value
            ]
            self._dataframe = DataFrame(data, columns=columns)

        return self._dataframe


class BucketData(BaseData):
    @property
    def buckets(self):
        return self._iter_object


class FileSetData(BaseData):
    @property
    def file_sets(self):
        return self._iter_object


class PackageData(BaseData):
    @property
    def packages(self):
        return self._iter_object


class FileData(BaseData):
    @property
    def files(self):
        return self._iter_object
