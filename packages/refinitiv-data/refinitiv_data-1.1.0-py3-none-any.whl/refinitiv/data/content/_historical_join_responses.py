from types import SimpleNamespace
from typing import List, Union

from ._content_data import Data
from ._df_builder import build_empty_df
from ..delivery._data._parsed_data import ParsedData
from ..delivery._data._response import Response


def historical_join_responses(
    responses: List[Response], data: Union["Data", dict]
) -> Response:
    errors = []
    http_statuses = []
    http_headers = []
    http_responses = []
    request_messages = []

    for response in responses:
        http_statuses.append(response.http_status)
        http_headers.append(response.http_headers)
        request_messages.append(response.request_message)
        http_responses.append(response.http_response)

        if response.errors:
            errors += response.errors

    raw_response = SimpleNamespace()
    raw_response.request = request_messages
    raw_response.headers = http_headers
    data_factory = SimpleNamespace()
    response = Response(
        any(r.is_success for r in responses),
        ParsedData(http_statuses, raw_response),
        data_factory,
    )
    data_factory.create_data = (
        lambda *args, **kwargs: data
        if isinstance(data, Data)
        else Data(data, build_empty_df, owner_=response)
    )
    response.errors += errors
    response.http_response = http_responses

    return response
