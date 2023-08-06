from refinitiv.data.content.ownership import org_info


def test_org_info():
    try:
        definition = org_info.Definition(universe="")
    except Exception as e:
        assert False, str(e)
