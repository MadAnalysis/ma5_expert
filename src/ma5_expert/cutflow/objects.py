import logging
from typing import Text, Sequence

from ma5_expert.system.exceptions import InvalidInput
from .cut import Cut

log = logging.getLogger("ma5_expert")


class CutFlow:
    """
    Collection of cuts

    Parameters
    ----------
    cutflow : Sequence[Cut]
        list of cuts
    """

    def __init__(
        self, name: Text = "__unknown_cutflow__", cutflow: Sequence[Cut] = None
    ):
        self.id = name
        if cutflow is None:
            self._data = []
        else:
            for cut in cutflow:
                self.addCut(cut)

    def __getitem__(self, item):
        return self._data[item]

    def addCut(self, cut: Cut):
        if isinstance(cut, Cut):
            self._data.append(cut)
        else:
            raise InvalidInput("Unknown input.")

    @property
    def final_cut(self):
        return self._data[-1]

    @property
    def isAlive(self):
        if self.final_cut.Nentries is not None:
            return self.final_cut.Nentries > 0
        return self.final_cut.Nevents > 0.0

    @property
    def xsec(self):
        return self._data[0].xsec

    @xsec.setter
    def xsec(self, val: float):
        for cut in self:
            cut.xsec = xsec

    @property
    def lumi(self):
        return self._data[0].lumi

    @lumi.setter
    def lumi(self, val: float):
        for cut in self:
            cut._lumi = lumi

    @property
    def CutNames(self):
        return list(self.keys())

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return (cut for cut in self._data)

    def items(self):
        return ((ix, cut) for ix, cut in enumerate(self._data))

    def keys(self):
        return (cut.id for cut in self._data)

    def getCut(self, id):
        for cut in self:
            if cut.id == id:
                return cut

        return None

    @property
    def regiondata(self):
        return {self.id: {"Nf": self.final_cut.sumW, "N0": self[0].sumW}}

    def __repr__(self):
        txt = f"* {self.id} :\n"
        for cut in self:
            txt += cut.__repr__()
        return txt
