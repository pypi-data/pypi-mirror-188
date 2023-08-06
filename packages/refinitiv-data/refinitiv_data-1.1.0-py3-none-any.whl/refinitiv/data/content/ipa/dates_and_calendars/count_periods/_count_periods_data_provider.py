from typing import TYPE_CHECKING, List

from .._content_data_validator import ContentDataValidator
from .._request_factory import DatesAndCalendarsResponseFactory
from ...._content_data import Data
from ...._content_data_provider import ContentDataProvider
from ...._df_builder import default_build_df
from .....content.ipa._content_provider import DatesAndCalendarsRequestFactory
from .....delivery._data._data_provider import ValidatorContainer

if TYPE_CHECKING:
    from .....delivery._data._data_provider import ParsedData


class Period:
    def __init__(self, count: float, tenor: str, tag: str = ""):
        self._count = count
        self._tenor = tenor
        self._tag = tag

    @property
    def count(self):
        return self._count

    @property
    def tenor(self):
        return self._tenor

    @property
    def tag(self):
        return self._tag


class CountedPeriods(Data):
    _counted_periods = None

    @property
    def counted_periods(self):
        if self._counted_periods is None:
            self._counted_periods = [
                Period(item["count"], item["tenor"], tag=item.get("tag"))
                for item in self._raw
            ]

        return self._counted_periods

    def __getitem__(self, item: int):
        return self.counted_periods[item]


class CountedPeriod(Data):
    def __init__(self, raw: dict, count: float, tenor: str, tag: str = "", **kwargs):
        super().__init__(raw, **kwargs)
        self._period = Period(count, tenor, tag)

    @property
    def counted_period(self):
        return self._period


class CountPeriodsResponseFactory(DatesAndCalendarsResponseFactory):
    def create_data_success(self, parsed_data: "ParsedData", **kwargs):
        raw: List[dict] = self.get_raw(parsed_data)
        for item in raw:
            if item.get("error"):
                return self.create_fail(item, **kwargs)

        if len(raw) > 1:
            data = CountedPeriods(raw, default_build_df)

        else:
            raw_item = raw[0]
            data = CountedPeriod(
                raw,
                raw_item["count"],
                raw_item["tenor"],
                raw_item.get("tag"),
                dfbuilder=default_build_df,
                **kwargs,
            )

        return data


count_periods_data_provider = ContentDataProvider(
    request=DatesAndCalendarsRequestFactory(),
    response=CountPeriodsResponseFactory(),
    validator=ValidatorContainer(content_validator=ContentDataValidator()),
)
