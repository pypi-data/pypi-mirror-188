import pytest

from refinitiv.data.discovery._search_templates.namespaces import Namespace
from refinitiv.data.discovery._search_templates.search import DiscoverySearchTemplate


class TestBasicNameSpace:
    def test_basic(self):
        ns = Namespace(
            locals=Namespace(
                One=DiscoverySearchTemplate(name="One"),
            ),
            user=Namespace(
                sub=Namespace(
                    Two=DiscoverySearchTemplate(name="Two"),
                ),
                Three=DiscoverySearchTemplate(name="Three"),
            ),
        )
        assert ns.get("user.sub.Two")
        assert not ns.get("user.sub.Two.val")
        assert set(ns) == {"locals", "user"}

    def test_keys_must_be_strings(self):
        with pytest.raises(TypeError):
            Namespace(**{1: DiscoverySearchTemplate("1")})

    def test_names_cant_contain_dots(self):
        with pytest.raises(ValueError):
            Namespace(**{"a.b": DiscoverySearchTemplate("1")})

    def test_cant_have_arbitrary_types(self):
        with pytest.raises(TypeError):
            Namespace(abc=123)
