import allure
import pytest

from refinitiv.data.content import fundamental_and_reference
from refinitiv.data.errors import RDError
from tests.integration.conftest import set_rdp_config, set_udf_config
from tests.integration.constants_list import HttpStatusCode, HttpReason
from tests.integration.helpers import (
    check_response_dataframe_columns_date_as_index,
    check_index_column_contains_dates,
    check_response_dataframe_universe_date_as_index,
    check_response_dataframe_contains_columns_names,
)
from tests.integration.helpers import (
    get_async_response_from_definition,
    get_async_response_from_definitions,
    check_response_status,
    check_non_empty_response_data,
    check_dataframe_column_date_for_datetime_type,
)

DOW_JONES_CONSTITUENTS = [
    "GS.N",
    "NKE.N",
    "CSCO.OQ",
    "JPM.N",
    "DIS.N",
    "INTC.OQ",
    "DOW.N",
    "MRK.N",
    "CVX.N",
    "AXP.N",
    "VZ.N",
    "HD.N",
    "WBA.OQ",
    "MCD.N",
    "UNH.N",
    "KO.N",
    "JNJ.N",
    "MSFT.OQ",
    "HON.OQ",
    "CRM.N",
    "PG.N",
    "IBM.N",
    "MMM.N",
    "AAPL.OQ",
    "WMT.N",
    "CAT.N",
    "AMGN.OQ",
    "V.N",
    "TRV.N",
    "BA.N",
]


@allure.suite("Content object - Fundamental and Reference")
@allure.feature("Content object - Fundamental and Reference")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("datagrid")
class TestFundamentalAndReference:
    @allure.title(
        "Create fundamental_and_reference definition object with valid params - synchronously"
    )
    @pytest.mark.caseid("37935805")
    @pytest.mark.parametrize(
        "universe,fields,row_headers,expected_column_names",
        [
            ("AMZN.O", "TR.Revenue", ["date"], "Revenue"),
            (
                    ["TRI.N", "IBM.N", "GOOG.O", "AAPL.O"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    "date",
                    ["Revenue", "Gross Profit"],
            ),
        ],
    )
    @pytest.mark.smoke
    def test_fundamental_and_reference_definition_object_with_valid_params_and_get_data(
            self,
            set_underlying_platform_config,
            open_desktop_session,
            universe,
            fields,
            row_headers,
            expected_column_names,
    ):
        response = fundamental_and_reference.Definition(
            universe=universe, fields=fields, row_headers=row_headers
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_columns_date_as_index(
            response, universe, expected_column_names
        )
        check_response_dataframe_universe_date_as_index(response, universe)

    @allure.title(
        "Create fundamental_and_reference definition object with chain as universe - asynchronously"
    )
    @pytest.mark.caseid("37935806")
    @pytest.mark.parametrize(
        "universe,fields,row_headers,expected_column_names",
        [
            (
                    ["0#.DJI"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    ["date"],
                    ["Revenue", "Gross Profit"],
            ),
            (
                    ["0#.DJI"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    None,
                    ["Revenue", "Gross Profit"],
            ),
        ],
    )
    async def test_fundamental_and_reference_definition_object_with_chain_and_get_data_async(
            self,
            set_underlying_platform_config,
            open_desktop_session_async,
            universe,
            fields,
            row_headers,
            expected_column_names,
    ):
        response = await get_async_response_from_definition(
            fundamental_and_reference.Definition(
                universe=universe, fields=fields, row_headers=row_headers
            )
        )

        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)

        if row_headers is not None:
            check_response_dataframe_columns_date_as_index(
                response, DOW_JONES_CONSTITUENTS, expected_column_names
            )
            check_response_dataframe_universe_date_as_index(
                response, DOW_JONES_CONSTITUENTS
            )
        else:
            check_response_dataframe_contains_columns_names(
                response, expected_column_names
            )

    @allure.title(
        "Create fundamental_and_reference definition object with global/local parameters"
    )
    @pytest.mark.caseid("37935808")
    @pytest.mark.parametrize(
        "universe,fields,parameters,expected_column_names",
        [
            (
                    ["GOOG.O", "AAPL.O"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    {"SDate": "0CY", "Curn": "CAD"},
                    ["Revenue", "Gross Profit"],
            ),
            (
                    ["GOOG.O", "AAPL.O"],
                    ["TR.PriceTargetMean(SDate:0CY)", "TR.LOWPRICE(SDate:0d)"],
                    None,
                    ["Price Target - Mean", "Low Price"],
            ),
        ],
    )
    def test_fundamental_and_reference_definition_object_with_global_or_local_parameters(
            self,
            set_underlying_platform_config,
            open_desktop_session,
            universe,
            fields,
            parameters,
            expected_column_names,
    ):
        response = fundamental_and_reference.Definition(
            universe, fields, parameters
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column_names)

    @allure.title(
        "Create fundamental_and_reference definition object and get timeseries data"
    )
    @pytest.mark.caseid("37935809")
    @pytest.mark.parametrize(
        "universe,fields,parameters,row_headers,expected_column_names",
        [
            (
                    ["GOOG.O", "MSFT.O", "FB.O", "AMZN.O", "TWTR.K"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    {"Scale": 6, "SDate": 0, "EDate": -3, "FRQ": "FY", "Curn": "EUR"},
                    [fundamental_and_reference.RowHeaders.DATE],
                    ["Revenue", "Gross Profit"],
            )
        ],
    )
    def test_fundamental_and_reference_definition_object_and_get_timeseries_data(
            self,
            set_underlying_platform_config,
            open_desktop_session,
            universe,
            fields,
            parameters,
            row_headers,
            expected_column_names,
    ):
        response = fundamental_and_reference.Definition(
            universe, fields, parameters, row_headers
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_universe_date_as_index(response, universe)
        check_response_dataframe_columns_date_as_index(
            response, universe, expected_column_names
        )
        check_index_column_contains_dates(response)

    @allure.title(
        "Create fundamental_and_reference definition object with invalid params and get error"
    )
    @pytest.mark.caseid("37935811")
    @pytest.mark.parametrize(
        "set_platform_config,universe,fields,expected_error",
        [
            (
                    set_rdp_config,
                    [],
                    ["", "INVALID"],
                    "Error code -1 | No data item defined. Requested universes: []. Requested fields: ['', 'INVALID']",
            ),
            (
                    set_rdp_config,
                    ["INVALID"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    "Error code 412 | Unable to resolve all requested identifiers in ['INVALID'].",
            ),
            (
                    set_rdp_config,
                    ["GOOG.O"],
                    ["TR.INVALID"],
                    "Error code 218 | Unable to resolve all requested fields in ['TR.INVALID']. The formula must contain at least one field or function.",
            ),
            (
                    set_udf_config,
                    [],
                    ["", "INVALID"],
                    "Error code 400 | Validation error Requested universes: []. Requested fields: ['', 'INVALID']",
            ),
            (
                    set_udf_config,
                    ["INVALID"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    "Error code 412 | Unable to resolve all requested identifiers in ['INVALID'].",
            ),
            (
                    set_udf_config,
                    ["GOOG.O"],
                    ["TR.INVALID"],
                    "Error code 218 | Unable to resolve all requested fields in ['TR.INVALID']. The formula must contain at least one field or function.",
            ),
        ],
    )
    def test_fundamental_and_reference_definition_object_with_invalid_params_and_get_error(
            self,
            set_platform_config,
            universe,
            fields,
            expected_error,
            open_desktop_session,
    ):
        set_platform_config("datagrid")
        with pytest.raises(RDError) as error:
            fundamental_and_reference.Definition(
                universe=universe, fields=fields
            ).get_data()

        assert str(error.value) == expected_error

    @allure.title(
        "Create fundamental_and_reference definition object using closed session"
    )
    @pytest.mark.caseid("37935812")
    async def test_fundamental_and_reference_definition_object_using_closed_session(
            self, set_underlying_platform_config, open_desktop_session_async
    ):
        session = open_desktop_session_async
        await session.close_async()
        definition = fundamental_and_reference.Definition([], [])
        with pytest.raises(
                ValueError, match="Session is not opened. Can't send any request"
        ):
            await get_async_response_from_definition(definition)

    @allure.title(
        "Create fundamental_and_reference definition object with extended params"
    )
    @pytest.mark.caseid("37935813")
    @pytest.mark.parametrize(
        "universe,fields,parameters,expected_column_names,extended_params_universe",
        [
            (
                    ["MSFT.O", "FB.O", "AMZN.O", "TWTR.K"],
                    ["TR.Revenue", "TR.Revenue.date", "TR.GrossProfit"],
                    {"Scale": 6, "SDate": 0, "EDate": -3, "FRQ": "FY", "Curn": "EUR"},
                    ["Revenue", "Gross Profit"],
                    ["GOOG.O", "AAPL.O"],
            )
        ],
    )
    def test_fundamental_and_reference_definition_object_with_extended_params(
            self,
            set_underlying_platform_config,
            open_desktop_session,
            universe,
            fields,
            parameters,
            expected_column_names,
            extended_params_universe,
    ):
        extended_params = {"universe": extended_params_universe}
        response = fundamental_and_reference.Definition(
            universe, fields, parameters, extended_params=extended_params
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(response, expected_column_names)
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title(
        "Create fundamental_and_reference definition object with use_field_names_in_headers True"
    )
    @pytest.mark.caseid("38359418")
    @pytest.mark.parametrize(
        "universe,fields,parameters,row_headers,expected_column_names",
        [
            (
                    ["GOOG.O", "MSFT.O", "FB.O", "AMZN.O", "TWTR.K"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    {"Scale": 6, "SDate": 0, "EDate": -3, "FRQ": "FY", "Curn": "EUR"},
                    "date",
                    ["TR.Revenue", "TR.GrossProfit"],
            )
        ],
    )
    def test_fundamental_and_reference_definition_object_with_use_field_names_in_headers_true(
            self,
            set_underlying_platform_config,
            open_desktop_session,
            universe,
            fields,
            parameters,
            row_headers,
            expected_column_names,
    ):
        response = fundamental_and_reference.Definition(
            universe, fields, parameters, row_headers, use_field_names_in_headers=True
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_columns_date_as_index(
            response, universe, expected_column_names
        )
        check_response_dataframe_universe_date_as_index(response, universe)
        check_index_column_contains_dates(response)

    @allure.title(
        "Create fundamental_and_reference definition object with use mix valid and invalid data and get partial result"
    )
    @pytest.mark.caseid("39506181")
    @pytest.mark.parametrize(
        "universe,fields,expected_columns_names",
        [
            (
                    ["GOOG.O", "INVAL", "FB.O", "AMZN.O", "TWTR.K"],
                    ["TR.GrossProfit", "INVALID_FIELD"],
                    ["Instrument", "TR.GrossProfit"],
            )
        ],
    )
    def test_fundamental_and_reference_definition_object_with_use_mix_valid_and_invalid_data(
            self,
            set_underlying_platform_config,
            open_desktop_session,
            universe,
            fields,
            expected_columns_names,
    ):
        response = fundamental_and_reference.Definition(
            universe, fields, use_field_names_in_headers=True
        ).get_data()
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)
        check_response_dataframe_contains_columns_names(
            response, expected_columns_names
        )

        assert (
                response.errors[0][1]
                == "Unable to collect data for the field 'TR.GrossProfit' and some specific identifier(s)."
        )

    @allure.title(
        "Create async fundamental_and_reference definition object with invalid params and get error"
    )
    @pytest.mark.caseid("37935811")
    @pytest.mark.parametrize(
        "set_platform_config,universe,fields,expected_error",
        [
            (
                    set_rdp_config,
                    [],
                    ["", "INVALID"],
                    "No data item defined. Requested universes: []. Requested fields: ['', 'INVALID']",
            ),
            (
                    set_rdp_config,
                    ["INVALID"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    "Unable to resolve all requested identifiers in ['INVALID'].",
            ),
            (
                    set_rdp_config,
                    ["GOOG.O"],
                    ["TR.INVALID"],
                    "Unable to resolve all requested fields in ['TR.INVALID']. The formula must contain at least one field or function.",
            ),
            (
                    set_udf_config,
                    [],
                    ["", "INVALID"],
                    "Validation error Requested universes: []. Requested fields: ['', 'INVALID']",
            ),
            (
                    set_udf_config,
                    ["INVALID"],
                    ["TR.Revenue", "TR.GrossProfit"],
                    "Unable to resolve all requested identifiers in ['INVALID'].",
            ),
            (
                    set_udf_config,
                    ["GOOG.O"],
                    ["TR.INVALID"],
                    "Unable to resolve all requested fields in ['TR.INVALID']. The formula must contain at least one field or function.",
            ),
        ],
    )
    async def test_async_fundamental_and_reference_definition_object_with_invalid_params_and_get_error(
            self,
            set_platform_config,
            universe,
            fields,
            expected_error,
            open_desktop_session_async,
    ):
        set_platform_config("datagrid")
        task_result = await get_async_response_from_definitions(
            fundamental_and_reference.Definition(universe=universe, fields=fields),
            fundamental_and_reference.Definition(universe=universe, fields=fields),
        )

        for result in task_result:
            for error in result.errors:
                assert expected_error in error, f"Actual error {error}"

    @allure.title(
        "Create fundamental_and_reference definition object with SCREEN to force ticket workflow on UDF"
    )
    @pytest.mark.caseid("")
    @pytest.mark.parametrize(
        "set_platform_config,universe,fields",
        [
            (
                    set_udf_config,
                    [
                        'SCREEN(U(IN(Equity(active,public,private,primary))/*UNV:PublicPrivate*/), Contains(TR.BusinessSummary,"polymer"), CURN=USD)'
                    ],
                    [
                        "TR.CommonName",
                        "TR.HeadquartersCountry",
                        "TR.GICSSector",
                        "TR.OrganizationStatusCode",
                        "TR.Revenue",
                    ],
            )
        ],
    )
    def test_fundamental_and_reference_definition_object_with_screen_universe_get_data(
            self,
            set_platform_config,
            universe,
            fields,
            open_desktop_session,
    ):
        set_platform_config("datagrid")
        response = fundamental_and_reference.Definition(
            universe=universe, fields=fields
        ).get_data()
        assert response.is_success
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)

    @allure.title(
        "Create fundamental_and_reference definition object with SCREEN to force ticket workflow on UDF - asynchronously"
    )
    @pytest.mark.caseid("")
    @pytest.mark.parametrize(
        "set_platform_config,universe,fields",
        [
            (
                    set_udf_config,
                    [
                        'SCREEN(U(IN(Equity(active,public,private,primary))/*UNV:PublicPrivate*/), Contains(TR.BusinessSummary,"polymer"), CURN=USD)'
                    ],
                    [
                        "TR.CommonName",
                        "TR.HeadquartersCountry",
                        "TR.GICSSector",
                        "TR.OrganizationStatusCode",
                        "TR.Revenue",
                    ],
            )
        ],
    )
    async def test_fundamental_and_reference_definition_object_with_screen_universe_get_data_async(
            self,
            set_platform_config,
            universe,
            fields,
            open_desktop_session_async,
    ):
        set_platform_config("datagrid")
        response = await get_async_response_from_definition(
            fundamental_and_reference.Definition(universe=universe, fields=fields)
        )
        assert response.is_success
        check_response_status(response, HttpStatusCode.TWO_HUNDRED, HttpReason.OK)
        check_non_empty_response_data(response)

    @allure.title(
        "Create fundamental_and_reference definition object with Peers and Screen function as universe"
    )
    @pytest.mark.parametrize(
        "universe,fields,row_headers",
        [
            (
                    'Peers("VOD.L")',
                    [
                        "TR.CommonName",
                        "TR.HeadquartersCountry",
                        "TR.GICSSector",
                        "TR.OrganizationStatusCode",
                        "TR.Revenue",
                    ],
                    ["date"],
            ),
            (
                    'SCREEN(U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010"))',
                    [
                        "TR.CommonName",
                        "TR.HeadquartersCountry",
                        "TR.GICSSector",
                        "TR.OrganizationStatusCode",
                        "TR.Revenue",
                    ],
                    None,
            ),
            (
                    "VOD.L",
                    [
                        "TR.PeersRank",
                        "TR.RIC",
                        "AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum)/TR.TotalRevenue(Period=LTM,Methodology=InterimSum),TR.GrossProfit(Period=FY0)/TR.TotalRevenue(Period=FY0))*100",
                    ],
                    [fundamental_and_reference.RowHeaders.DATE],
            ),
        ],
    )
    @pytest.mark.caseid("C43855964")
    @pytest.mark.smoke
    def test_fundamental_and_reference_definition_object_with_peers_and_screen_and_get_data(
            self,
            set_underlying_platform_config,
            open_desktop_session,
            universe,
            fields,
            row_headers,
    ):
        response = fundamental_and_reference.Definition(
            universe=universe, fields=fields, row_headers=row_headers
        ).get_data()

        if row_headers:
            check_index_column_contains_dates(response)
        check_non_empty_response_data(response)

        if not row_headers:
            if set_underlying_platform_config == "rdp-underlying-platform":
                links_count = response.data.raw['links']['count']
            else:
                links_count = response.data.raw['totalColumnsCount']

            assert response.data.df.shape[0] == links_count
