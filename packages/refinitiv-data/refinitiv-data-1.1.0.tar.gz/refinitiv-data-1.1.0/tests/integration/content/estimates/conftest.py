import refinitiv.data.content.estimates as rde


def invalid_view_actuals_interim_estimates(universe):
    definition = rde.view_actuals.interim.Definition(
        universe=universe, package=rde.Package.PROFESSIONAL
    )
    return definition


def view_actuals_annual_estimates(universe, package=None):
    definition = rde.view_actuals.annual.Definition(
        universe=universe, package=package, use_field_names_in_headers=True
    ).get_data()
    return definition


def view_actuals_kpi_annual_estimates(universe, use_field_names_in_headers=False):
    definition = rde.view_actuals_kpi.annual.Definition(
        universe=universe, use_field_names_in_headers=use_field_names_in_headers
    ).get_data()
    return definition


def view_summary_annual_estimates(universe, package=None):
    definition = rde.view_summary.annual.Definition(
        universe=universe, package=package, use_field_names_in_headers=False
    ).get_data()
    return definition


def view_summary_historical_non_periodic_estimates(universe, package, extended_params):
    definition = rde.view_summary.historical_snapshots_non_periodic_measures.Definition(
        universe=universe, package=package, extended_params=extended_params
    ).get_data()
    return definition


def view_summary_historical_annual_estimates(universe, package, extended_params):
    definition = (
        rde.view_summary.historical_snapshots_periodic_measures_annual.Definition(
            universe=universe, package=package, extended_params=extended_params
        ).get_data()
    )
    return definition


def view_summary_recommendations_estimates(universe, package):
    definition = rde.view_summary.recommendations.Definition(
        universe=universe, package=package
    ).get_data()
    return definition


def view_summary_kpi_annual_estimates(universe):
    definition = rde.view_summary_kpi.annual.Definition(universe=universe)
    return definition
