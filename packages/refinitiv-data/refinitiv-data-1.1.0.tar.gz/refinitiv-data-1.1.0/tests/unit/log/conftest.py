from types import SimpleNamespace


class Record(object):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name


stub_datetime = SimpleNamespace()
stub_datetime.strftime = lambda _: "datetime"
