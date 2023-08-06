import pytest

from refinitiv.data.content.search import Views as SearchViews
from refinitiv.data.discovery._search_templates.manage import (
    depascalize_view,
    BuiltinNamespace,
)


def test_depascalize_view():
    for upper_value, enum_item in SearchViews.__members__.items():
        assert depascalize_view(enum_item.value) == upper_value


class TestBuiltinNamespace:
    def test_getitem(self):
        ns = BuiltinNamespace()
        assert ns["RICCategory"]

    def test_getitem_not_template(self):
        ns = BuiltinNamespace()
        with pytest.raises(AttributeError):
            ns["keys"]
