from typing import TYPE_CHECKING

from pandas import DataFrame

from .._tools import (
    ParamItem,
    SerParamItem,
    qpl_datetime_adapter,
    ValueParamItem,
    is_date_true,
)
from ..content._content_data import Data as BaseData
from ..content._content_response_factory import ContentResponseFactory
from ..delivery._data import RequestMethod
from ..delivery._data._data_provider import DataProvider
from ..delivery._data._request_factory import RequestFactory
from ..delivery._data._validators import ValidatorContainer, ContentValidator

if TYPE_CHECKING:
    from ..delivery._data._parsed_data import ParsedData

fx_swp_to_swp_body_params_config = [
    ParamItem("fx_cross_code", "fxCrossCode"),
    ValueParamItem(
        "market_data_date_time",
        "marketDataDate",
        qpl_datetime_adapter.get_str,
        is_true=is_date_true,
    ),
    ParamItem("tenors"),
    ParamItem("fields"),
    SerParamItem("spot_ccy_1", "spotCcy1"),
    SerParamItem("spot_ccy_2", "spotCcy2"),
    SerParamItem("swap_points_ccy_1", "swapPointsCcy1"),
    SerParamItem("swap_points_ccy_2", "swapPointsCcy2"),
]


class FxSwpToSwpRequestFactory(RequestFactory):
    def update_url(self, url_root, url, path_parameters, query_parameters) -> str:
        return url

    def get_request_method(self, *, method=None, **kwargs) -> RequestMethod:
        return RequestMethod.POST

    @property
    def body_params_config(self):
        return fx_swp_to_swp_body_params_config

    def get_header_parameters(self, *args, **kwargs) -> dict:
        return {
            "x-tr-applicationid": "QPSInternal",
            "x-tr-clientapplicationid": "postman",
            "x-tr-clientid": "RDLib_python",
            "x-tr-loglevel": "Debug",
            "x-tr-scope": "RDLib-scope",
            "x-tr-uuid": "PADACT-002",
        }


class Data(BaseData):
    @property
    def df(self):
        if self._dataframe is None:
            swap_points = self.raw["swapPoints"]
            self._dataframe = DataFrame(swap_points)

        return self._dataframe


class QPLContentValidator(ContentValidator):
    @classmethod
    def content_data_has_no_error(cls, data: "ParsedData") -> bool:
        content_data = data.content_data
        error = content_data.get("error")
        if error:
            data.error_codes = error.get("code")
            data.error_messages = error.get("message")
            return False

        return True

    def __init__(self) -> None:
        super().__init__()
        self.validators.append(self.content_data_has_no_error)


fx_swp_to_swp_data_provider = DataProvider(
    request=FxSwpToSwpRequestFactory(),
    response=ContentResponseFactory(data_class=Data),
    validator=ValidatorContainer(content_validator=QPLContentValidator()),
)
