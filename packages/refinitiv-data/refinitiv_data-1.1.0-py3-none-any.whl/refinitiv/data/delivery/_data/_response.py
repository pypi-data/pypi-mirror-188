import abc
from itertools import zip_longest
from typing import Generic, TypeVar, TYPE_CHECKING

from ._endpoint_data import Error
from ..._tools import cached_property

if TYPE_CHECKING:
    from ._parsed_data import ParsedData
    from ._response_factory import ABCDataFactory

T = TypeVar("T")


class ABCResponse(abc.ABC):
    is_success: bool


class BaseResponse(Generic[T], ABCResponse):
    def __init__(
        self,
        is_success: bool,
        parsed_data: "ParsedData",
        data_factory: "ABCDataFactory",
        **kwargs,
    ) -> None:
        self.is_success: bool = is_success
        self._parsed_data = parsed_data
        self._data_factory = data_factory
        self._kwargs = kwargs

        self._status = parsed_data.status
        self.errors = [
            Error(code, msg)
            for code, msg in zip_longest(
                parsed_data.error_codes, parsed_data.error_messages
            )
        ]
        self._raw_response = parsed_data.raw_response
        self.http_response = self._raw_response

    @cached_property
    def data(self):
        return self._data_factory.create_data(
            self._parsed_data, owner_=self, **self._kwargs
        )

    @cached_property
    def requests_count(self):
        if isinstance(self.http_response, list):
            return len(self.http_response)
        return 1

    @property
    def request_message(self):
        if self._raw_response:
            return self._raw_response.request
        return None

    @property
    def closure(self):
        if self._raw_response:
            request = self._raw_response.request
            if isinstance(request, list):
                if isinstance(request[0], list):
                    request = request[0]
                closure = [_request.headers.get("closure") for _request in request]
            else:
                closure = request.headers.get("closure")
            return closure
        return None

    @property
    def http_status(self):
        return self._status

    @property
    def http_headers(self):
        if self._raw_response:
            return self._raw_response.headers
        return None


class Response(BaseResponse):
    pass
