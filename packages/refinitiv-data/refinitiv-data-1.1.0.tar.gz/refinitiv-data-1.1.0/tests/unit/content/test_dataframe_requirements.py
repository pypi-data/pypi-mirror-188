import numpy as np
import pandas as pd
import pytest

from refinitiv.data._content_type import ContentType
from refinitiv.data.content._df_build_type import DFBuildType
from refinitiv.data.content._df_builder_factory import get_dfbuilder
from tests.unit.content.data_for_tests import (
    NONE_REPLACED_WITH_NA_RDP_DATA,
    NONE_REPLACED_WITH_NA_UDF_DATA,
    NAN_REPLACED_WITH_NA_RDP_DATA,
    NAN_REPLACED_WITH_NA_UDF_DATA,
    EMPTY_STRING_LEAVE_AS_IT_IS_RDP_DATA,
    EMPTY_STRING_LEAVE_AS_IT_IS_UDF_DATA,
    INSTRUMENT_AND_CURRENCY_ARE_EMPTY_STRINGS_RDP_DATA,
    INSTRUMENT_AND_CURRENCY_ARE_EMPTY_STRINGS_UDF_DATA,
    TWO_SAME_DATES_DOES_NOT_MERGE_IN_ONE_RDP_DATA,
    TWO_SAME_DATES_DOES_NOT_MERGE_IN_ONE_UDF_DATA,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA,
    DELETE_ROW_IF_DATE_IS_NONE_UDF_DATA,
    DELETE_ROW_IF_DATE_IS_NONE_RDP_DATA,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_4,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_4,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_3,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_3,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_2,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_2,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_1,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_1,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_5,
    MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_5,
    TWO_UNIVERSES_ONE_FIELD_RDP_DATA,
    TWO_UNIVERSES_ONE_FIELD_UDF_DATA,
)

"""
https://confluence.refinitiv.com/display/EF/RD+Lib+Python+-+Technical+Requirements+-+DataFrame+Requirements
"""


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, NONE_REPLACED_WITH_NA_RDP_DATA),
        (ContentType.DATA_GRID_UDF, NONE_REPLACED_WITH_NA_UDF_DATA),
    ],
    ids=["None replaced with NA. RDP", "None replaced with NA. UDF"],
)
def test_none_replaced_with_na(content_type, input_data, dfbuild_type):
    # when
    dataframe_build = get_dfbuilder(content_type, dfbuild_type)
    """
    #### INDEX ####
    
      Instrument       Date Currency
    0     GOOG.O 2020-01-20     <NA>
    1     GOOG.O 2020-12-31     <NA>
    
    #### DATE_AS_INDEX #### 
    
    GOOG.O     Currency
    Date               
    2020-12-31     <NA>
    2020-01-20     <NA>
    """
    testing_df = dataframe_build(input_data)

    # then
    assert testing_df["Currency"][0] is pd.NA
    assert testing_df["Currency"][1] is pd.NA


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, NAN_REPLACED_WITH_NA_RDP_DATA),
        (ContentType.DATA_GRID_UDF, NAN_REPLACED_WITH_NA_UDF_DATA),
    ],
    ids=["NaN replaced with NA. RDP", "NaN replaced with NA. UDF"],
)
def test_nan_replaced_with_na(content_type, input_data, dfbuild_type):
    # when
    dataframe_build = get_dfbuilder(content_type, dfbuild_type)
    """
    #### INDEX ####
    
      Instrument       Date Currency
    0     GOOG.O 2020-01-20     1000
    1     GOOG.O 2020-12-31     <NA>

    #### DATE_AS_INDEX ####
     
    GOOG.O     Currency
    Date               
    2020-12-31     <NA>
    2020-01-20     1000
    """
    testing_df = dataframe_build(input_data)

    # then
    if dfbuild_type is DFBuildType.INDEX:
        assert isinstance(testing_df["Currency"][0], np.int64)
        assert testing_df["Currency"][1] is pd.NA

    elif dfbuild_type is DFBuildType.DATE_AS_INDEX:
        assert testing_df["Currency"][0] is pd.NA
        assert isinstance(testing_df["Currency"][1], np.int64)

    else:
        assert False, f"No assert for {dfbuild_type}"


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, EMPTY_STRING_LEAVE_AS_IT_IS_RDP_DATA),
        (ContentType.DATA_GRID_UDF, EMPTY_STRING_LEAVE_AS_IT_IS_UDF_DATA),
    ],
    ids=["Empty string leave as it is. RDP", "Empty string leave as it is. UDF"],
)
def test_empty_string_leave_as_it_is(content_type, input_data, dfbuild_type):
    # when
    dataframe_build = get_dfbuilder(content_type, dfbuild_type)
    """
    #### INDEX ####

      Instrument       Date Currency
    0     GOOG.O 2020-01-20         
    1     GOOG.O 2020-12-31         

    #### DATE_AS_INDEX ####

    GOOG.O     Currency
    Date               
    2020-12-31         
    2020-01-20         
       
    """
    testing_df = dataframe_build(input_data)

    # then
    assert testing_df["Currency"][0] == ""
    assert testing_df["Currency"][1] == ""


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, INSTRUMENT_AND_CURRENCY_ARE_EMPTY_STRINGS_RDP_DATA),
        (ContentType.DATA_GRID_UDF, INSTRUMENT_AND_CURRENCY_ARE_EMPTY_STRINGS_UDF_DATA),
    ],
    ids=[
        "Instrument and Currency are empty strings for dfbuild index. RDP",
        "Instrument and Currency are empty strings for dfbuild index. UDF",
    ],
)
def test_instrument_and_currency_are_empty_strings_for_dfbuild_index(
    content_type, input_data
):
    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.INDEX)
    """
    #### INDEX ####
    
      Instrument       Date Currency
    0            2020-01-20     <NA>   
    1     GOOG.O 2020-12-31     1000
    """
    testing_df = dataframe_build(input_data)

    # then
    assert testing_df["Currency"][0] is pd.NA
    assert testing_df["Instrument"][0] == ""


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, INSTRUMENT_AND_CURRENCY_ARE_EMPTY_STRINGS_RDP_DATA),
        (ContentType.DATA_GRID_UDF, INSTRUMENT_AND_CURRENCY_ARE_EMPTY_STRINGS_UDF_DATA),
    ],
    ids=[
        "Instrument and Currency are empty strings for dfbuild date as index. RDP",
        "Instrument and Currency are empty strings for dfbuild date as index. UDF",
    ],
)
def test_instrument_and_currency_are_empty_strings_for_dfbuild_date_as_index(
    content_type, input_data
):
    expected_str = (
        "Currency          GOOG.O\n"
        "Date                    \n"
        "2020-12-31  <NA>    1000\n"
        "2020-01-20          <NA>"
    )

    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####

    Currency          GOOG.O
    Date                    
    2020-12-31  <NA>    1000
    2020-01-20          <NA>
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, testing_str
    assert str(testing_df.dtypes["GOOG.O"]) == "Int64"
    assert str(testing_df.dtypes[""]) == "string"


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, TWO_UNIVERSES_ONE_FIELD_RDP_DATA),
        (ContentType.DATA_GRID_UDF, TWO_UNIVERSES_ONE_FIELD_UDF_DATA),
    ],
    ids=["Two universes and one field. RDP", "Two universes and one field. UDF"],
)
def test_two_universes_with_one_field(content_type, input_data):
    expected_str = (
        "BID         EUR=  LSEG.L\n"
        "Date                    \n"
        "2022-02-28  2000    <NA>\n"
        "2022-01-31  2000    <NA>\n"
        "2020-12-31  <NA>    1000\n"
        "2020-01-20  <NA>    1000"
    )
    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####

    BID         EUR=  LSEG.L
    Date                    
    2022-02-28  2000    <NA>
    2022-01-31  2000    <NA>
    2020-12-31  <NA>    1000
    2020-01-20  <NA>    1000
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, testing_str
    assert str(testing_df.dtypes["EUR="]) == "Int64"
    assert str(testing_df.dtypes["LSEG.L"]) == "Int64"


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, TWO_SAME_DATES_DOES_NOT_MERGE_IN_ONE_RDP_DATA),
        (ContentType.DATA_GRID_UDF, TWO_SAME_DATES_DOES_NOT_MERGE_IN_ONE_UDF_DATA),
    ],
    ids=[
        "Two same values does not merge in one. RDP",
        "Two same values does not merge in one. UDF",
    ],
)
def test_two_same_dates_does_not_merge_in_one(content_type, input_data):
    expected_str = (
        "IBM        Currency  Revenue - Mean\n"
        "Date                               \n"
        "2021-08-30      USD     75127177530\n"
        "2021-07-29      USD     75129376130\n"
        "2021-05-21      USD     74329699000\n"
        "2021-05-21      USD     74329699000\n"
        "2021-04-25      USD     74397055190\n"
        "2021-03-22      USD     74221312380\n"
        "2021-02-11      USD     74195199870\n"
        "2021-01-27      USD     74195199870\n"
        "2020-12-16      USD     73950729070\n"
        "2020-10-23      USD     73965242400\n"
        "2020-10-23      USD     73965242400"
    )
    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####

    IBM        Currency  Revenue - Mean
    Date                               
    2021-08-30      USD     75127177530
    2021-07-29      USD     75129376130
    2021-05-21      USD     74329699000
    2021-05-21      USD     74329699000
    2021-04-25      USD     74397055190
    2021-03-22      USD     74221312380
    2021-02-11      USD     74195199870
    2021-01-27      USD     74195199870
    2020-12-16      USD     73950729070
    2020-10-23      USD     73965242400
    2020-10-23      USD     73965242400
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, testing_str


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA),
        (ContentType.DATA_GRID_UDF, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA),
    ],
    ids=[
        "Merge values with same date in one row. RDP",
        "Merge values with same date in one row. UDF",
    ],
)
def test_merge_values_with_same_date_in_one_row(content_type, input_data):
    expected_str = (
        "                IBM                   VOD.L               \n"
        "           Currency Revenue - Mean Currency Revenue - Mean\n"
        "Date                                                      \n"
        "2021-08-30      USD    75127177530     <NA>           <NA>\n"
        "2021-08-25     <NA>           <NA>      EUR    45088444860\n"
        "2021-07-29      USD    75129376130      EUR    45109776750\n"
        "2021-06-29     <NA>           <NA>      EUR    44967283500\n"
        "2021-05-27     <NA>           <NA>      EUR    44918585000\n"
        "2021-05-21      USD    74329699000     <NA>           <NA>\n"
        "2021-05-21      USD    74329699000     <NA>           <NA>\n"
        "2021-04-28     <NA>           <NA>      EUR    43503348730\n"
        "2021-04-25      USD    74397055190     <NA>           <NA>\n"
        "2021-03-31     <NA>           <NA>      EUR    43445947190\n"
        "2021-03-22      USD    74221312380     <NA>           <NA>\n"
        "2021-02-24     <NA>           <NA>      EUR    43421860050\n"
        "2021-02-11      USD    74195199870     <NA>           <NA>\n"
        "2021-01-27      USD    74195199870     <NA>           <NA>\n"
        "2021-01-20     <NA>           <NA>      EUR    43333798760\n"
        "2020-12-16      USD    73950729070      EUR    43372965910\n"
        "2020-11-23     <NA>           <NA>      EUR    43442990380\n"
        "2020-10-23      USD    73965242400     <NA>           <NA>\n"
        "2020-10-23      USD    73965242400     <NA>           <NA>\n"
        "2020-10-21     <NA>           <NA>      EUR    43375027760"
    )
    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####

                    IBM                   VOD.L               
               Currency Revenue - Mean Currency Revenue - Mean
    Date                                                      
    2021-08-30      USD    75127177530     <NA>           <NA>
    2021-08-25     <NA>           <NA>      EUR    45088444860
    2021-07-29      USD    75129376130      EUR    45109776750
    2021-06-29     <NA>           <NA>      EUR    44967283500
    2021-05-27     <NA>           <NA>      EUR    44918585000
    2021-05-21      USD    74329699000     <NA>           <NA>
    2021-05-21      USD    74329699000     <NA>           <NA>
    2021-04-28     <NA>           <NA>      EUR    43503348730
    2021-04-25      USD    74397055190     <NA>           <NA>
    2021-03-31     <NA>           <NA>      EUR    43445947190
    2021-03-22      USD    74221312380     <NA>           <NA>
    2021-02-24     <NA>           <NA>      EUR    43421860050
    2021-02-11      USD    74195199870     <NA>           <NA>
    2021-01-27      USD    74195199870     <NA>           <NA>
    2021-01-20     <NA>           <NA>      EUR    43333798760
    2020-12-16      USD    73950729070      EUR    43372965910
    2020-11-23     <NA>           <NA>      EUR    43442990380
    2020-10-23      USD    73965242400     <NA>           <NA>
    2020-10-23      USD    73965242400     <NA>           <NA>
    2020-10-21     <NA>           <NA>      EUR    43375027760
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, testing_str


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, DELETE_ROW_IF_DATE_IS_NONE_RDP_DATA),
        (ContentType.DATA_GRID_UDF, DELETE_ROW_IF_DATE_IS_NONE_UDF_DATA),
    ],
    ids=[
        "Delete row if date is none. RDP",
        "Delete row if date is none. UDF",
    ],
)
def test_delete_row_if_date_is_none(content_type, input_data):
    expected_str_rdp = (
        "                  GOOG.O                 INVAL                      FB.O             \n"
        "                 Revenue  Gross Profit Revenue Gross Profit      Revenue Gross Profit\n"
        "Date                                                                                 \n"
        "2021-12-31  257637000000  146698000000    <NA>         <NA>         <NA>         <NA>\n"
        "2020-12-31          <NA>          <NA>    <NA>         <NA>  85965000000  69273000000"
    )
    expected_str_udf = (
        "                  GOOG.O                               INVAL                                    FB.O                           \n"
        "                 Revenue  Gross Profit INVALID_FIELD Revenue Gross Profit INVALID_FIELD      Revenue Gross Profit INVALID_FIELD\n"
        "Date                                                                                                                           \n"
        "2021-12-31  257637000000  146698000000                  <NA>         <NA>          <NA>         <NA>         <NA>          <NA>\n"
        "2020-12-31          <NA>          <NA>          <NA>    <NA>         <NA>          <NA>  85965000000  69273000000              "
    )

    expected_str = (
        expected_str_udf
        if content_type is ContentType.DATA_GRID_UDF
        else expected_str_rdp
    )
    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####
    # UDF #
                  GOOG.O                               INVAL                                    FB.O                           
                 Revenue  Gross Profit INVALID_FIELD Revenue Gross Profit INVALID_FIELD      Revenue Gross Profit INVALID_FIELD
Date                                                                                                                           
2021-12-31  257637000000  146698000000                  <NA>         <NA>          <NA>         <NA>         <NA>          <NA>
2020-12-31          <NA>          <NA>          <NA>    <NA>         <NA>          <NA>  85965000000  69273000000              

    # RDP #
                  GOOG.O                 INVAL                      FB.O             
                 Revenue  Gross Profit Revenue Gross Profit      Revenue Gross Profit
Date                                                                                 
2021-12-31  257637000000  146698000000    <NA>         <NA>         <NA>         <NA>
2020-12-31          <NA>          <NA>    <NA>         <NA>  85965000000  69273000000
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, f"\n{testing_df.to_string()}"


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_1),
        (ContentType.DATA_GRID_UDF, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_1),
    ],
    ids=[
        "Merge values with same date in one row. Combination 1. RDP",
        "Merge values with same date in one row. Combination 1. UDF",
    ],
)
def test_merge_values_with_same_date_in_one_row_combination_1(content_type, input_data):
    expected_str = (
        "                IBM                   VOD.L                   NKE.N               \n"
        "           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean\n"
        "Date                                                                              \n"
        "2020-10-23      USD    73965242400      EUR    43375027760     <NA>           <NA>\n"
        "2020-05-07     <NA>           <NA>     <NA>           <NA>      GBP    43375027760"
    )

    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####
                IBM                   VOD.L                   NKE.N               
           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean
Date                                                                              
2020-10-23      USD    73965242400      EUR    43375027760     <NA>           <NA>
2020-05-07     <NA>           <NA>     <NA>           <NA>      GBP    43375027760
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, f"\n{testing_df.to_string()}"


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_2),
        (ContentType.DATA_GRID_UDF, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_2),
    ],
    ids=[
        "Merge values with same date in one row. Combination 2. RDP",
        "Merge values with same date in one row. Combination 2. UDF",
    ],
)
def test_merge_values_with_same_date_in_one_row_combination_2(content_type, input_data):
    expected_str = (
        "                IBM                   VOD.L                   NKE.N               \n"
        "           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean\n"
        "Date                                                                              \n"
        "2020-10-23      USD    73965242400      EUR    43375027760      GBP    43375027760"
    )

    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####
                IBM                   VOD.L                   NKE.N               
           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean
Date                                                                              
2020-10-23      USD    73965242400      EUR    43375027760      GBP    43375027760
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, f"\n{testing_df.to_string()}"


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_3),
        (ContentType.DATA_GRID_UDF, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_3),
    ],
    ids=[
        "Merge values with same date in one row. Combination 3. RDP",
        "Merge values with same date in one row. Combination 3. UDF",
    ],
)
def test_merge_values_with_same_date_in_one_row_combination_3(content_type, input_data):
    expected_str = (
        "                IBM                   VOD.L                   NKE.N               \n"
        "           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean\n"
        "Date                                                                              \n"
        "2020-10-23     <NA>           <NA>      EUR    43375027760     <NA>           <NA>\n"
        "2020-09-18      USD    73965242400     <NA>           <NA>     <NA>           <NA>\n"
        "2020-05-07     <NA>           <NA>     <NA>           <NA>      GBP    43375027760"
    )

    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####
                IBM                   VOD.L                   NKE.N               
           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean
Date                                                                              
2020-10-23     <NA>           <NA>      EUR    43375027760     <NA>           <NA>
2020-09-18      USD    73965242400     <NA>           <NA>     <NA>           <NA>
2020-05-07     <NA>           <NA>     <NA>           <NA>      GBP    43375027760
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, f"\n{testing_df.to_string()}"


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_4),
        (ContentType.DATA_GRID_UDF, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_4),
    ],
    ids=[
        "Merge values with same date in one row. Combination 4. RDP",
        "Merge values with same date in one row. Combination 4. UDF",
    ],
)
def test_merge_values_with_same_date_in_one_row_combination_4(content_type, input_data):
    expected_str = (
        "                IBM                   VOD.L                   NKE.N               \n"
        "           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean\n"
        "Date                                                                              \n"
        "2020-10-23     <NA>           <NA>      EUR    43375027760      GBP    43375027760\n"
        "2020-05-07      USD    73965242400     <NA>           <NA>     <NA>           <NA>"
    )

    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####
                IBM                   VOD.L                   NKE.N               
           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean
Date                                                                              
2020-10-23     <NA>           <NA>      EUR    43375027760      GBP    43375027760
2020-05-07      USD    73965242400     <NA>           <NA>     <NA>           <NA>
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, f"\n{testing_df.to_string()}"


@pytest.mark.parametrize(
    "content_type, input_data",
    [
        (ContentType.DATA_GRID_RDP, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_RDP_DATA_5),
        (ContentType.DATA_GRID_UDF, MERGE_VALUES_WITH_SAME_DATE_IN_ONE_ROW_UDF_DATA_5),
    ],
    ids=[
        "Merge values with same date in one row. Combination 5. RDP",
        "Merge values with same date in one row. Combination 5. UDF",
    ],
)
def test_merge_values_with_same_date_in_one_row_combination_5(content_type, input_data):
    expected_str = (
        "                IBM                   VOD.L                   NKE.N               \n"
        "           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean\n"
        "Date                                                                              \n"
        "2020-10-23      USD    73965242400     <NA>           <NA>      GBP    43375027760\n"
        "2020-05-07     <NA>           <NA>      EUR    43375027760     <NA>           <NA>"
    )

    # when
    dataframe_build = get_dfbuilder(content_type, DFBuildType.DATE_AS_INDEX)
    """
    #### DATE_AS_INDEX ####
                IBM                   VOD.L                   NKE.N               
           Currency Revenue - Mean Currency Revenue - Mean Currency Revenue - Mean
Date                                                                              
2020-10-23      USD    73965242400     <NA>           <NA>      GBP    43375027760
2020-05-07     <NA>           <NA>      EUR    43375027760     <NA>           <NA>
    """
    testing_df = dataframe_build(input_data)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_str, f"\n{testing_df.to_string()}"
