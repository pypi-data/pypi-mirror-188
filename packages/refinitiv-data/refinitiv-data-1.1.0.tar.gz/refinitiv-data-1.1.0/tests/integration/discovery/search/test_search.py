import allure
import pytest

from refinitiv.data.discovery import search, search_templates, Views
from refinitiv.data.errors import RDError
from tests.integration.helpers import (
    check_response_value,
    check_if_dataframe_is_not_none,
)


@allure.suite("FinCoder layer")
@allure.feature("FinCoder layer")
@allure.severity(allure.severity_level.NORMAL)
class TestSearch:
    @allure.title("Get search with query using a string")
    @pytest.mark.caseid("C43895895")
    @pytest.mark.parametrize(
        "query, expected_business_entity",
        [("Microsoft", ["QUOTExEQUITY", "ORGANISATION"])],
    )
    def test_search_with_query_using_string_and_get_data(
        self, open_session, query, expected_business_entity
    ):
        response = search(query)

        check_response_value(response, "BusinessEntity", expected_business_entity)

    @allure.title("Get structured search with boost")
    @pytest.mark.caseid("C43895897")
    @pytest.mark.parametrize(
        "view,filter,boost,select,expected_business_entity",
        [
            (
                Views.PHYSICAL_ASSETS,
                "RCSAssetTypeLeaf eq 'oil refinery' and RCSRegionLeaf eq 'Venezuela'",
                "PlantStatus ne 'Normal Operation'",
                "DocumentTitle,BusinessEntity",
                ["PHYSICALASSETxPLANT"],
            )
        ],
    )
    def test_search_with_boost_and_get_data(
        self, open_session, view, filter, boost, select, expected_business_entity
    ):
        response = search(view=view, filter=filter, boost=boost, select=select)

        check_response_value(response, "BusinessEntity", expected_business_entity)

    @allure.title("Get search with invalid params")
    @pytest.mark.caseid("C43895898")
    @pytest.mark.parametrize(
        "view, filter",
        [(Views.PHYSICAL_ASSETS, "Invalid Filters")],
    )
    def test_search_with_invalid_params(self, open_session, view, filter):
        with pytest.raises(RDError) as error:
            search(view=view, filter=filter)

        assert (
            str(error.value)
            == "Error code 400 | Invalid filter: PROPERTY node <Filters> cannot follow PROPERTY node <Invalid>"
        )

    @allure.title("Get search with search template")
    @pytest.mark.caseid("C48966252")
    def test_search_with_search_template(self, load_config, open_session):
        response = search_templates["Equity"].search(
            exchange_name="Frankfurt Stock Exchange",
            navigators="RCSAssetCategoryLeaf(buckets:3, sub:ExchangeName(buckets:2))",
        )

        check_response_value(response, "ExchangeName", ["Frankfurt Stock Exchange"])

    @allure.title("Get search with embedded search template")
    @pytest.mark.caseid("C48966253")
    def test_search_with_embedded_search_template(self, open_session):
        response = search_templates.UnderlyingRICToOption.search(ric="VOD.L")

        check_if_dataframe_is_not_none(response)
        assert "VOD010bB3.EX" in response["RIC"].tolist()

    @allure.title("Create request with invalid search template")
    @pytest.mark.caseid("C48966256")
    def test_invalid_search_template(self, open_session):
        response = search_templates.UnderlyingRICToOption.search(ric="Invalid RIC")

        assert response.empty, f"Response is not empty"
