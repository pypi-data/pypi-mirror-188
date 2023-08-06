from types import SimpleNamespace


class StubDefinition:
    def __init__(self, axis) -> None:
        request_item = SimpleNamespace()
        surface_parameters = SimpleNamespace()
        surface_parameters._get_enum_parameter = lambda *args: axis
        request_item.surface_parameters = surface_parameters

        self._kwargs = {"universe": request_item}
