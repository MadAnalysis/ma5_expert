from math import sqrt

from ma5_expert.system.exceptions import InvalidInput

from typing import List, Any, Union, Tuple, Text, Dict, Sequence, Optional
import logging

log = logging.getLogger("ma5_expert")


class Cut:
    """
    Cut object

    Parameters
    ----------
    name : str
        name of the cut
    Nentries : int
        number of monte carlo events
    sumw : float
        sum of weights
    sumw2 : float
        sum of square of weights
    previous_cut : Cut
        Cut which has been applied before the current cut
    initial_cut : Cut
        initial cut in the cutflow
    xsec : float
        cross section [pb]
    Nevents : float
        number of events
    lumi : float
        luminosity [fb^-1]
    """

    def __init__(
        self,
        name: Optional[Text] = "__unknown_cut__",
        Nentries: Optional[int] = None,
        sumw: Optional[float] = None,
        sumw2: Optional[float] = None,
        previous_cut: Optional[Any] = None,
        initial_cut: Optional[Any] = None,
        xsec: Optional[float] = None,
        Nevents: Optional[float] = None,
        lumi: Optional[float] = None,
    ):

        self.id = name  # Name of the cut
        self.Nentries = Nentries if Nentries is not None else 0  # Number of MC events
        self._sumW = sumw  # sum of weights
        self._sumW2 = sumw2  # sum of square of the weights
        self._initial_cut = initial_cut
        self._previous_cut = previous_cut
        self._lumi = lumi
        self._xsection = xsec

        if Nevents is not None:
            self._Nevents = Nevents

    @property
    def sumW(self):
        """
        Sum of weights
        """
        return self._sumW

    @property
    def xsec(self) -> float:
        """
        Cross section [pb]
        """
        if hasattr(self, "_xsection"):
            return self._xsection
        else:
            return -1

    @xsec.setter
    def xsec(self, val: float) -> None:
        self._xsection = xsec
        if hasattr(self, "_Nevents"):
            delattr(self, "_Nevents")

    @property
    def lumi(self):
        if self._lumi is not None:
            return self._lumi
        return -1

    @property
    def eff(self):
        """
        cumulative efficiency
        """
        if isinstance(self._initial_cut, Cut):
            if self.sumW is not None:
                try:
                    return self.sumW / self._initial_cut.sumW
                except ZeroDivisionError as err:
                    return 0.
            else:
                try:
                    return float(self.Nevents) / self._initial_cut.Nevents
                except ZeroDivisionError as err:
                    return 0.0
        else:
            return 1

    @property
    def rel_eff(self):
        """
        relative efficiency
        """
        if isinstance(self._previous_cut, Cut):
            if self.sumW is not None:
                try:
                    return self.sumW / self._previous_cut.sumW
                except ZeroDivisionError:
                    return -1
            else:
                try:
                    return float(self.Nevents) / self._previous_cut.Nevents
                except ZeroDivisionError as err:
                    return 0.0
        else:
            return 1

    @property
    def mc_eff(self):
        """
        Monte Carlo efficiency
        """
        if isinstance(self._initial_cut, Cut) and self.Nentries is not None:
            try:
                return self.Nentries / self._initial_cut.Nentries
            except ZeroDivisionError as err:
                log.warning("Initial entries has no MC event")
                return 0.0

        return -1

    @property
    def mc_rel_eff(self):
        """
        Monte Carlo relative efficiency
        """
        if isinstance(self._previous_cut, Cut) and self.Nentries is not None:
            try:
                return self.Nentries / self._previous_cut.Nentries
            except ZeroDivisionError as err:
                log.warning("Previous entry has no MC event")
                return 0.0

        return -1

    @property
    def mc_unc(self) -> float:
        """
        Monte Carlo uncertainty
        """
        if self.Nentries > 0 and self._lumi is not None:
            return self.Nevents * sqrt(
                self.eff * (1.0 - self.eff) / float(self.Nentries)
            )

        return 0.0

    @property
    def Nevents(self) -> float:
        if hasattr(self, "_Nevents"):
            return self._Nevents
        else:
            if self.lumi >= 0.0:
                if self.xsec >= 0.0:
                    return self.xsec * self.eff * 1000.0 * self._lumi
                else:
                    return self.eff * self._initial_cut.Nevents
            else:
                log.warning("Luminosity haven't been set. Returning xsec X eff")
                return self.xsec * self.eff

    def __repr__(self):
        nentries = self.Nentries if self.Nentries is not None else -1
        txt = (
            f"  * {self.id} : \n"
            + f"     - Number of Entries    : {nentries:.0f}\n"
            + f"     - Number of Events     : {self.Nevents:.3f} ± {self.mc_unc:.3f}(ΔMC)\n"
            + f"     - Cut & Rel Efficiency : {self.eff:.3f}, {self.rel_eff:.3f}\n"
        )
        return txt

    def __str__(self):
        return self.__repr__()
