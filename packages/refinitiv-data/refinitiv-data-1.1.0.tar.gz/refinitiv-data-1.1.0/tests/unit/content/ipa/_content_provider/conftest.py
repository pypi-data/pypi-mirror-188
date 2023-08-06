from enum import Enum


class StubInstrument:
    def __init__(self) -> None:
        self._kwargs = {}

    def get_dict(self):
        return {}


class StubOutputs(Enum):
    OUTPUTS = "outputs"
