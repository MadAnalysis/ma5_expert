import ma5_expert as ma5
import numpy as np
import os

cutflow_file = (
    "docs/examples/mass1000005_300.0_mass1000022_60.0_mass1000023_250.0_xs_5.689/Output/"
    "SAF/defaultset/atlas_susy_2018_31/Cutflows"
)


def test_collection():
    collection = ma5.cutflow.Collection(cutflow_file, xsection=5.689, lumi=139.0)

    SRs = [x.split(".saf")[0] for x in os.listdir(cutflow_file)]

    for sr in SRs:
        assert sr in collection.SRnames, f"Can not find region {sr}."
        assert hasattr(collection, sr), f"Collection does not have {sr} attribute."

    alive = ["SRA_M", "SRA_L", "SRA_H", "SRA", "SRC", "SRB", "SRC_24", "SRC_22"]
    current_alive = [x.id for x in collection.get_alive()]
    for sr in alive:
        assert sr in current_alive, f"{sr} is not within the alive regions."


def test_SRA():
    collection = ma5.cutflow.Collection(cutflow_file, xsection=5.689, lumi=139.0)
    SRA = collection.SRA

    # Initial cut
    assert SRA[0].sumW == 2.277976e01, f"Expected 2.277976e+01, got {SRA[0].sumW}"
    assert SRA[0].Nentries == 200000, f"Expected 200000, got {SRA[0].Nentries}"

    assert SRA[1].sumW == 1.440089e01, f"Expected 1.440089e+01, got {SRA[1].sumW}"
    assert SRA[1].Nentries == 156651, f"Expected 156651, got {SRA[1].Nentries}"

    assert SRA[2].sumW == 6.048645e00, f"Expected 6.048645e+00, got {SRA[2].sumW}"
    assert SRA[2].Nentries == 65546, f"Expected 65546, got {SRA[2].Nentries}"

    assert SRA[3].sumW == 1.840285e00, f"Expected 1.840285e+00, got {SRA[3].sumW}"
    assert SRA[3].Nentries == 19965, f"Expected 19965, got {SRA[3].Nentries}"

    assert SRA[4].sumW == 2.175267e-02, f"Expected 2.175267e-02, got {SRA[4].sumW}"
    assert SRA[4].Nentries == 191, f"Expected 191, got {SRA[4].Nentries}"

    assert SRA[5].sumW == 8.200151e-03, f"Expected 8.200151e-03, got {SRA[5].sumW}"
    assert SRA[5].Nentries == 72, f"Expected 72, got {SRA[5].Nentries}"

    assert SRA[6].sumW == 7.744776e-03, f"Expected 7.744776e-03, got {SRA[6].sumW}"
    assert SRA[6].Nentries == 68, f"Expected 68, got {SRA[6].Nentries}"

    assert SRA[7].sumW == 3.758569e-03, f"Expected 3.758569e-03, got {SRA[7].sumW}"
    assert SRA[7].Nentries == 33, f"Expected 33, got {SRA[7].Nentries}"

    assert SRA[8].sumW == 2.847176e-03, f"Expected 2.847176e-03, got {SRA[8].sumW}"
    assert SRA[8].Nentries == 25, f"Expected 25, got {SRA[8].Nentries}"

    assert SRA[9].sumW == 2.847176e-03, f"Expected 2.847176e-03, got {SRA[9].sumW}"
    assert SRA[9].Nentries == 25, f"Expected 25, got {SRA[9].Nentries}"

    assert SRA[10].sumW == 1.139115e-03, f"Expected 1.139115e-03, got {SRA[10].sumW}"
    assert SRA[10].Nentries == 10, f"Expected 10, got {SRA[10].Nentries}"

    assert SRA[11].sumW == 1.139115e-03, f"Expected 1.139115e-03, got {SRA[11].sumW}"
    assert SRA[11].Nentries == 10, f"Expected 10, got {SRA[11].Nentries}"
    assert SRA[11].rel_eff == 1.0, f"Expected 1, got {SRA[11].rel_eff}"
    assert (
        SRA[11].eff == 1.139115e-03 / SRA[0].sumW
    ), f"Expected {1.139115e-03 / SRA[0].sumW:.3f}, got {SRA[11].eff}"
