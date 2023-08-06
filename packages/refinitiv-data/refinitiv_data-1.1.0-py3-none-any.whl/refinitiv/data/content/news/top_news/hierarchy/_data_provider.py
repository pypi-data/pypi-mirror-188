from ._subcategory import Subcategory
from ._top_news_id import TopNewsId
from ...._content_data import Data
from ...._content_data_provider import ContentDataProvider
from ...._content_response_factory import ContentResponseFactory
from ....._tools import cached_property, ValueParamItem, make_enum_arg_parser
from .....delivery._data._data_provider import RequestFactory


class HierarchyData(Data):
    @cached_property
    def hierarchy(self):
        return {
            category["name"]: {
                page["name"]: Subcategory.from_dict(page) for page in category["pages"]
            }
            for category in self.raw.get("data", [])
        }


top_news_id_arg_parser = make_enum_arg_parser(TopNewsId)

query_params = [ValueParamItem("id", function=top_news_id_arg_parser.get_str)]


class HierarchyRequestFactory(RequestFactory):
    @property
    def query_params_config(self):
        return query_params


news_top_news_hierarchy_data_provider = ContentDataProvider(
    request=HierarchyRequestFactory(),
    response=ContentResponseFactory(data_class=HierarchyData),
)
