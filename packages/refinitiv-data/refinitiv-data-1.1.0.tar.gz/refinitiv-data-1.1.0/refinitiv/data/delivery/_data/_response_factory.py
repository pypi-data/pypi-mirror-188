import abc
from typing import TYPE_CHECKING, Type, Generic, TypeVar

from ._data_factory import DataFactoryMixin, ABCDataFactory
from ._endpoint_data import EndpointData, ABCData
from ._response import Response, ABCResponse

if TYPE_CHECKING:
    from ._parsed_data import ParsedData

RT = TypeVar("RT")


class ABCResponseFactory(Generic[RT], abc.ABC):
    @abc.abstractmethod
    def create_response(
        self, is_success: bool, parsed_data: "ParsedData", **kwargs
    ) -> RT:
        pass

    @abc.abstractmethod
    def create_success(self, parsed_data: "ParsedData", **kwargs) -> RT:
        pass

    @abc.abstractmethod
    def create_fail(self, parsed_data: "ParsedData", **kwargs) -> RT:
        pass


class ResponseFactory(DataFactoryMixin, ABCResponseFactory[Response]):
    def __init__(
        self,
        response_class: Type[ABCResponse] = None,
        data_class: Type[ABCData] = None,
    ):
        super().__init__()
        self.response_class = response_class or Response
        self.data_class = data_class or EndpointData

    def create_response(
        self, is_success: bool, parsed_data: "ParsedData", **kwargs
    ) -> Response:
        if is_success:
            return self.create_success(parsed_data, **kwargs)
        else:
            return self.create_fail(parsed_data, **kwargs)

    def create_success(self, parsed_data: "ParsedData", **kwargs) -> Response:
        return self.response_class(True, parsed_data, data_factory=self, **kwargs)

    def create_fail(self, parsed_data: "ParsedData", **kwargs) -> Response:
        return self.response_class(False, parsed_data, data_factory=self, **kwargs)
