from ._image import Image, ResizedImage
from ..._content_data_provider import ContentDataProvider
from ...._tools import ParamItem
from ...._tools import extend_params
from ....delivery._data._data_provider import RequestFactory
from ..._content_response_factory import ContentResponseFactory
from ...._core.session import Session
from ...._tools import ParamItem, get_correct_filename
from ....delivery._data._data_provider import (
    RequestFactory,
)
from ....delivery._data._endpoint_data import EndpointData
from ....delivery._data._parsed_data import ParsedData
from ....delivery._data._response_factory import ResponseFactory
from ....delivery._data._validators import (
    ValidatorContainer,
    ContentValidator,
    ContentTypeValidator,
)


class ImageData(EndpointData):
    @property
    def image(self) -> "Image":
        if "image" in self.raw:
            return ResizedImage(self.raw)
        return Image(self.raw)


query_params = [
    ParamItem("width"),
    ParamItem("height"),
]


class ImagesRequestFactory(RequestFactory):
    def extend_query_parameters(self, query_parameters, extended_params=None):
        return extend_params(query_parameters, extended_params)

    @property
    def query_params_config(self):
        return query_params

    def get_header_parameters(
        self, session=None, header_parameters=None, width=None, height=None, **kwargs
    ):
        if width or height:
            return {"accept": "image/jpeg"}
        return {"accept": "application/json"}

    def get_path_parameters(self, session=None, *, image_id=None, **kwargs):
        return {"imageId": image_id}

    def get_url(self, *args, **kwargs):
        return f"{super().get_url(*args, **kwargs)}/{{imageId}}"


def replace_from_end(s: str, old: str, new: str, count: int) -> str:
    return s[::-1].replace(old, new, count)[::-1]


def get_extension_by_image_content_type(content_type: str) -> str:
    # content_type: 'image/svg+xml'
    extension = content_type.split("/")[1]
    # extension -> 'svg+xml'
    if "+" in extension:
        extension = extension.split("+")[0]
        # extension -> 'svg'
    return extension


def get_image_filename(image_id: str, content_type: str) -> str:
    extension = get_extension_by_image_content_type(content_type)
    filename = f"{image_id}.{extension}"
    return get_correct_filename(filename, "_")


class ImagesResponseFactory(ResponseFactory):
    def create_data_success(
        self,
        parsed_data: "ParsedData",
        image_id=None,
        **kwargs,
    ):
        headers = parsed_data.raw_response.headers
        content_type = dict(headers).get("content-type")
        if content_type.startswith("image/"):
            image_data = {
                "image": parsed_data.raw_response.content,
                "filename": get_image_filename(image_id, content_type),
            }
        else:
            image_data = self.get_raw(parsed_data)

        return self.data_class(image_data, **kwargs)


class ImagesContentValidator(ContentValidator):
    @property
    def validators(self):
        return [self.content_data_is_not_none]


news_images_data_provider = ContentDataProvider(
    request=ImagesRequestFactory(),
    response=ImagesResponseFactory(data_class=ImageData),
    validator=ValidatorContainer(
        content_validator=ImagesContentValidator(),
        content_type_validator=ContentTypeValidator({"application/json", "image/jpeg"}),
    ),
)
