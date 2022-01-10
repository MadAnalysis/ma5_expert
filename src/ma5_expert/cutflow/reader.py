import logging
import math
import os
from typing import Text, Sequence, Optional

from ma5_expert.system.exceptions import InvalidInput
from ma5_expert.tools.SafReader import SAF
from .cut import Cut
from .objects import CutFlow

log = logging.getLogger("ma5_expert")


class Collection(object):
    def __init__(self, cutflow_path="", saf_file=False, **kwargs):
        """

        Parameters
        ----------
        collection_path : STR
            The path where all the cutflow saf files exist. The default is ''.
        saf_file : STR, optional
            Sample information file. The default is False.
        **kwargs :
            xsection : FLOAT
                Cross section value overwrite. The default is -1
            ID : STR
                Name of the collection. The default is SR-Collection
            lumi : FLOAT
                Luminosity overwrite. The Default is 1e-3

        Raises
        ------
        ValueError
            Raised if can't find collection path.

        Returns
        -------
        Cut flow collection.

        """
        self.SR_collection_path = ""
        xsec = kwargs.get("xsection", 0.0) + kwargs.get("xsec", 0.0)
        nevents = kwargs.get("nevents", None)
        self.lumi = kwargs.get("lumi", None)

        if saf_file != False:
            self.saf = SAF(saf_file=saf_file, xsection=xsec)
            xsec = self.saf.xsec

        self.collection_name = kwargs.get("name", "__unknown_collection__")
        self._srID = []

        if cutflow_path != "":
            if os.path.isdir(cutflow_path):
                self.cutflow_path = os.path.normpath(cutflow_path)
                self._readCollection(xsec, nevents)
            else:
                raise ValueError("Can't find the collection path! " + cutflow_path)

    def __getitem__(self, item):
        if item not in self._srID:
            raise InvalidInput(f"Unknown SR : {item}")
        for key, sr in self.items():
            if key == item:
                return sr

    def _readCollection(
        self, xsec: Optional[float] = None, nevents: Optional[float] = None
    ):
        for sr in [x for x in os.listdir(self.cutflow_path) if x.endswith(".saf")]:
            fl = os.path.join(self.cutflow_path, sr)
            with open(fl, "r") as f:
                cutflow = f.readlines()

            currentSR = CutFlow(sr.split(".")[0])

            i = 0
            while i < len(cutflow):
                if cutflow[i].startswith("<InitialCounter>"):
                    i += 2
                    current_cut = Cut(
                        name="Initial",
                        Nentries=int(cutflow[i].split()[0])
                        + int(cutflow[i].split()[1]),
                        sumw=float(cutflow[i + 1].split()[0])
                        + float(cutflow[i + 1].split()[1]),
                        sumw2=float(cutflow[i + 2].split()[0])
                        + float(cutflow[i + 2].split()[1]),
                        xsec=xsec,
                        Nevents=nevents,
                        lumi=self.lumi,
                    )
                    currentSR.addCut(current_cut)

                elif cutflow[i].startswith("<Counter>"):
                    i += 1
                    current_cut = Cut(
                        name=cutflow[i].split('"')[1],
                        Nentries=int(cutflow[i + 1].split()[0])
                        + int(cutflow[i + 1].split()[1]),
                        sumw=float(cutflow[i + 2].split()[0])
                        + float(cutflow[i + 2].split()[1]),
                        sumw2=float(cutflow[i + 3].split()[0])
                        + float(cutflow[i + 3].split()[1]),
                        xsec=xsec,
                        previous_cut=currentSR[-1],
                        initial_cut=currentSR[0],
                        lumi=self.lumi,
                    )
                    currentSR.addCut(current_cut)
                i += 1

            try:
                setattr(self, currentSR.id, currentSR)
                self._srID.append(currentSR.id)
            except Exception as err:
                log.error(err)
                currentSR.id = f"SR_{len(self.srID)}"
                setattr(self, currentSR.id, currentSR)
                self._srID.append(currentSR.id)

    @property
    def SRnames(self):
        return list(self.keys())

    def keys(self):
        return (x for x in self._srID)

    def items(self):
        return ((x, getattr(self, x)) for x in self._srID)

    def addSignalRegion(
        self,
        SR_name: Text,
        cut_names: Sequence[Text],
        cut_values: Sequence[float],
        Nentries=None,
    ):

        assert len(cut_names) == len(cut_values), (
            f"Cut names does not match with the values: "
            f"{len(cut_names)} != {len(cut_values)}"
        )

        if Nentries is None:
            Nentries = [math.inf] * len(cut_names)

        assert len(Nentries) == len(cut_values), (
            f"Cut values does not match with the MC number of events:"
            f" {len(Nentries)} != {len(cut_values)}"
        )

        SR = CutFlow(SR_name)
        for ix, (name, val, entries) in enumerate(zip(cut_names, cut_values, Nentries)):
            if ix == 0:
                current_cut = Cut(
                    name=name,
                    Nevents=val,
                    Nentries=entries,
                )
            else:
                current_cut = Cut(
                    name=name,
                    previous_cut=SR[-1],
                    initial_cut=SR[0],
                    Nevents=val,
                    Nentries=entries,
                )
            SR.addCut(current_cut)

        try:
            setattr(self, SR.id, SR)
            self._srID.append(SR.id)
        except Exception as err:
            log.error(err)
            SR.id = f"SR_{len(self.srID)}"
            setattr(self, SR.id, SR)
            self._srID.append(SR.id)

    def __repr__(self):
        txt = ""
        for ix, (key, item) in enumerate(self.items()):
            txt += (
                (ix != 0) * "\n\n\n" + "   * Signal Region : " + key + "\n" + str(item)
            )
        return txt

    def __str__(self):
        return self.__repr__()

    def get_alive(self):
        return [sr for id, sr in self.items() if sr.isAlive]

    @property
    def regiondata(self):
        regdat = {}
        for k, i in self.items():
            regdat[k] = i.regiondata[i.id]
        return regdat
