from refinitiv.data.content.estimates.view_summary import (
    annual,
    historical_snapshots_non_periodic_measures,
    historical_snapshots_periodic_measures_annual,
    historical_snapshots_periodic_measures_interim,
    historical_snapshots_recommendations,
    interim,
    non_periodic_measures,
    recommendations,
)


def test_annual(create_estimates_definition):
    annual.Definition(**create_estimates_definition)


def test_historical_snapshots_non_periodic_measures(create_estimates_definition):
    historical_snapshots_non_periodic_measures.Definition(**create_estimates_definition)


def test_historical_snapshots_periodic_measures_annual(create_estimates_definition):
    historical_snapshots_periodic_measures_annual.Definition(
        **create_estimates_definition
    )


def test_historical_snapshots_periodic_measures_interim(create_estimates_definition):
    historical_snapshots_periodic_measures_interim.Definition(
        **create_estimates_definition
    )


def test_historical_snapshots_recommendations(create_estimates_definition):
    historical_snapshots_recommendations.Definition(**create_estimates_definition)


def test_interim(create_estimates_definition):
    interim.Definition(**create_estimates_definition)


def test_non_periodic_measures(create_estimates_definition):
    non_periodic_measures.Definition(**create_estimates_definition)


def test_recommendations(create_estimates_definition):
    recommendations.Definition(**create_estimates_definition)


def test_annual_error(create_estimates_definition_with_error):
    try:
        annual.Definition(**create_estimates_definition_with_error)
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)


def test_historical_snapshots_non_periodic_measures_error(
    create_estimates_definition_with_error,
):
    try:
        historical_snapshots_non_periodic_measures.Definition(
            **create_estimates_definition_with_error
        )
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)


def test_historical_snapshots_periodic_measures_annual_error(
    create_estimates_definition_with_error,
):
    try:
        historical_snapshots_periodic_measures_annual.Definition(
            **create_estimates_definition_with_error
        )
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)


def test_historical_snapshots_periodic_measures_interim_error(
    create_estimates_definition_with_error,
):
    try:
        historical_snapshots_periodic_measures_interim.Definition(
            **create_estimates_definition_with_error
        )
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)


def test_historical_snapshots_recommendations_error(
    create_estimates_definition_with_error,
):
    try:
        historical_snapshots_recommendations.Definition(
            **create_estimates_definition_with_error
        )
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)


def test_interim_error(create_estimates_definition_with_error):
    try:
        interim.Definition(**create_estimates_definition_with_error)
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)


def test_non_periodic_measures_error(create_estimates_definition_with_error):
    try:
        non_periodic_measures.Definition(**create_estimates_definition_with_error)
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)


def test_recommendations_error(create_estimates_definition_with_error):
    try:
        recommendations.Definition(**create_estimates_definition_with_error)
    except (TypeError, ValueError):
        assert True
    except Exception as e:
        assert False, str(e)
