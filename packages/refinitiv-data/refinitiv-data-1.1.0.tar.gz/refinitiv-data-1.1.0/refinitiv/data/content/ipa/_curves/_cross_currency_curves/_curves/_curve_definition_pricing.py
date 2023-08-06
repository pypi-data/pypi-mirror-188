from typing import Optional, TYPE_CHECKING

from .._enums import MainConstituentAssetClass, RiskType
from ...._object_definition import ObjectDefinition
from ._enums import ConstituentOverrideMode


if TYPE_CHECKING:
    from ......_types import OptStr, OptBool


class CrossCurrencyCurveDefinitionPricing(ObjectDefinition):
    """
    Generates the Cross Currency curves for the definitions provided

    Parameters
    ----------
    constituent_override_mode : ConstituentOverrideMode, optional
        A method to use the default constituents. the possible values are:   *
        replacedefinition: replace the default constituents by the user constituents
        from the input request,   * mergewithdefinition: merge the default constituents
        and the user constituents from the input request, the default value is
        'replacedefinition'.  if the ignoreexistingdefinition is true, the
        constituentoverridemode is set to replacedefinition.
    main_constituent_asset_class : MainConstituentAssetClass, optional
        The asset class used to generate the zero coupon curve. the possible values are:
        * fxforward   * swap
    risk_type : RiskType, optional
        The risk type to which the generated cross currency curve is sensitive. the
        possible value is:   * 'crosscurrency'
    base_currency : str, optional
        The base currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'eur').
    base_index_name : str, optional
        The name of the floating rate index (e.g., 'estr') applied to the base currency.
    id : str, optional
        The identifier of the cross currency definitions.
    ignore_existing_definition : bool, optional
        An indicator whether default definitions are used to get curve parameters and
        constituents. the possible values are:   * true: default definitions are not
        used (definitions and constituents must be set in the request),   * false:
        default definitions are used.
    is_non_deliverable : bool, optional
        An indicator whether the instrument is non-deliverable:   * true: the instrument
        is non-deliverable,   * false: the instrument is not non-deliverable. the
        property can be used to retrieve cross currency definition for the adjusted
        interest rate curve.
    name : str, optional
        The fxcross currency pair applied to the reference or pivot currency. it is
        expressed in iso 4217 alphabetical format (e.g., 'eur usd fxcross').
    quoted_currency : str, optional
        The quoted currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'usd').
    quoted_index_name : str, optional
        The name of the floating rate index (e.g., 'sofr') applied to the quoted
        currency.
    source : str, optional
        A user-defined string that is provided by the creator of a curve. curves created
        by refinitiv have the 'refinitiv' source.
    """

    def __init__(
        self,
        constituent_override_mode: Optional[ConstituentOverrideMode] = None,
        main_constituent_asset_class: Optional[MainConstituentAssetClass] = None,
        risk_type: Optional[RiskType] = None,
        base_currency: "OptStr" = None,
        base_index_name: "OptStr" = None,
        id: "OptStr" = None,
        ignore_existing_definition: "OptBool" = None,
        is_non_deliverable: "OptBool" = None,
        name: "OptStr" = None,
        quoted_currency: "OptStr" = None,
        quoted_index_name: "OptStr" = None,
        source: "OptStr" = None,
    ) -> None:
        super().__init__()
        self.constituent_override_mode = constituent_override_mode
        self.main_constituent_asset_class = main_constituent_asset_class
        self.risk_type = risk_type
        self.base_currency = base_currency
        self.base_index_name = base_index_name
        self.id = id
        self.ignore_existing_definition = ignore_existing_definition
        self.is_non_deliverable = is_non_deliverable
        self.name = name
        self.quoted_currency = quoted_currency
        self.quoted_index_name = quoted_index_name
        self.source = source

    @property
    def constituent_override_mode(self):
        """
        A method to use the default constituents. the possible values are:   *
        replacedefinition: replace the default constituents by the user constituents
        from the input request,   * mergewithdefinition: merge the default constituents
        and the user constituents from the input request, the default value is
        'replacedefinition'.  if the ignoreexistingdefinition is true, the
        constituentoverridemode is set to replacedefinition.
        :return: enum ConstituentOverrideMode
        """
        return self._get_enum_parameter(
            ConstituentOverrideMode, "constituentOverrideMode"
        )

    @constituent_override_mode.setter
    def constituent_override_mode(self, value):
        self._set_enum_parameter(
            ConstituentOverrideMode, "constituentOverrideMode", value
        )

    @property
    def main_constituent_asset_class(self):
        """
        The asset class used to generate the zero coupon curve. the possible values are:
        * fxforward   * swap
        :return: enum MainConstituentAssetClass
        """
        return self._get_enum_parameter(
            MainConstituentAssetClass, "mainConstituentAssetClass"
        )

    @main_constituent_asset_class.setter
    def main_constituent_asset_class(self, value):
        self._set_enum_parameter(
            MainConstituentAssetClass, "mainConstituentAssetClass", value
        )

    @property
    def risk_type(self):
        """
        The risk type to which the generated cross currency curve is sensitive. the
        possible value is:   * 'crosscurrency'
        :return: enum RiskType
        """
        return self._get_enum_parameter(RiskType, "riskType")

    @risk_type.setter
    def risk_type(self, value):
        self._set_enum_parameter(RiskType, "riskType", value)

    @property
    def base_currency(self):
        """
        The base currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'eur').
        :return: str
        """
        return self._get_parameter("baseCurrency")

    @base_currency.setter
    def base_currency(self, value):
        self._set_parameter("baseCurrency", value)

    @property
    def base_index_name(self):
        """
        The name of the floating rate index (e.g., 'estr') applied to the base currency.
        :return: str
        """
        return self._get_parameter("baseIndexName")

    @base_index_name.setter
    def base_index_name(self, value):
        self._set_parameter("baseIndexName", value)

    @property
    def id(self):
        """
        The identifier of the cross currency definitions.
        :return: str
        """
        return self._get_parameter("id")

    @id.setter
    def id(self, value):
        self._set_parameter("id", value)

    @property
    def ignore_existing_definition(self):
        """
        An indicator whether default definitions are used to get curve parameters and
        constituents. the possible values are:   * true: default definitions are not
        used (definitions and constituents must be set in the request),   * false:
        default definitions are used.
        :return: bool
        """
        return self._get_parameter("ignoreExistingDefinition")

    @ignore_existing_definition.setter
    def ignore_existing_definition(self, value):
        self._set_parameter("ignoreExistingDefinition", value)

    @property
    def is_non_deliverable(self):
        """
        An indicator whether the instrument is non-deliverable:   * true: the instrument
        is non-deliverable,   * false: the instrument is not non-deliverable. the
        property can be used to retrieve cross currency definition for the adjusted
        interest rate curve.
        :return: bool
        """
        return self._get_parameter("isNonDeliverable")

    @is_non_deliverable.setter
    def is_non_deliverable(self, value):
        self._set_parameter("isNonDeliverable", value)

    @property
    def name(self):
        """
        The fxcross currency pair applied to the reference or pivot currency. it is
        expressed in iso 4217 alphabetical format (e.g., 'eur usd fxcross').
        :return: str
        """
        return self._get_parameter("name")

    @name.setter
    def name(self, value):
        self._set_parameter("name", value)

    @property
    def quoted_currency(self):
        """
        The quoted currency in the fxcross currency pair. it is expressed in iso 4217
        alphabetical format (e.g., 'usd').
        :return: str
        """
        return self._get_parameter("quotedCurrency")

    @quoted_currency.setter
    def quoted_currency(self, value):
        self._set_parameter("quotedCurrency", value)

    @property
    def quoted_index_name(self):
        """
        The name of the floating rate index (e.g., 'sofr') applied to the quoted
        currency.
        :return: str
        """
        return self._get_parameter("quotedIndexName")

    @quoted_index_name.setter
    def quoted_index_name(self, value):
        self._set_parameter("quotedIndexName", value)

    @property
    def source(self):
        """
        A user-defined string that is provided by the creator of a curve. curves created
        by refinitiv have the 'refinitiv' source.
        :return: str
        """
        return self._get_parameter("source")

    @source.setter
    def source(self, value):
        self._set_parameter("source", value)
