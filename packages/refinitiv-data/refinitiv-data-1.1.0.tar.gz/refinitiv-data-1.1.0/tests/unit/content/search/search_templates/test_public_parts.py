from unittest.mock import patch

import pandas as pd
import pytest

from refinitiv.data.content.search import Views as SearchViews
from refinitiv.data.discovery import search_templates
from refinitiv.data.discovery._search_templates.search import DiscoverySearchTemplate
from refinitiv.data.discovery._search_templates.manage import UserNamespace
from refinitiv.data import get_config


class Tmp:
    """Tpl template

    Methods
    -------
    search
        a
            A param
            default: 1

        b
            B param

        c
            default: 'string'
    """


class TestDiscoverySearchTemplate:
    def test_repr(self):
        assert (
            repr(DiscoverySearchTemplate(name="DST"))
            == "<DiscoverySearchTemplate 'DST'>"
        )

    def test_export(self):
        class TestSearchTemplate(DiscoverySearchTemplate):
            def __init__(self):
                super().__init__(
                    name="RICCategory",
                    pass_through_defaults={
                        "view": SearchViews.QUOTES_AND_STIRS,
                        "select": "RCSAssetCategoryLeaf",
                        "top": 1,
                    },
                    placeholders_defaults={
                        "ric": "ABC",
                    },
                    filter="RIC eq '#{ric}'",
                )

        assert TestSearchTemplate()._export() == {
            "request_body": {
                "View": "QuotesAndSTIRs",
                "Select": "RCSAssetCategoryLeaf",
                "Top": 1,
                "Filter": "RIC eq '#{ric}'",
            },
            "parameters": {
                "ric": {"default": "ABC"},
            },
        }


class TestNamespaces:
    def test_none_namespace(self):
        get_config().set_param(
            "search.templates", {"CustomNamespace1": None}, auto_create=True
        )
        assert isinstance(search_templates["CustomNamespace1"], UserNamespace)

    def test_namespace_getitem(self):
        get_config().set_param(
            "search.templates",
            {"CustomNamespace2": {"InternalNamespace": None}},
            auto_create=True,
        )
        assert isinstance(
            search_templates["CustomNamespace2"]["InternalNamespace"], UserNamespace
        )

    def test_namespace_keys(self):
        get_config().set_param(
            "search.templates",
            {"CustomNamespace3": {"InternalNamespace": None}},
            auto_create=True,
        )
        assert search_templates["CustomNamespace3"].keys() == ["InternalNamespace"]

    def test_namespace_in(self):
        get_config().set_param(
            "search.templates",
            {"CustomNamespace4": {"InternalNamespace": None}},
            auto_create=True,
        )
        assert "InternalNamespace" in search_templates["CustomNamespace4"]

    def test_template_in_namespace(self):
        get_config().set_param(
            "search.templates",
            {
                "CustomNamespace5": {
                    "Equity": {
                        "request_body": {
                            "View": "EquityQuotes",
                            "Filter": "#{a}",
                        },
                    }
                }
            },
            auto_create=True,
        )
        assert isinstance(
            search_templates["CustomNamespace5"]["Equity"], DiscoverySearchTemplate
        )

    def test_namespace_with_body(self):
        get_config().set_param(
            "search.templates",
            {
                "CustomNamespace6": {
                    "parameters": {
                        "ric": {"default": "ABC"},
                    },
                }
            },
            auto_create=True,
        )
        assert isinstance(search_templates["CustomNamespace6"], UserNamespace)

    def test_template_in_nested_namespace(self):
        get_config().set_param(
            "search.templates",
            {
                "CustomNamespace7": {
                    "InternalNamespace": {
                        "Equity": {
                            "request_body": {
                                "View": "EquityQuotes",
                                "Filter": "#{a}",
                            },
                        }
                    }
                }
            },
            auto_create=True,
        )
        assert isinstance(
            search_templates["CustomNamespace7"]["InternalNamespace"]["Equity"],
            DiscoverySearchTemplate,
        )

    def test_request_body_namespace_key(self):
        get_config().set_param(
            "search.templates",
            {"CustomNamespace8": None},
            auto_create=True,
        )
        with pytest.raises(KeyError) as excinfo:
            template = search_templates["CustomNamespace8"]["request_body"]
            assert "request_body is a reserved key" in str(excinfo.value)


class TestTemplates:
    def test_keys(self):
        config = get_config()
        if "search.templates" in config:
            del config["search.templates"]
        config.set_param("search.templates", {"Equity": None}, auto_create=True)
        assert set(search_templates.keys()) == {"Equity"}

    def test_empty_config(self):
        config = get_config()
        if "search.templates" in config:
            del config["search.templates"]
        assert set(search_templates.keys()) == set()
        with pytest.raises(KeyError):
            search_templates["Abracadabra"]

    def test_in_operator(self):
        get_config().set_param("search.templates", {"Equity": None}, auto_create=True)
        assert "Equity" in search_templates

    def test_converts_arguments_case(self):
        get_config().set_param(
            "search.templates",
            {
                "Equity": {
                    "request_body": {
                        "GroupCount": 5,
                    }
                }
            },
            auto_create=True,
        )
        assert "group_count" in search_templates["Equity"]._search_kwargs()
        assert search_templates["Equity"]._search_kwargs()["group_count"] == 5

    def test_defaults(self):
        get_config().set_param(
            "search.templates",
            {
                "Equity": {
                    "request_body": {
                        "View": "EquityQuotes",
                        "Filter": "#{a}",
                    },
                    "parameters": {"a": {"default": 1}},
                }
            },
            auto_create=True,
        )
        search_templates["Equity"]._search_kwargs()

    def test_definition_arg_in_parameters(self):
        get_config().set_param(
            "search.templates",
            {
                "Equity": {
                    "request_body": {
                        "View": "EquityQuotes",
                    },
                    "parameters": {
                        "top": {
                            "default": 100,
                            "description": "top description",
                        }
                    },
                }
            },
            auto_create=True,
        )
        assert search_templates["Equity"]._search_kwargs().get("top") == 100
        assert "top description" in search_templates["Equity"].__doc__

    def test_docstrings(self):
        get_config().set_param(
            "search.templates",
            {
                "Tpl": {
                    "request_body": {
                        "View": "EquityQuotes",
                        "Filter": "#{a} #{b} #{c}",
                    },
                    "description": "Tpl template",
                    "parameters": {
                        "a": {"default": 1, "description": "A param"},
                        "b": {"description": "B param"},
                        "c": {"default": "string"},
                    },
                }
            },
            auto_create=True,
        )

        assert search_templates["Tpl"].__doc__.strip() == Tmp.__doc__.strip()

    def test_conditionals(self):
        get_config().set_param(
            "search.templates",
            {
                "Roots": {
                    "request_body": {
                        "Filter": "{{if ric}}RIC eq '#{ric}'{{endif}}",
                    },
                    "parameters": {
                        "ric": {
                            "optional": True,
                        }
                    },
                }
            },
            auto_create=True,
        )
        assert search_templates["Roots"]._search_kwargs() == {"filter": ""}

    def test_locals(self):
        get_config().set_param(
            "search.templates",
            {
                "Roots": {
                    "request_body": {
                        "Filter": "RicRoot eq '#{_.Root.RicRoot.0}'",
                    },
                    "locals": {"Root": {"request_body": {"Filter": "RIC eq '#{ric}'"}}},
                }
            },
            auto_create=True,
        )
        with patch(
            "refinitiv.data.discovery._search_templates.search.search.Definition.get_data"
        ) as mock:
            mock.return_value.data.df = pd.DataFrame([{"RicRoot": "1333"}])
            assert (
                search_templates["Roots"]._search_kwargs(ric="1333.T")["filter"]
                == "RicRoot eq '1333'"
            )

    def test_locals_join(self):
        get_config().set_param(
            "search.templates",
            {
                "Roots": {
                    "request_body": {"Filter": "RicRoot in [#{_.Root.RicRoot|in}]"},
                    "locals": {"Root": {"request_body": {"Filter": "RIC eq '#{ric}'"}}},
                }
            },
            auto_create=True,
        )
        with patch(
            "refinitiv.data.discovery._search_templates.search.search.Definition.get_data"
        ) as mock:
            mock.return_value.data.df = pd.DataFrame(
                [{"RicRoot": "1333"}, {"RicRoot": "1334"}]
            )
            assert (
                search_templates["Roots"]._search_kwargs(ric="1333.T")["filter"]
                == "RicRoot in ['1333', '1334']"
            )

    def test_locals_required_sub_arg(self):
        get_config().set_param(
            "search.templates",
            {
                "Roots": {
                    "request_body": {"Filter": "RicRoot eq '#{_.Root.RicRoot}'"},
                    "locals": {"Root": {"request_body": {"Filter": "RIC eq '#{ric}'"}}},
                }
            },
            auto_create=True,
        )
        with patch(
            "refinitiv.data.discovery._search_templates.search.search.Definition.get_data"
        ):
            with pytest.raises(KeyError):
                search_templates["Roots"]._search_kwargs()

    def test_unknown_subtemplate(self):
        get_config().set_param(
            "search.templates",
            {
                "RootsUnknownSubtemplate": {
                    "request_body": {"Filter": "RicRoot eq '#{_.Root.RicRoot}'"},
                    "locals": {},
                }
            },
            auto_create=True,
        )
        with pytest.raises(ValueError):
            search_templates["RootsUnknownSubtemplate"]._search_kwargs()

    def test_locals_nonused(self):
        get_config().set_param(
            "search.templates",
            {
                "Roots": {
                    "request_body": {"Filter": "RicRoot eq 'ABC'"},
                    "locals": {"Root": {"request_body": {}}},
                }
            },
            auto_create=True,
        )
        with patch(
            "refinitiv.data.discovery._search_templates.search.search.Definition.get_data"
        ) as mock:
            assert (
                search_templates["Roots"]._search_kwargs()["filter"]
                == "RicRoot eq 'ABC'"
            )
            mock.assert_not_called()

    def test_locals_only_in_if_detected(self):
        get_config().set_param(
            "search.templates",
            {
                "RootsWithIf": {
                    "request_body": {
                        "Filter": "{{if _.Shmoot.RicRoot.0}}RicRoot eq 'USD='{{endif}}"
                    },
                    "locals": {
                        "Shmoot": {"request_body": {"Filter": "RIC eq '#{ric}'"}}
                    },
                }
            },
            auto_create=True,
        )
        with patch(
            "refinitiv.data.discovery._search_templates.search.search.Definition.get_data"
        ):
            with pytest.raises(KeyError):
                search_templates["RootsWithIf"]._search_kwargs()
