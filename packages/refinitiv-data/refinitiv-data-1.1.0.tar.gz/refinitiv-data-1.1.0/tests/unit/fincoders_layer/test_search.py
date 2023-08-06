import refinitiv.data as rd
from refinitiv.data._core.session import set_default
from tests.unit.conftest import StubSession
from tests.unit.fincoders_layer.data_for_tests import (
    SEARCH_QUERY_CFO_RESPONSE,
    SEARCH_QUERY_IBM_RESPONSE,
)


def test_search_query_cfo():
    expected_srt = (
        "  BusinessEntity                                                                              DocumentTitle       PermID           PI\n"
        "0         PERSON           Amy E. Hood - Microsoft Corp - Chief Financial Officer, Executive Vice President  34415553383  34415553383\n"
        "1         PERSON                  Luca Maestri - Apple Inc - Chief Financial Officer, Senior Vice President  34414554748  34414554748\n"
        "2         PERSON        Brian T. Olsavsky - Amazon.com Inc - Chief Financial Officer, Senior Vice President  34417610894  34417610894\n"
        "3         PERSON              Ruth M. Porat - Alphabet Inc - Chief Financial Officer, Senior Vice President  34413960665  34413960665\n"
        "4         PERSON                             David M. Wehner - Meta Platforms Inc - Chief Financial Officer  34414804241  34414804241\n"
        "5         PERSON  Marc D. Hamburg - Berkshire Hathaway Inc - Chief Financial Officer, Senior Vice President  34413152672  34413152672\n"
        "6         PERSON                                       Andrew K. Klatt - Berkshire Hathaway Inc - CFO & COO  34414966250  34414966250\n"
        "7         PERSON                              Xu Hong - Alibaba Group Holding Ltd - Chief Financial Officer  34425652371  34425652371\n"
        "8         PERSON            John Lo - Tencent Holdings Ltd - Chief Financial Officer, Senior Vice President  34414907131  34414907131\n"
        "9         PERSON          Vasant M. Prabhu - Visa Inc - Vice Chairman of the Board, Chief Financial Officer  34413340523  34413340523"
    )
    # given
    session = StubSession(is_open=True, response=SEARCH_QUERY_CFO_RESPONSE)
    set_default(session)

    # when
    testing_df = rd.discovery.search(query="cfo", view=rd.discovery.Views.PEOPLE)

    # teardown
    set_default(None)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_srt


def test_search_query_ibm():
    expected_srt = (
        "  BusinessEntity                                                                                               DocumentTitle       PermID         PI       RIC\n"
        "0   ORGANISATION                                                        International Business Machines Corp, Public Company         <NA>      37036      <NA>\n"
        "1   ORGANISATION                                                                               Banco IBM SA, Private Company         <NA>      76208      <NA>\n"
        "2   QUOTExEQUITY                                     International Business Machines Corp, Ordinary Share, NYSE Consolidated  55839165994    1097326       IBM\n"
        "3   ORGANISATION                           Tiers Corporate Bond Backed Certificates Trust Series Ibm 1997 4, Private Company         <NA>   18062670      <NA>\n"
        "4   QUOTExEQUITY              Eurex International Business Machines Equity Future Chain Contract , Equity Future, USD, Eurex  21481052421   48924732   0#IBMF:\n"
        "5   QUOTExEQUITY              Euronext Amsterdam IBM Dividend Future Chain Contracts, Equity Future, USD, Euronext Amsterdam  21612423771  259118763  0#IBMDF:\n"
        "6   QUOTExEQUITY               Eurex International Business Machines Equity Future Continuation 1, Equity Future, USD, Eurex  21481052892   49450681    IBMFc1\n"
        "7   QUOTExEQUITY               Eurex International Business Machines Equity Future Continuation 2, Equity Future, USD, Eurex  21481053949   50092347    IBMFc2\n"
        "8   QUOTExEQUITY  Euronext Amsterdam IBM Single Stock Dividend Future Continuation 1, Equity Future, USD, Euronext Amsterdam  21613372305  260213021   IBMDFc1\n"
        "9   QUOTExEQUITY               Eurex International Business Machines Equity Future Continuation 3, Equity Future, USD, Eurex  21481053950   50092348    IBMFc3"
    )

    # given
    session = StubSession(is_open=True, response=SEARCH_QUERY_IBM_RESPONSE)
    set_default(session)

    # when
    testing_df = rd.discovery.search(query="IBM")

    # teardown
    set_default(None)

    # then
    testing_str = testing_df.to_string()
    assert testing_str == expected_srt
