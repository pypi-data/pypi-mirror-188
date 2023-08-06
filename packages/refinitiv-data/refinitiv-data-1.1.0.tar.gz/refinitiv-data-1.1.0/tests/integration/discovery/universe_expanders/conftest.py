from tests.integration.helpers import compare_list

FCHI_CONSTITUENTS = [
    "AIRP.PA",
    "AIR.PA",
    "ALSO.PA",
    "MT.AS",
    "AXAF.PA",
    "BNPP.PA",
    "BOUY.PA",
    "CAPP.PA",
    "CARR.PA",
    "CAGR.PA",
    "DANO.PA",
    "DAST.PA",
    "ENGIE.PA",
    "ESLX.PA",
    "EUFI.PA",
    "HRMS.PA",
    "PRTP.PA",
    "OREP.PA",
    "LVMH.PA",
    "LEGD.PA",
    "MICP.PA",
    "ORAN.PA",
    "PERP.PA",
    "PUBP.PA",
    "RENA.PA",
    "SAF.PA",
    "SGOB.PA",
    "SASY.PA",
    "SCHN.PA",
    "SOGN.PA",
    "STLA.PA",
    "STM.PA",
    "TEPRF.PA",
    "TCFP.PA",
    "TTEF.PA",
    "URW.AS",
    "VIE.PA",
    "SGEF.PA",
    "VIV.PA",
    "WLN.PA",
]

FCHI_SUMMARY_LINKS = [".DJI", "EUR=", "/.STOXX50E", ".FCHI", ".AD.FCHI"]

LSEG_PEERS_INSTRUMENTS = [
    "DB1Gn.DE",
    "ENX.PA",
    "SDR.L",
    "AMUN.PA",
    "DWSG.DE",
    "PGHN.S",
    "ABDN.L",
    "EQTAB.ST",
    "EMG.L",
    "HRGV.L",
    "III.L",
    "ASHM.L",
    "STAN.L",
    "ALLFG.AS",
    "NWG.L",
    "BPTB.L",
    "ANTIN.PA",
    "INGA.AS",
    "BARC.L",
    "UBSG.S",
    "LLOY.L",
    "ABNd.AS",
    "CBKG.DE",
    "BAER.S",
    "CSGN.S",
    "ICP.L",
    "TKOO.PA",
    "DBKGn.DE",
    "SJP.L",
    "HSBA.L",
    "ICE.N",
    "SPGI.N",
    "ERST.VI",
    "NDASE.ST",
    "ADYEN.AS",
    "KBC.BR",
    "NDAQ.OQ",
    "PUBP.PA",
    "COIN.OQ",
    "CME.OQ",
    "DANSKE.CO",
    "CABK.MC",
    "CBOE.Z",
    "VMUK.L",
    "JUP.L",
    "RAT.L",
    "QLT.L",
    "ITX.MC",
    "BBVA.MC",
    "ISP.MI",
]


def check_chain_discovery_object_for_attributes(chain, name, expected_constituents):
    assert chain.name == name, f"Discovery chain contain {chain.name}"
    compare_list(
        chain.constituents, expected_constituents
    ), f"Inconsistency in constituents list"
    assert hasattr(chain, "summary_links")


def is_iterable(obj):
    try:
        iter(obj)
    except TypeError:
        return False
    return True
