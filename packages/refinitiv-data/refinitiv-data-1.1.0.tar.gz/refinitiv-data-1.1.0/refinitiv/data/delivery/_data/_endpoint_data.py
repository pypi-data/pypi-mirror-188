# coding: utf8
import abc
import collections
from enum import Enum, unique
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from ._response import ABCResponse

Error = collections.namedtuple("Error", ["code", "message"])


@unique
class RequestMethod(str, Enum):
    """
    The RESTful Data service can support multiple methods when
    sending requests to a specified endpoint.
       GET : Request data from the specified endpoint.
       POST : Send data to the specified endpoint to create/update a resource.
       DELETE : Request to delete a resource from a specified endpoint.
       PUT : Send data to the specified endpoint to create/update a resource.
    """

    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"

    def __str__(self) -> str:
        return str(self.value)


class ABCData(abc.ABC):
    pass


class EndpointData(ABCData, object):
    def __init__(self, raw: Any, owner_: "ABCResponse" = None, **kwargs):
        self._raw = raw
        self._owner = owner_
        self._kwargs = kwargs

    @property
    def raw(self):
        return self._raw
