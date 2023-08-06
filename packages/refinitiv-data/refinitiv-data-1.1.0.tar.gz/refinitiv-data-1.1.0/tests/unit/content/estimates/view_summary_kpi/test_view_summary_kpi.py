from refinitiv.data.content.estimates.view_summary_kpi import (
    annual,
    historical_snapshots_kpi,
    interim,
)


def test_annual(create_estimates_kpi_definition):
    annual.Definition(**create_estimates_kpi_definition)


def test_historical_snapshots_kpi(create_estimates_kpi_definition):
    historical_snapshots_kpi.Definition(**create_estimates_kpi_definition)


def test_interim(create_estimates_kpi_definition):
    interim.Definition(**create_estimates_kpi_definition)


def test_annual_error(create_estimates_kpi_definition_with_error):
    try:
        annual.Definition(**create_estimates_kpi_definition_with_error)
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)


def test_historical_snapshots_kpi_error(create_estimates_kpi_definition_with_error):
    try:
        historical_snapshots_kpi.Definition(
            **create_estimates_kpi_definition_with_error
        )
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)


def test_interim_error(create_estimates_kpi_definition_with_error):
    try:
        interim.Definition(**create_estimates_kpi_definition_with_error)
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)
