import ma5_expert as ma5
import numpy as np

histo_file = (
    "examples/mass1000005_300.0_mass1000022_60.0_mass1000023_250.0_xs_5.689/Output/"
    "SAF/defaultset/atlas_susy_2018_31/Histograms/histos.saf"
)


def test_reader():
    """Test histogram reader basics"""
    collection = ma5.histogram.Collection(
        original_file=histo_file, xsection=2.193581363835e-05, lumi=137.0
    )

    histo_names = ["SRA_Meff", "SRA_Mh", "SRB_PTj1", "SRB_MhAvg", "SRC_MET", "SRC_Sig"]
    for idx, hist in enumerate(histo_names):
        if collection.histo_names[idx] != hist:
            raise IndexError("Histogram ordering is wrong")

    assert collection.xsection == 2.193581363835e-05
    assert collection.lumi == 137.0 == collection.luminosity
    assert collection.size == 6
    assert collection.original_file == histo_file


def test_SRA_Meff():
    """test the results of SRA_Meff"""
    collection = ma5.histogram.Collection(
        original_file=histo_file, xsection=2.193581363835e-05, lumi=137.0
    )

    SRA_Meff = collection["SRA_Meff"]
    assert SRA_Meff.name == "SRA_Meff"
    assert SRA_Meff.regions == ["SRA"], f"Expected ['SRA'], got {SRA_Meff.regions}"
    assert SRA_Meff._nbins == 11, f"Expected 11, got {SRA_Meff._nbins}"
    assert [x.sumW for x in SRA_Meff._bins] == [
        0.0,
        2.277358e-04,
        3.416810e-04,
        2.279074e-04,
        0.0,
        2.278284e-04,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]

    # <Statistics> L0
    assert SRA_Meff._nEvents == 10, f"Expected 10, got {SRA_Meff._nEvents}"
    # <Statistics> L1
    assert (
        SRA_Meff._normEwEvents == 1.139115e-03
    ), f"Expected 1.139115e-03, got {SRA_Meff._normEwEvents}"
    # <Statistics> L2
    assert SRA_Meff._nEntries == 10, f"Expected 10, got {SRA_Meff._nEntries}"
    # <Statistics> L3
    assert (
        SRA_Meff._normEwEntries == 1.139115e-03
    ), f"Expected 1.139115e-03, got {SRA_Meff._normEwEntries}"
    # <Statistics> L4
    assert (
        SRA_Meff._sumWeightsSq == 1.297583e-07
    ), f"Expected 1.297583e-07, got {SRA_Meff._sumWeightsSq}"
    # <Statistics> L5
    assert (
        SRA_Meff._sumValWeight == 1.828939e00
    ), f"Expected 1.828939e+00, got {SRA_Meff._sumValWeight}"
    # <Statistics> L6
    assert (
        SRA_Meff._sumValSqWeight == 3.316870e03
    ), f"Expected 3.316870e+03, got {SRA_Meff._sumValSqWeight}"


def test_SRA_Mh():
    """test the results of SRA_Mh"""
    collection = ma5.histogram.Collection(
        original_file=histo_file, xsection=2.193581363835e-05, lumi=137.0
    )

    SRA_Mh = collection["SRA_Mh"]
    assert SRA_Mh.name == "SRA_Mh"
    assert SRA_Mh.regions == ["SRA"], f"Expected ['SRA'], got {SRA_Mh.regions}"
    assert SRA_Mh._nbins == 12, f"Expected 12, got {SRA_Mh._nbins}"
    assert [x.sumW for x in SRA_Mh._bins] == [
        4.554236e-04,
        1.252638e-03,
        7.972762e-04,
        2.278764e-04,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
    ]
    assert (
        SRA_Mh._overflow.sumW == 1.139622e-04
    ), f"Expected 1.139622e-04, got {SRA_Mh._overflow.sumW}"

    # <Statistics> L0
    assert SRA_Mh._nEvents == 25, f"Expected 25, got {SRA_Mh._nEvents}"
    # <Statistics> L1
    assert (
        SRA_Mh._normEwEvents == 2.847176e-03
    ), f"Expected 2.847176e-03, got {SRA_Mh._normEwEvents}"
    # <Statistics> L2
    assert SRA_Mh._nEntries == 25, f"Expected 25, got {SRA_Mh._nEntries}"
    # <Statistics> L3
    assert (
        SRA_Mh._normEwEntries == 2.847176e-03
    ), f"Expected 2.847176e-03, got {SRA_Mh._normEwEntries}"
    # <Statistics> L4
    assert (
        SRA_Mh._sumWeightsSq == 3.242567e-07
    ), f"Expected 3.242567e-07, got {SRA_Mh._sumWeightsSq}"
    # <Statistics> L5
    assert (
        SRA_Mh._sumValWeight == 3.106979e-01
    ), f"Expected 3.106979e-01, got {SRA_Mh._sumValWeight}"
    # <Statistics> L6
    assert (
        SRA_Mh._sumValSqWeight == 1.129757e02
    ), f"Expected 1.129757e+02, got {SRA_Mh._sumValSqWeight}"


def test_SRB_PTj1():
    """test the results of SRB_PTj1"""
    collection = ma5.histogram.Collection(
        original_file=histo_file, xsection=2.193581363835e-05, lumi=137.0
    )

    SRB_PTj1 = collection["SRB_PTj1"]
    assert SRB_PTj1.name == "SRB_PTj1"
    assert SRB_PTj1.regions == ["SRB"], f"Expected ['SRB'], got {SRB_PTj1.regions}"
    assert SRB_PTj1._nbins == 9, f"Expected 9, got {SRB_PTj1._nbins}"
    assert SRB_PTj1._xmin == 5.000000e01, f"Expected 5.000000e+01, got {SRB_PTj1._xmin}"
    assert SRB_PTj1._xmax == 9.500000e02, f"Expected 5.000000e+01, got {SRB_PTj1._xmax}"

    bin_sumW = [
        0.0,
        1.139142e-04,
        3.414924e-04,
        1.024837e-03,
        4.556432e-04,
        5.695884e-04,
        2.278284e-04,
        3.416330e-04,
        0.0,
    ]

    assert [x.sumW for x in SRB_PTj1._bins] == bin_sumW

    xsec, lumi = 2.193581363835e-05, 137.0

    assert (
        SRB_PTj1.weights.tolist()
        == np.array([w / 3.074937e-03 for w in bin_sumW], dtype=np.float32).tolist()
    )

    assert (
        SRB_PTj1.norm_weights(xsec=xsec).tolist()
        == np.array([xsec * w / 3.074937e-03 for w in bin_sumW], dtype=np.float32).tolist()
    )

    assert (
        SRB_PTj1.lumi_weights(xsec=xsec, lumi=lumi).tolist()
        == np.array(
            [xsec * 1000.0 * lumi * w / 3.074937e-03 for w in bin_sumW], dtype=np.float32
        ).tolist()
    )

    assert SRB_PTj1._overflow.sumW == 0.0, f"Expected 0.0, got {SRB_PTj1._overflow.sumW}"

    # <Statistics> L0
    assert SRB_PTj1._nEvents == 27, f"Expected 27, got {SRB_PTj1._nEvents}"
    # <Statistics> L1
    assert (
        SRB_PTj1._normEwEvents == 3.074937e-03
    ), f"Expected 3.074937e-03, got {SRB_PTj1._normEwEvents}"
    # <Statistics> L2
    assert SRB_PTj1._nEntries == 27, f"Expected 27, got {SRB_PTj1._nEntries}"
    # <Statistics> L3
    assert (
        SRB_PTj1._normEwEntries == 3.074937e-03
    ), f"Expected 3.074937e-03, got {SRB_PTj1._normEwEntries}"
    # <Statistics> L4
    assert (
        SRB_PTj1._sumWeightsSq == 3.501942e-07
    ), f"Expected 3.501942e-07, got {SRB_PTj1._sumWeightsSq}"
    # <Statistics> L5
    assert (
        SRB_PTj1._sumValWeight == 1.562016e00
    ), f"Expected 1.562016e+00, got {SRB_PTj1._sumValWeight}"
    # <Statistics> L6
    assert (
        SRB_PTj1._sumValSqWeight == 8.721591e02
    ), f"Expected 8.721591e+02, got {SRB_PTj1._sumValSqWeight}"
