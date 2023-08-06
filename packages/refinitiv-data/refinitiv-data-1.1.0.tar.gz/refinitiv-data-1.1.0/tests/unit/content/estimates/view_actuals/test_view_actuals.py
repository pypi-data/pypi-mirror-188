from refinitiv.data.content.estimates.view_actuals import annual, interim


def test_annual(create_estimates_definition):
    annual.Definition(**create_estimates_definition)


def test_interim(create_estimates_definition):
    interim.Definition(**create_estimates_definition)


def test_annual_error(create_estimates_definition_with_error):
    try:
        annual.Definition(**create_estimates_definition_with_error)
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
