import pytest

from refinitiv.data._tools.templates import InvalidPlaceholderError
from refinitiv.data.discovery._search_templates.base import (
    extract_used_templates_from_placeholders_and_namespace,
    TargetTemplate,
    Target,
)
from refinitiv.data.discovery._search_templates.namespaces import Namespace
from tests.unit.content.search.search_templates.catshelterdb import CatsDatabaseTarget


class TestExtractUsedTemplatesFromPlaceholdersAndNamespace:
    def test_basic(self):
        ns = Namespace(
            _=Namespace(
                One=TargetTemplate(name="One"),
            ),
            user=Namespace(
                sub=Namespace(
                    Two=TargetTemplate(name="Two"),
                ),
                Three=TargetTemplate(name="Three"),
            ),
        )
        names = {"_.One.col", "user.sub.Two.val"}
        assert extract_used_templates_from_placeholders_and_namespace(names, ns) == {
            "_.One",
            "user.sub.Two",
        }

    def test_simplest(self):
        assert (
            extract_used_templates_from_placeholders_and_namespace(
                {"pre.A.val"},
                Namespace(_=Namespace(A=TargetTemplate(name="A"))),
            )
            == set()
        )

    def test_uknown_subtemplate(self):
        with pytest.raises(ValueError):
            extract_used_templates_from_placeholders_and_namespace(
                {"_.A", "_.B"},
                Namespace(_=Namespace(A=TargetTemplate(name="A"))),
            )


class CatSearchTemplate(TargetTemplate):
    _target_class = CatsDatabaseTarget


class TestTargetTemplate:
    def test_basic(self):
        birman_cats = CatSearchTemplate(
            name="Search Birman cats",
            view="cats",
            filter="breed == 'Birman'",
        )
        assert set(birman_cats.search().breed) == {"Birman"}

    def test_repr(self):
        assert (
            repr(TargetTemplate(name="TT")) == "<TargetTemplate for Target name='TT'>"
        )

    def test_placeholders(self):
        search_by_breed = CatSearchTemplate(
            name="Search Birman cats",
            view="cats",
            filter="breed == '#{breed}'",
        )
        assert set(search_by_breed.search(breed="Sphynx").breed) == {"Sphynx"}

    def test_subtemplate_namespace(self):
        body_type_cats_tpl = CatSearchTemplate(
            name="Cats by body type",
            ns=Namespace(
                locals=Namespace(
                    BreedsByBodyType=CatSearchTemplate(
                        name="Breeds by body_type",
                        view="breeds",
                        filter="body_type == '#{body_type}'",
                    ),
                ),
            ),
            view="cats",
            filter="breed in (#{locals.BreedsByBodyType.name|in})",
        )
        assert body_type_cats_tpl._subtemplates_used == {"locals.BreedsByBodyType"}
        assert (
            body_type_cats_tpl._search_kwargs(body_type="dwarf")["filter"]
            == "breed in ('Munchkin')"
        )
        assert set(body_type_cats_tpl.search(body_type="dwarf").name) == {
            "Elsa",
            "Maverick",
        }

        body_type_in_city = CatSearchTemplate(
            name="Cats by body type",
            ns=Namespace(
                user=Namespace(
                    SheltersInCity=CatSearchTemplate(
                        name="Shelters in city",
                        view="shelters",
                        filter="city == '#{city}'",
                    )
                ),
                locals=Namespace(
                    BreedsByBodyType=CatSearchTemplate(
                        name="Breeds by body_type",
                        view="breeds",
                        filter="body_type == '#{body_type}'",
                    ),
                ),
            ),
            optional_placeholders=["city"],
            view="cats",
            filter="breed in (#{locals.BreedsByBodyType.name|in}){{if city}} and shelter in (#{user.SheltersInCity.name|in}){{endif}}",
        )

        # TODO: this must work, but it does not. Need to develop more complex logic for used templates detection
        # assert body_type_in_city._search_kwargs(body_type="dwarf")["filter"] == \
        #     "breed in ('Munchkin')"
        # assert set(body_type_in_city.search(body_type="dwarf").name) == {
        #     "Elsa", "Maverick",
        # }

        assert (
            body_type_in_city._search_kwargs(body_type="dwarf", city="Paris")["filter"]
            == "breed in ('Munchkin') and shelter in ('01', '03')"
        )
        assert set(body_type_in_city.search(body_type="dwarf", city="Paris").name) == {
            "Maverick",
        }


class DummyTarget(Target):
    """DummyTarget, call does nothing"""

    def __init__(self):
        super().__init__()
        self.args_names = {"filter", "boost", "top", "skip"}


class DummyTemplate(TargetTemplate):
    _target_class = DummyTarget


class TestTargetTemplateKwargs:
    """Test TargetTemplate API without calling Target"""

    def test_raise_error_for_default_not_in_definition(self):
        with pytest.raises(Exception):
            TargetTemplate(bad_argument=None)

    @pytest.mark.skip("other exception in jinja")
    def test_invalid_placeholder_syntax(self):
        with pytest.raises(InvalidPlaceholderError):
            TargetTemplate(boost="ExchangeName xeq '#???'")

    def test_applies_substitution_variables(self):
        template = DummyTemplate(
            filter="AssetState ne '#{state}' and SearchAllCategoryv2 eq '#{cat}'",
            boost="ExchangeName xeq '#{name}'",
        )
        assert template._search_kwargs(state="state", cat="cat", name="name") == {
            "filter": "AssetState ne 'state' and SearchAllCategoryv2 eq 'cat'",
            "boost": "ExchangeName xeq 'name'",
        }

    @pytest.mark.skip("jinja does not support alternative syntax")
    def test_escape_symbol(self):
        template = DummyTemplate(boost="#name and ##name")
        assert template._search_kwargs(name="name") == {"boost": "name and #name"}

    @pytest.mark.skip("jinja does not support alternative syntax")
    def test_applies_non_braced_variables(self):
        template = DummyTemplate(boost="ExchangeName xeq '#name'")
        assert template._search_kwargs(name="name") == {
            "boost": "ExchangeName xeq 'name'",
        }

    def test_exception_raised_if_sub_value_is_not_there(self):
        template = DummyTemplate(boost="ExchangeName xeq '#{name}'")
        with pytest.raises(Exception):
            template._search_kwargs()

    def test_cant_redefine_parameter_with_placeholders(self):
        template = DummyTemplate(boost="ExchangeName xeq '#{name}'")
        with pytest.raises(Exception):
            template._search_kwargs(boost=None, name="")  # no exception

    def test_non_template_arguments(self):
        template = DummyTemplate(top=3, skip=2)
        assert template._search_kwargs() == {"top": 3, "skip": 2}

    def test_tunnels_other_arguments(self):
        template = DummyTemplate(top=3)
        assert template._search_kwargs(skip=2) == {"top": 3, "skip": 2}

    def test_exception_on_bad_kwarg(self):
        template = DummyTemplate()
        with pytest.raises(Exception):
            template._search_kwargs(bad_argument_name=None)

    def test_templates_variables_with_same_name_as_search_argument(self):
        with pytest.raises(Exception):
            DummyTemplate(boost="ExchangeName xeq '#{top}'")

    def test_default_values(self):
        template = DummyTemplate(
            boost="ExchangeName xeq '#{exchange}'",
            placeholders_defaults={"exchange": 5},
        )
        assert template._search_kwargs() == {
            "boost": "ExchangeName xeq '5'",
        }

    def test_search_kwargs_result_changes_must_not_change_template(self):
        template = DummyTemplate(top=3, skip=2)
        result = template._search_kwargs()
        result["top"] = 5
        assert template._search_kwargs()["top"] == 3

    def test_bad_pass_through(self):
        with pytest.raises(Exception):
            template = DummyTemplate(pass_through_defaults={"bad_pass_through": 5})
