import abc
from typing import TYPE_CHECKING, Type, Union, Generic, TypeVar

from ._endpoint_data import EndpointData, ABCData
from ._response import ABCResponse

if TYPE_CHECKING:
    from ._parsed_data import ParsedData

DT = TypeVar("DT")


class ABCDataFactory(Generic[DT], abc.ABC):
    @abc.abstractmethod
    def create_data(
        self, parsed_data: "ParsedData", owner: ABCResponse, **kwargs
    ) -> DT:
        pass

    @abc.abstractmethod
    def create_data_success(
        self, parsed_data: "ParsedData", owner: ABCResponse, **kwargs
    ) -> DT:
        pass

    @abc.abstractmethod
    def create_data_fail(
        self, parsed_data: "ParsedData", owner: ABCResponse, **kwargs
    ) -> DT:
        pass


class DataFactoryMixin(ABCDataFactory[DT]):
    data_class: Type[DT]

    @staticmethod
    def get_raw(parsed_data: "ParsedData") -> Union[dict, list, str]:
        return parsed_data.content_data

    def create_data(
        self, parsed_data: "ParsedData", owner_: ABCResponse, **kwargs
    ) -> DT:
        if owner_.is_success:
            return self.create_data_success(parsed_data, owner_=owner_, **kwargs)
        else:
            return self.create_data_fail(parsed_data, owner_=owner_, **kwargs)

    def create_data_success(
        self, parsed_data: "ParsedData", owner_: ABCResponse, **kwargs
    ) -> DT:
        return self.data_class(raw=self.get_raw(parsed_data), owner_=owner_, **kwargs)

    def create_data_fail(
        self, parsed_data: "ParsedData", owner_: ABCResponse, **kwargs
    ) -> DT:
        return self.data_class(
            raw=parsed_data.content_data or {}, owner_=owner_, **kwargs
        )


class DataFactory(DataFactoryMixin[EndpointData]):
    def __init__(self, data_class: Type[ABCData] = None):
        self.data_class = data_class or EndpointData
