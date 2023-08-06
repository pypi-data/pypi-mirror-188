import abc
from typing import Dict, Optional

import pandas as pd
from pandas import DataFrame

from ._context import Context
from ..._tools import ohlc
from ..._tools._dataframe import (
    convert_dtypes,
)


class CustInstContext(Context, abc.ABC):
    @property
    def can_get_data(self) -> bool:
        return bool(self.universe.cust_inst)

    @property
    def can_build_df(self) -> bool:
        return bool(self._cust_inst_data and not (self._adc_data or self._hp_data))

    @property
    def can_join_hp_multiindex_df(self) -> bool:
        return bool(
            not self._adc_data
            and (self._hp_data and self._cust_inst_data and len(self.universe.hp) > 1)
        )

    @property
    def raw(self) -> Optional[Dict]:
        return self._cust_inst_data and self._cust_inst_data.raw

    @property
    def df(self) -> Optional[DataFrame]:
        return self._cust_inst_data and self._cust_inst_data.df

    def build_df(self, use_field_names_in_headers: bool, *args) -> DataFrame:
        """
        Builds custom instrument dataframe.

        Parameters
        ----------
        use_field_names_in_headers : bool
            Flag to use field names in headers
        args
            Variable length additional arguments list.

        Returns
        -------
        pd.DataFrame
            Custom instrument dataframe.

        """
        fields = self.fields
        df = self.df

        if fields:
            data = self.prepare_data(self.raw, fields)
            headers = self.prepare_headers(fields.raw)
            use_multiindex = len(fields.raw) > 1 and len(self.universe.cust_inst) > 1
            df = self._build_common_df(
                data, headers, use_field_names_in_headers, use_multiindex=use_multiindex
            )

        df = convert_dtypes(df)
        df.ohlc = ohlc.__get__(df, None)
        return df

    def join_hp_multiindex_df(self, hp_df: DataFrame, use_field_names_in_headers: bool):
        """
        Joins historical pricing multiindex dataframe with custom instruments dataframe.

        Parameters
        ----------
        hp_df : pd.DataFrame
            Historical pricing multiindex dataframe.
        use_field_names_in_headers : bool
            Flag to use fields names in headers.

        Returns
        -------
        pd.DataFrame
            Historical pricing multiindex dataframe, joined with custom instruments
            dataframe.
        """
        fields = self._get_fields_from_raw()
        data = self.prepare_data(self.raw, fields)
        headers = self.prepare_headers(fields)
        cust_df = self._build_common_df(
            data, headers, use_field_names_in_headers, use_multiindex=True
        )
        joined_df = hp_df.join(cust_df, how="outer")
        df = convert_dtypes(joined_df)
        df.ohlc = ohlc.__get__(df, None)
        return df

    def _build_common_df(
        self,
        data: list,
        headers: list,
        use_field_names_in_headers: bool,
        use_multiindex: bool,
    ):
        """
        Builds common dataframe for custom instruments data.

        Parameters
        ----------
        data : list
            Data to create dataframe.
        headers : list
            Headers to create dataframe.
        use_field_names_in_headers : bool
            Flag to use fields names in headers.
        use_multiindex : bool
            Flag to use multiindex for dataframe creation or not.

        Returns
        -------
        DataFrame
        """
        df = self.dfbuilder.build_date_as_index(
            {"data": data, "headers": headers},
            use_field_names_in_headers,
            use_multiindex=use_multiindex,
        )
        return df

    def _get_fields_from_raw(self):
        fields = []
        if isinstance(self.raw, list):
            headers = self.raw[0]["headers"]

        else:
            headers = self.raw["headers"]

        for header in headers:
            name = header.get("name")
            if name and name.lower() not in {"date", "instrument"}:
                fields.append(name)

        return fields

    def _get_fields_from_headers(self, headers, use_field_names_in_headers):
        name = "name" if use_field_names_in_headers else "title"
        return [
            header[name]
            for header in self.dfbuilder.get_headers({"headers": headers})
            if header[name].lower() not in {"date", "instrument"}
        ]

    def prepare_to_build(
        self, use_field_names_in_headers, df: DataFrame, headers, *args
    ):
        """
        Creates dataframe with ADC, historical pricing and custom instruments data.

        Join or merge previously created ADC and historical pricing dataframe with
        custom instruments dataframe.

        Parameters
        ----------
        use_field_names_in_headers : bool
            Use
        df : pd.DataFrame
            Previously created ADC and historical pricing dataframe.
        headers : List
            Common headers for building dataframe
        args
            Variable length additional arguments list.

        Returns
        -------
        pd.Dataframe that includes ADC, hp and custom instruments data.

        """
        if not self.fields:
            fields = self._get_fields_from_raw()

        else:
            fields = self._get_fields_from_headers(headers, use_field_names_in_headers)

        data = self.prepare_data(self.raw, fields)
        headers = self.prepare_headers(fields)
        cust_df = self._build_common_df(
            data, headers, use_field_names_in_headers, use_multiindex=True
        )

        if (not self._adc_data and self._hp_data) or (
            self._adc_data and not self._hp_data
        ):
            df = df.join(cust_df, how="outer")
        else:
            df = pd.merge(df, cust_df, on=["Date"])

        self._cust_inst_data._df = df
