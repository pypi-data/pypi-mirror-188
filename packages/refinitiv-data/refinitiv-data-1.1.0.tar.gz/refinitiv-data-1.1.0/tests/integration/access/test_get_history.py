from datetime import timedelta, datetime

import allure
import pytest

import refinitiv.data as rd
from tests.integration.access.conftest import (
    check_column_names_is_exist_in_response_and_df_not_empty,
    check_rics_fields_order_respects_and_df_not_empty,
    check_df_index_names,
    check_df_contains_ohlc_columns_and_universes,
)
from tests.integration.helpers import (
    check_response_data_start_end_date,
    check_index_column_contains_dates,
    check_dataframe_column_date_for_datetime_type,
    check_if_dataframe_is_not_none,
    check_the_number_of_items_in_dataframe,
    check_universe_order_in_df,
)


@allure.suite("FinCoder layer")
@allure.feature("FinCoder layer - get_history")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.underlying_content("datagrid")
class TestGetHistory:
    @allure.title("Getting history for single instrument")
    @pytest.mark.parametrize(
        "universe,fields,expected_fields",
        [
            (["IBM.N", "EUR="], None, None),
            ("LSEG.L", None, None),
            ("LSEG.L", "TR.Revenue", "Revenue"),
        ],
    )
    @pytest.mark.caseid("C37270766_1")
    @pytest.mark.smoke
    def test_get_history_for_single_instrument_and_all_fields(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
        expected_fields,
    ):
        """
        result1 = rd.get_history(
            universe=["IBM.N", "EUR="], fields=None
        )
        result2 = rd.get_history(
            universe="LSEG.L", fields=None
        )
        result3 = rd.get_history(
            universe="LSEG.L", fields="TR.Revenue"
        )
        """
        response = rd.get_history(
            universe=universe, fields=fields, use_field_names_in_headers=False
        )
        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_index_column_contains_dates(response)
        check_if_dataframe_is_not_none(response)

    @allure.title("Getting history for multiple instruments with commingle fields")
    @pytest.mark.parametrize(
        "universe,fields,interval,start_date,end_date,expected_fields",
        [
            (
                "IBM",
                [
                    "BID",
                    "TR.RevenueMean.currency",
                    "TR.RevenueMean",
                    "TR.RevenueMean",
                ],
                "1h",
                timedelta(-10),
                timedelta(0),
                [
                    "BID",
                    "Currency",
                    "Revenue - Mean",
                ],
            ),
            (
                (
                    ["IBM", "VOD.L"],
                    [
                        "BID",
                        "TR.RevenueMean.currency",
                        "TR.RevenueMean",
                    ],
                    "hourly",
                    "2022-06-01T11:00:00",
                    "2022-06-06T11:00:00",
                    [
                        ("IBM", "BID"),
                        ("IBM", "Currency"),
                        ("IBM", "Revenue - Mean"),
                        ("VOD.L", "BID"),
                        ("VOD.L", "Currency"),
                        ("VOD.L", "Revenue - Mean"),
                    ],
                )
            ),
        ],
        ids=["timedelta", "string"],
    )
    @pytest.mark.caseid("37270766")
    @pytest.mark.smoke
    def test_get_history_for_multiple_instruments(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
        interval,
        start_date,
        end_date,
        expected_fields,
        request,
    ):
        """
        response1 = rd.get_history(
            universe="IBM",
            fields=[
                "BID",
                "TR.RevenueMean.currency",
                "TR.RevenueMean",
                "TR.RevenueMean",
            ],
            interval="1h",
            start=timedelta(-10),
            end=timedelta(0),
        )

        response2 = rd.get_history(
            universe=["IBM", "VOD.L"],
            fields=[
                "BID",
                "TR.RevenueMean.currency",
                "TR.RevenueMean",
            ],
            interval="hourly",
            start="2022-06-01T11:00:00",
            end="2022-06-06T11:00:00",
        )

        """
        response = rd.get_history(
            universe=universe,
            fields=fields,
            interval=interval,
            start=start_date,
            end=end_date,
        )

        check_df_index_names(response, interval)
        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_index_column_contains_dates(response)
        check_response_data_start_end_date(response, start_date, end_date, request)

    @allure.title("Getting history for instruments with platform session")
    @pytest.mark.parametrize(
        "universe,fields,interval,start_date,end_date,expected_fields",
        [
            (
                ["EUR=", "VOD.L"],
                [
                    "BID",
                    "TR.RevenueMean.currency",
                    "TR.RevenueMean",
                    "TR.RevenueMean",
                ],
                "daily",
                timedelta(-30),
                timedelta(0),
                [
                    ("EUR=", "BID"),
                    ("EUR=", "Currency"),
                    ("EUR=", "Revenue - Mean"),
                    ("VOD.L", "BID"),
                    ("VOD.L", "Currency"),
                    ("VOD.L", "Revenue - Mean"),
                ],
            )
        ],
        ids=["timedelta"],
    )
    @pytest.mark.caseid("C37270766_2")
    def test_get_history_for_instruments_with_platform_session(
        self,
        set_underlying_platform_config,
        open_platform_session_with_rdp_creds,
        universe,
        fields,
        interval,
        start_date,
        end_date,
        expected_fields,
        request,
    ):
        response = rd.get_history(
            universe=universe,
            fields=fields,
            interval=interval,
            start=start_date,
            end=end_date,
        )
        check_df_index_names(response, interval)
        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_index_column_contains_dates(response)
        check_response_data_start_end_date(response, start_date, end_date, request)

    @allure.title("Getting history with duplicated instruments")
    @pytest.mark.parametrize(
        "universes,fields,interval,start_date,end_date,expected_fields",
        [
            (
                (
                    ["IBM", "IBM", "VOD.L"],
                    [
                        "ASK",
                        "TR.RevenueMean.currency",
                        "TR.RevenueMean",
                    ],
                    "monthly",
                    datetime(2022, 3, 10),
                    datetime(2022, 5, 31),
                    [
                        ("IBM", "ASK"),
                        ("IBM", "Currency"),
                        ("IBM", "Revenue - Mean"),
                        ("IBM", "ASK"),
                        ("IBM", "Currency"),
                        ("IBM", "Revenue - Mean"),
                        ("VOD.L", "ASK"),
                        ("VOD.L", "Currency"),
                        ("VOD.L", "Revenue - Mean"),
                    ],
                )
            ),
        ],
        ids=["datetime"],
    )
    @pytest.mark.caseid("37270767")
    def test_get_history_with_duplicated_instruments(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universes,
        fields,
        interval,
        start_date,
        end_date,
        expected_fields,
        request,
    ):
        response = rd.get_history(
            universe=universes,
            fields=fields,
            interval=interval,
            start=start_date,
            end=end_date,
        )
        list_of_instruments = list(response.columns)
        check_the_number_of_items_in_dataframe(
            expected_fields[0], list_of_instruments, universes.count(universes[0])
        )
        check_index_column_contains_dates(response)
        check_response_data_start_end_date(response, start_date, end_date, request)
        check_df_index_names(response, interval)

    @allure.title("Getting history with invalid instrument")
    @pytest.mark.parametrize(
        "universe,fields,interval,start_date,end_date,expected_fields",
        [
            (
                (
                    ["IBM", "INVALID", "VOD.L"],
                    [
                        "BID",
                        "TR.RevenueMean",
                    ],
                    "1Y",
                    datetime(2018, 3, 10),
                    datetime(2021, 12, 31),
                    [
                        ("IBM", "BID"),
                        ("IBM", "Revenue - Mean"),
                        ("VOD.L", "BID"),
                        ("VOD.L", "Revenue - Mean"),
                        ("INVALID", "BID"),
                        ("INVALID", "Revenue - Mean"),
                    ],
                )
            )
        ],
        ids=["datetime"],
    )
    @pytest.mark.caseid("37270776")
    def test_get_history_with_invalid_instruments(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
        interval,
        start_date,
        end_date,
        expected_fields,
        request,
    ):
        response = rd.get_history(
            universe=universe,
            fields=fields,
            interval=interval,
            end=end_date,
            start=start_date,
        )

        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_index_column_contains_dates(response)
        check_response_data_start_end_date(response, start_date, end_date, request)
        check_df_index_names(response, interval)

    @allure.title("Getting pricing history for single and multiple instruments")
    @pytest.mark.parametrize(
        "universe,fields,interval,expected_fields",
        [
            (
                ["EUR="],
                ["BID", "ASK"],
                "daily",
                ["BID", "ASK"],
            ),
            (
                ["EUR=", "GBP="],
                ["BID", "ASK"],
                "daily",
                [("GBP=", "BID"), ("GBP=", "ASK"), ("EUR=", "BID"), ("EUR=", "ASK")],
            ),
            (
                ["EUR=", "GBP="],
                ["BID", "ASK"],
                "tick",
                [
                    ("GBP=", "BID"),
                    ("GBP=", "ASK"),
                    ("EUR=", "BID"),
                    ("EUR=", "ASK"),
                ],
            ),
        ],
    )
    @pytest.mark.caseid("37270777")
    def test_get_pricing_history_for_single_and_multiple_instruments(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
        interval,
        expected_fields,
    ):
        response = rd.get_history(
            universe=universe,
            fields=fields,
            interval=interval,
            start=datetime(2022, 5, 24),
        )

        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_index_column_contains_dates(response)
        check_df_index_names(response, interval)

    @allure.title("Getting history for pricing fields")
    @pytest.mark.parametrize(
        "universe,fields,interval,end",
        [
            (
                "IBM",
                ["HIGH_1", "LOW_1", "TRDPRC_1", "NUM_MOVES"],
                "daily",
                "2020-01-01",
            ),
            (
                ["LSEG.L", "VOD.L", "GOOG.O", "AAPL.OQ", "IBM.N"],
                ["ASK", "TRNOVR_UNS", "VWAP", "BLKCOUNT", "BLKVOLUM"],
                "1Y",
                "2022-01-01",
            ),
        ],
        ids=["single", "multiple"],
    )
    @pytest.mark.caseid("38386444")
    def test_get_history_pricing_fields(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        request,
        universe,
        fields,
        interval,
        end,
    ):
        response = rd.get_history(
            universe=universe, fields=fields, interval=interval, end=end
        )

        if "single" in request.node.callspec.id:
            check_column_names_is_exist_in_response_and_df_not_empty(response, fields)
        else:
            check_rics_fields_order_respects_and_df_not_empty(
                response, universe, fields
            )
        check_index_column_contains_dates(response)
        check_df_index_names(response, interval)

    @allure.title("Getting history for fundamental and reference fields")
    @pytest.mark.parametrize(
        "universe,fields,interval,use_field_names_in_headers,expected_fields_udf,expected_fields_rdp",
        [
            (
                "IBM",
                ["TR.Revenue.date", "TR.RevenueMean.currency", "TR.RevenueMean"],
                "daily",
                True,
                ["TR.REVENUEMEAN", "TR.REVENUE.DATE", "TR.REVENUEMEAN.currency"],
                ["TR.Revenue", "TR.RevenueMean"],
            ),
            (
                "GOOG.O",
                ["TR.Revenue.date", "TR.Revenue"],
                "daily",
                False,
                ["Date", "Revenue"],
                ["Date", "Revenue"],
            ),
            (
                ["LSEG", "GOOG.O"],
                "TR.Revenue",
                "daily",
                False,
                ["LSEG", "GOOG.O"],
                ["LSEG", "GOOG.O"],
            ),
        ],
        ids=["single_field_names", "single_field_titles", "multiple_title_names"],
    )
    @pytest.mark.caseid("38386491")
    def test_get_history_fundamental_and_reference_fields(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
        interval,
        use_field_names_in_headers,
        expected_fields_rdp,
        expected_fields_udf,
    ):
        response = rd.get_history(
            universe=universe,
            fields=fields,
            interval=interval,
            use_field_names_in_headers=use_field_names_in_headers,
        )
        expected_fields = expected_fields_udf
        if set_underlying_platform_config == "rdp-underlying-platform":
            expected_fields = expected_fields_rdp
        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_dataframe_column_date_for_datetime_type(response)

    @allure.title("Getting mix of pricing and fundamental history")
    @pytest.mark.parametrize(
        "universe,fields,interval,expected_fields",
        [
            (
                ["IBM", "EUR="],
                [
                    "BID",
                    "TR.RevenueMean.currency",
                ],
                "daily",
                [
                    ("EUR=", "BID"),
                    ("EUR=", "Currency"),
                    ("IBM", "BID"),
                    ("IBM", "Currency"),
                ],
            ),
            (
                (
                    ["VOD.L", "EUR="],
                    [
                        "BID",
                        "ASK",
                        "EVENT_TYPE",
                    ],
                    "tick",
                    [
                        ("EUR=", "EVENT_TYPE"),
                        ("EUR=", "BID"),
                        ("EUR=", "ASK"),
                        ("VOD.L", "EVENT_TYPE"),
                        ("VOD.L", "BID"),
                        ("VOD.L", "ASK"),
                    ],
                )
            ),
        ],
    )
    @pytest.mark.caseid("37270778")
    def test_get_mix_of_pricing_and_fundamental_history(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
        interval,
        expected_fields,
    ):
        response = rd.get_history(
            universe=universe,
            fields=fields,
            interval=interval,
        )

        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_index_column_contains_dates(response)
        check_df_index_names(response, interval)

    @allure.title("Getting history raises error on invalid fields list")
    @pytest.mark.parametrize(
        "universe,fields,interval",
        [
            (
                "IBM",
                ["INVALID_FIELD_1", "INVALID_FIELD_2"],
                "daily",
            ),
            (
                "INVAL",
                ["TR.Revenue.date", "TR.Revenue", "TR.GrossProfit"],
                "tick",
            ),
        ],
    )
    @pytest.mark.caseid("38386507")
    def test_get_history_with_invalid_fields(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
        interval,
    ):
        response = rd.get_history(universe=universe, fields=fields, interval=interval)

        assert response.empty, f"Response is empty: {response}"

    @allure.title("Getting history with resampling ohlc data")
    @pytest.mark.caseid("C43506364")
    @pytest.mark.parametrize(
        "universe,fields,interval,count",
        [
            (
                ["VOD.L", "GOOG.O"],
                ["BID", "ASK"],
                "tick",
                50,
            )
        ],
    )
    def test_get_history_with_bars_resampling(
        self,
        open_desktop_session,
        universe,
        fields,
        interval,
        count,
    ):
        response = rd.get_history(
            universe=universe, fields=fields, interval=interval, count=count
        )
        assert response.size == count * 2 * len(universe) * len(
            fields
        ), f"Inconsistency with the amount of returned data "
        dataframe = response.ohlc("2s")
        assert not response.empty, "Empty dataframe received"
        check_index_column_contains_dates(dataframe)
        check_df_contains_ohlc_columns_and_universes(dataframe, fields, universe)
        check_df_index_names(dataframe)
        check_universe_order_in_df(response, universe)

    @allure.title("Getting history by function and chain")
    @pytest.mark.parametrize(
        "universe,fields,expected_universe",
        [
            (
                'SCREEN(U(IN(Equity(active,public,primary))/*UNV:Public*/), IN(TR.HQCountryCode,"AR"), IN(TR.GICSIndustryCode,"401010"))',
                [
                    "TR.Revenue",
                    "BID",
                ],
                None,
            ),
            ('Peers("VOD.L")', ["BID", "TR.Revenue"], [("LBTYA.OQ", "BID")]),
            pytest.param(
                ["AAPL.OQ", "Peers('IBM')", "0#.DJI"],
                ["BID", "TR.Revenue"],
                [("AAPL.OQ", "BID"), ("CRM.N", "BID")],
                id="chain",
            ),
            (
                "GOOG.O",
                [
                    "ASK",
                    "BID",
                    "AVAIL(TR.GrossProfit(Period=LTM,Methodology=InterimSum)/TR.TotalRevenue(Period=LTM,Methodology=InterimSum),TR.GrossProfit(Period=FY0)/TR.TotalRevenue(Period=FY0))*100",
                ],
                ["ASK", "BID"],
            ),
        ],
    )
    @pytest.mark.caseid("37270766")
    @pytest.mark.smoke
    def test_get_history_by_function_and_chain(
        self,
        request,
        set_underlying_platform_config,
        open_desktop_session,
        universe,
        fields,
        expected_universe,
    ):
        response = rd.get_history(
            universe=universe,
            fields=fields,
        )

        check_index_column_contains_dates(response)
        check_if_dataframe_is_not_none(response)

        list_of_instruments = list(response.columns)
        if expected_universe:
            for ric in expected_universe:
                assert ric in list_of_instruments

        if "chain" in request.node.callspec.id:
            check_the_number_of_items_in_dataframe(
                expected_universe[0], list_of_instruments, len(universe)
            )

    @allure.title("Getting CustomInstrument data")
    @pytest.mark.parametrize(
        "universe",
        [([]), (["IBM", "EUR="])],
        ids=["ci_instruments", "mix_universes"],
    )
    @pytest.mark.caseid("C43973495_1")
    def test_get_custom_instrument_data(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        create_instrument,
        request,
        universe,
    ):
        symbol_01 = create_instrument()
        symbol_02 = create_instrument()
        universes = universe + [symbol_01, symbol_02]

        if "ci_instruments" in request.node.callspec.id:
            expected_fields = [
                (symbol_01, "TRDPRC_1"),
                (symbol_02, "TRDPRC_1"),
            ]
        else:
            expected_fields = None

        response = rd.get_history(universe=universes)

        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_fields
        )
        check_index_column_contains_dates(response)
        check_if_dataframe_is_not_none(response)
        check_df_index_names(response, interval="daily")

    @allure.title("Getting mix of pricing, fundamental and CustomInstrument history")
    @pytest.mark.parametrize(
        "universe,fields,interval,start_date,end_date,expected_fields",
        [
            (
                ["IBM", "EUR="],
                ["TR.Revenue", "TR.PriceClose", "TRDPRC_1"],
                "1M",
                datetime.strptime("01-01-2022 00:00:00", "%d-%m-%Y %H:%M:%S"),
                datetime.strptime("01-07-2022 00:00:00", "%d-%m-%Y %H:%M:%S"),
                [
                    ("IBM", "Revenue"),
                    ("IBM", "Price Close"),
                    ("IBM", "TRDPRC_1"),
                    ("EUR=", "Revenue"),
                    ("EUR=", "Price Close"),
                    ("EUR=", "TRDPRC_1"),
                ],
            ),
        ],
    )
    @pytest.mark.caseid("C43973495_2")
    def test_get_mix_of_pricing_custom_instrument_fundamental_history(
        self,
        set_underlying_platform_config,
        open_desktop_session,
        create_instrument,
        universe,
        fields,
        interval,
        start_date,
        end_date,
        expected_fields,
    ):
        symbol_01 = create_instrument()
        symbol_02 = create_instrument()
        universes = universe + [symbol_01, symbol_02]
        expected_data = expected_fields + [
            (symbol_01, "TRDPRC_1"),
            (symbol_01, "Price Close"),
            (symbol_01, "Revenue"),
            (symbol_02, "TRDPRC_1"),
            (symbol_02, "Price Close"),
            (symbol_02, "Revenue"),
        ]

        response = rd.get_history(
            universe=universes,
            fields=fields,
            interval=interval,
            start=start_date,
            end=end_date,
        )

        check_column_names_is_exist_in_response_and_df_not_empty(
            response, expected_data
        )
        check_index_column_contains_dates(response)
        check_df_index_names(response, interval)

    @allure.title("Getting history by function and chain without ADC fields")
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
    @pytest.mark.caseid("C54271588")
    def test_get_history_by_function_and_chain_without_adc_fields(
        self, open_session, universe, fields
    ):
        response = rd.get_history(
            universe=universe,
            fields=fields,
        )

        assert response.empty, f"Dataframe is not empty"
