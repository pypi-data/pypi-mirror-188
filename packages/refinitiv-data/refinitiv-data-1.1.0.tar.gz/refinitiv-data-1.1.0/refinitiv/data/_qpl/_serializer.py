class Serializer:
    def __init__(self) -> None:
        super().__init__()
        self._dict = {}

    def _get_param(self, name):
        return self._dict.get(name)

    def _set_param(self, name, value):
        if value is None:
            return

        self._dict[name] = value

    def _get_list_param(self, name):
        return self._dict.get(name)

    def _set_list_param(self, name, value):
        if value is None:
            return

        self._dict[name] = [
            item.get_dict() if hasattr(item, "get_dict") else item for item in value
        ]

    def _get_list_of_enums(self, name):
        return self._dict.get(name)

    def _set_list_of_enums(self, enum_type, name, value):
        if value is None:
            return

        self._dict[name] = [
            item.value if isinstance(item, enum_type) else item for item in value
        ]

    def get_dict(self):
        return self._dict
