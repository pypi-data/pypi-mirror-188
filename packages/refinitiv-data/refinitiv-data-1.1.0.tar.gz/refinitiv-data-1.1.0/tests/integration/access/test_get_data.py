import allure
import pytest

import refinitiv.data as rd
from tests.integration.access.conftest import (
    check_column_names_is_exist_in_response_and_df_not_empty,
)
from tests.integration.discovery.universe_expanders.conftest import FCHI_CONSTITUENTS
from tests.integration.helpers import (
    check_dataframe_column_date_for_datetime_type,
    check_if_dataframe_is_not_none,
    check_response_value,
)

FIELDS = [
    "BID",
    "TR.RevenueMean.currency",
    "TR.RevenueMean",
    "TR.RevenueMean",
    "TR.RevenueMean.date",
]
PARAMETERS = {
    "SCale": 6,
    "SDate": 0,
    "EDate": -3,
    "FRQ": "FY",
    "Curn": "USD",
}


@allure.suite("FinCoder layer")
@allure.feature("FinCoder layer - get_data")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("datagrid")
class TestGetData:
    @allure.title("Get mix of pricing and fundamental data")
    @pytest.mark.parametrize(
        "universe,fields,expected_fields",
        [
            (
                ["GOOG.O", "VOD.L", "EUR="],
                FIELDS,
                [
                    "Instrument",
                    "BID",
                    "Date",
                    "Currency",
                    "Revenue - Mean",
                ],
            ),
            (
                ["USD=", "EUR="],
                ["BID", "TR.Revenue"],
                [
                    "Instrument",
                    "BID",
                ],
            ),
        ],
    )
    @pytest.mark.caseid("36976688")
    @pytest.mark.smoke
    def test_get_mix_pricing_and_fundamental_data(
        self, open_desktop_session, universe, fields, expected_fields
    ):
        response = rd.get_data(
            universe=universe,
            fields=fields,
            parameters=PARAMETERS,
        )

        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_response_value(response, "Instrument", universe)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Get fundamental data with parameters")
    @pytest.mark.parametrize(
        "universe,fields,expected_fields",
        [
            (
                ["GOOG.O", "AAPL.O"],
                ["TR.PriceTargetMean(Source=ThomsonReuters)", "TR.Revenue.date"],
                ["Instrument", "Date", "Price Target - Mean"],
            ),
            (
                ["GOOG.O", "AAPL.O"],
                ["TR.Revenue(SDate=0, EDate=-3).date", "TR.Revenue(SDate=0, EDate=-3)"],
                ["Instrument", "Date", "Revenue"],
            ),
        ],
    )
    @pytest.mark.caseid("36976693")
    def test_get_fundamental_data_with_parameters(
        self, open_desktop_session, universe, fields, expected_fields
    ):
        response = rd.get_data(
            universe=universe,
            fields=fields,
        )

        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_response_value(response, "Instrument", universe)

    @allure.title("Get fundamental fields history")
    @pytest.mark.parametrize(
        "expected_fields",
        [["Instrument", "Date", "Revenue", "Gross Profit"]],
    )
    @pytest.mark.caseid("36976694")
    def test_get_fundamental_fields_history(
        self, open_desktop_session, expected_fields
    ):
        response = rd.get_data(
            universe=["GOOG.O", "AAPL.O"],
            fields=["TR.Revenue.date", "TR.Revenue", "TR.GrossProfit"],
        )

        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )

    @allure.title("Get fundamental data with one of the invalid universe")
    @pytest.mark.parametrize(
        "expected_fields",
        [["Instrument", "Date", "Revenue", "Gross Profit"]],
    )
    @pytest.mark.caseid("36976695")
    def test_get_fundamental_fields_data_with_one_of_the_invalid_universe(
        self, open_desktop_session, expected_fields
    ):
        response = rd.get_data(
            universe=["GOOG.O", "INVALID"],
            fields=["TR.Revenue.date", "TR.Revenue", "TR.GrossProfit"],
        )

        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )

    @allure.title("Get fundamental data with one invalid universe")
    @pytest.mark.caseid("36976696")
    def test_get_fundamental_fields_data_with_one_invalid_universe(
        self, open_desktop_session
    ):
        response = rd.get_data(
            universe="INVALID",
            fields=["TR.Revenue.date", "TR.Revenue", "TR.GrossProfit"],
        )

        assert response.empty, f"Response is not empty: {response}"

    @allure.title("Get fundamental data only with universe")
    @pytest.mark.parametrize(
        "universe,fields",
        [(["GOOG.O", "VOD.L"], None), ("GOOG.O", [])],
    )
    @pytest.mark.caseid("37039589")
    def test_get_fundamental_data_only_with_universe(
        self, open_desktop_session, universe, fields
    ):
        response = rd.get_data(universe=universe, fields=fields)

        assert not response.empty, f"{response}"
        check_response_value(response, "Instrument", universe)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Get mix of pricing and fundamental data with parameter use_field_names_in_headers"
    )
    @pytest.mark.parametrize(
        "universe,expected_fields_udf,expected_fields_rdp",
        [
            (
                ["GOOG.O", "VOD.L", "EUR="],
                [
                    "Instrument",
                    "BID",
                    "TR.REVENUEMEAN.currency",
                    "TR.REVENUEMEAN",
                    "TR.REVENUEMEAN.DATE",
                ],
                [
                    "Instrument",
                    "BID",
                    "TR.RevenueMean",
                ],
            )
        ],
    )
    @pytest.mark.caseid("40099771")
    def test_get_mix_pricing_and_fundamental_data_with_use_field_names_in_headers(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        expected_fields_udf,
        expected_fields_rdp,
    ):
        response = rd.get_data(
            universe=universe,
            fields=FIELDS,
            parameters=PARAMETERS,
            use_field_names_in_headers=True,
        )
        expected_fields = expected_fields_udf
        if set_underlying_platform_config == "rdp-underlying-platform":
            expected_fields = expected_fields_rdp
        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_response_value(response, "Instrument", universe)

    @allure.title("Getting data by function and chain")
    @pytest.mark.parametrize(
        "universe,fields,expected_universe",
        [
            pytest.param(
                "0#.FCHI",
                ["BID", "ASK", "TR.Revenue"],
                FCHI_CONSTITUENTS,
                id="discovery_iterable",
            ),
            (
                'Peers("VOD.L")',
                ["BID", "ASK", "TR.Revenue"],
                ["LBTYA.OQ", "VTWRn.F", "TELIA.ST"],
            ),
            (
                'SCREEN(U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010"))',
                [
                    "TR.CommonName",
                    "TR.HeadquartersCountry",
                    "TR.GICSSector",
                    "TR.OrganizationStatusCode",
                    "TR.Revenue",
                    "BID",
                ],
                ["BMA.BA", "BBAR.BA", "BHIP.BA"],
            ),
            (
                "VOD.L",
                [
                    "TR.PeersRank",
                    "TR.RIC",
                    "AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum)/TR.TotalRevenue(Period=LTM,Methodology=InterimSum),TR.GrossProfit(Period=FY0)/TR.TotalRevenue(Period=FY0))*100",
                ],
                ["VOD.L"],
            ),
        ],
    )
    @pytest.mark.caseid("C43844230")
    @pytest.mark.smoke
    def test_get_data_by_function_and_chain(
        self,
        request,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
        expected_universe,
    ):
        if "discovery_iterable" in request.node.callspec.id:
            chain = rd.discovery.Chain(name=universe)
            list(chain.constituents)
            universe = chain

        response = rd.get_data(
            universe=universe,
            fields=fields,
        )

        list_of_instruments = list(response["Instrument"])
        check_if_dataframe_is_not_none(response)

        if expected_universe:
            for universe in expected_universe:
                assert (
                    universe in list_of_instruments
                ), f"The {universe} is missing in requested instruments"

    @allure.title("Getting data by function and chain without ADC fields")
    @pytest.mark.parametrize(
        "universe,fields",
        [
            ("0#.FCHI", ["BID", "ASK"]),
            ('Peers("VOD.L")', None),
            (
                'SCREEN(U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010"))',
                [
                    "ASK" "BID",
                ],
            ),
        ],
    )
    @pytest.mark.caseid("C54271593")
    def test_get_data_by_function_and_chain_without_adc_fields(
        self, open_session, universe, fields
    ):
        response = rd.get_data(
            universe=universe,
            fields=fields,
        )

        assert response.empty, f"Dataframe is not empty"

    @allure.title("Getting data with SCREEN which return empty response data from ADC")
    @pytest.mark.parametrize(
        "universe,fields",
        (
            [
                'SCREEN(U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401020"))',
                ["TR.RIC"],
            ],
        ),
    )
    @pytest.mark.caseid("C43844230")
    def test_get_data_with_screen_which_return_empty_response(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
    ):
        response = rd.get_data(
            universe=universe,
            fields=fields,
        )

        assert response.empty, f"Response is not empty: {response}"

    @allure.title("Get Custom Instrument with mix of objects data")
    @pytest.mark.parametrize(
        "universes,fields,expected_fields",
        [
            ("S)universe", None, None),
            (None, ["TRDPRC_1", "INVALID"], ["Instrument", "TRDPRC_1", "INVALID"]),
            (
                ["IBM.N", "LSEG.L"],
                ["BID", "ASK"],
                ["Instrument", "BID", "ASK"],
            ),
        ],
        ids=["invalid", "partial_valid", "mix_objects"],
    )
    @pytest.mark.caseid("C43973494")
    def test_get_custom_instrument_with_mix_objects_data(
        self,
        open_desktop_session,
        create_instrument,
        universes,
        fields,
        expected_fields,
        request,
    ):
        if "partial_valid" in request.node.callspec.id:
            universes = [create_instrument(), create_instrument()]
        if "mix_objects" in request.node.callspec.id:
            universes += [create_instrument(), create_instrument()]

        response = rd.get_data(
            universe=universes,
            fields=fields,
        )
        if "invalid" in request.node.callspec.id:
            assert response.empty, f"Response is not empty: {response}"
        else:
            check_column_names_is_exist_in_response_and_df_not_empty(
                response, expected_fields
            )
            check_response_value(response, "Instrument", universes)
