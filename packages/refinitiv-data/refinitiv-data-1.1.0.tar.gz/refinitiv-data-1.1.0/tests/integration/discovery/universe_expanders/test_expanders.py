import allure
import pytest

import refinitiv.data as rd
from refinitiv.data.errors import RDError
from refinitiv.data.discovery import Peers, Screener
from tests.integration.access.conftest import (
    check_column_names_is_exist_in_response_and_df_not_empty,
)
from tests.integration.discovery.universe_expanders.conftest import (
    check_chain_discovery_object_for_attributes,
    is_iterable,
    FCHI_CONSTITUENTS,
    FCHI_SUMMARY_LINKS,
    LSEG_PEERS_INSTRUMENTS,
)
from tests.integration.helpers import compare_list


@allure.suite("Discovery layer")
@allure.feature("Discovery layer - Universe Expander")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("datagrid")
class TestExpanders:
    @allure.title(
        "Create discovery chain object depend on scopes with different endpoints"
    )
    @pytest.mark.parametrize(
        "chain_name,scope,account",
        [
            ("0#.FCHI", "trapi.streaming.pricing.read", "machine"),
            (
                "0#.FCHI",
                "trapi.data.get.data.read",
                "eikon",
            ),
            pytest.param(
                "0#.FCHI",
                "trapi.data.pricing.read",
                "machine",
                marks=pytest.mark.skip(
                    reason="https://jira.refinitiv.com/browse/EAPI-4919"
                ),
            ),
        ],
        ids=[
            "get_chain_data_from_stream",
            "get_chain_data_from_adc",
            "get_chain_data_from_chain_endpoint",
        ],
    )
    @pytest.mark.caseid("C52511279")
    @pytest.mark.smoke
    def test_create_discovery_chain_object_depend_on_scopes_with_different_endpoints(
        self,
        request,
        create_session_with_scope,
        chain_name,
        scope,
        account,
    ):
        create_session_with_scope(scope=scope, acc=account)
        chain = rd.discovery.Chain(name=chain_name)
        list(chain.constituents)

        assert is_iterable(chain), "Chain object is not iterable"
        check_chain_discovery_object_for_attributes(
            chain, chain_name, FCHI_CONSTITUENTS
        )

        if "get_chain_data_from_stream" in request.node.callspec.id:
            compare_list(chain.summary_links, FCHI_SUMMARY_LINKS)

    @allure.title("Create discovery peers/screener object and get mix of pricing data")
    @pytest.mark.parametrize(
        "function,expression,fields,expected_universe",
        [
            (Peers, "LSEG.L", None, LSEG_PEERS_INSTRUMENTS),
            (
                Screener,
                'U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010")',
                [
                    "TR.CommonName",
                    "TR.HeadquartersCountry",
                    "TR.GICSSector",
                    "TR.OrganizationStatusCode",
                    "TR.Revenue",
                    "BID",
                ],
                ["BMA.BA", "BBAR.BA", "BHIP.BA", "GGAL.BA", "BPAT.BA", "SUPV.BA"],
            ),
        ],
    )
    @pytest.mark.caseid("C52511280")
    @pytest.mark.smoke
    def test_create_discovery_peers_screeners_objects_and_get_data(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        function,
        expression,
        fields,
        expected_universe,
    ):
        discovery_obj = function(expression=expression)
        actual_expression = discovery_obj.expression

        assert is_iterable(discovery_obj), f"{function} object is not iterable"
        assert (
            expression in actual_expression
        ), f"{expression} is missing for {function} object"
        assert (discovery_obj._universe, expected_universe)

        response = rd.get_data(
            universe=discovery_obj,
            fields=fields,
        )
        list_of_instruments = list(response["Instrument"])
        assert (list_of_instruments, expected_universe)
        check_column_names_is_exist_in_response_and_df_not_empty(response)

    @allure.title("Create discovery chain object with invalid name and get error")
    @pytest.mark.caseid("C52511281")
    @pytest.mark.parametrize("chain_name", ["invalid"])
    def test_create_chain_object_with_invalid_name_and_get_error(
        self, open_desktop_session, chain_name
    ):
        with pytest.raises(RDError) as error:
            chain = rd.discovery.Chain(name=chain_name)
            list(chain.constituents)
        assert str(error.value) == "Error code -1 | No values to unpack"

    @allure.title(
        "Create discovery peers/screeners object with invalid name and get error"
    )
    @pytest.mark.caseid("C52511297")
    @pytest.mark.parametrize(
        "function,error_message",
        [
            (
                Peers,
                "Error code 413 | Unable to resolve some identifier(s). Requested universes: peers(invalid). Requested fields: TR.RIC",
            ),
            (
                Screener,
                "Error code 800 | SCREEN(INVALID) processing failed. Requested universes: screen(invalid). Requested fields: TR.RIC",
            ),
        ],
    )
    def test_create_discovery_object_with_invalid_name_and_get_error(
        self, open_desktop_session, function, error_message
    ):
        with pytest.raises(RDError) as error:
            discovery_obj = function(expression="invalid")
            list(discovery_obj)
        assert str(error.value) == error_message
