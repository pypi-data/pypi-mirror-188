from typing import Type, TYPE_CHECKING

from ._content_data import Data
from ..delivery._data._response_factory import ResponseFactory

if TYPE_CHECKING:
    from ..delivery._data._endpoint_data import ABCData
    from ..delivery._data._response import Response
    from ..delivery._data._parsed_data import ParsedData


class ContentResponseFactory(ResponseFactory):
    def __init__(
        self,
        response_class: Type["Response"] = None,
        data_class: Type["ABCData"] = None,
    ):
        data_class = data_class or Data
        super().__init__(response_class, data_class)

    @staticmethod
    def get_dfbuilder(content_type=None, dfbuild_type=None, **kwargs):
        from ._df_builder_factory import get_dfbuilder, DFBuildType
        from .._content_type import ContentType

        content_type = content_type or kwargs.get(
            "__content_type__", ContentType.DEFAULT
        )
        dfbuild_type = dfbuild_type or kwargs.get(
            "__dfbuild_type__", DFBuildType.DATE_AS_INDEX
        )
        return get_dfbuilder(content_type, dfbuild_type)

    def create_data_success(self, parsed_data: "ParsedData", **kwargs) -> Data:
        return self.data_class(
            self.get_raw(parsed_data),
            self.get_dfbuilder(**kwargs),
            **kwargs,
        )

    def create_data_fail(self, parsed_data: "ParsedData", **kwargs) -> Data:
        return self.data_class(
            parsed_data.content_data or {},
            self.get_dfbuilder(**kwargs),
            **kwargs,
        )
