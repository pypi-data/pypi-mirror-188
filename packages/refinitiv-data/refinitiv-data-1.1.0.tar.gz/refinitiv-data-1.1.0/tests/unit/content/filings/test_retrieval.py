import pytest

from refinitiv.data.content.filings import retrieval


def test_retrieval_definition(create_filings_definition):
    retrieval.Definition(**create_filings_definition)


def test_retrieval_definition_error(create_filings_definition_with_error):
    try:
        retrieval.Definition(**create_filings_definition_with_error)
    except ValueError:
        assert True
    except Exception as e:
        assert False, str(e)


@pytest.mark.parametrize(
    "filings_definition, expected_repr",
    [
        (
            retrieval.Definition(filename="filename_1"),
            "<refinitiv.data.content.filings.retrieval.Definition object at {0} {{filename='filename_1', dcn='None', doc_id='None', filing_id='None'}}>",
        ),
        (
            retrieval.Definition(dcn="dcn_1"),
            "<refinitiv.data.content.filings.retrieval.Definition object at {0} {{filename='None', dcn='dcn_1', doc_id='None', filing_id='None'}}>",
        ),
        (
            retrieval.Definition(doc_id="doc_id_1"),
            "<refinitiv.data.content.filings.retrieval.Definition object at {0} {{filename='None', dcn='None', doc_id='doc_id_1', filing_id='None'}}>",
        ),
        (
            retrieval.Definition(filing_id="filing_id_1"),
            "<refinitiv.data.content.filings.retrieval.Definition object at {0} {{filename='None', dcn='None', doc_id='None', filing_id='filing_id_1'}}>",
        ),
    ],
)
def test_retrieval_definition_repr(filings_definition, expected_repr):
    # given
    obj_id = hex(id(filings_definition))

    # when
    s = repr(filings_definition)

    # then
    assert s == expected_repr.format(obj_id)
