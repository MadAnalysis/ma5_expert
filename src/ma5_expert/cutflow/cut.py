from math import sqrt
from dataclasses import dataclass, field
from typing import Any, Text, Optional
import logging

log = logging.getLogger("ma5_expert")


@dataclass
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

    name: Optional[Text] = "__unknown_cut__"
    Nentries: Optional[int] = None
    sumW: Optional[float] = None
    sumW2: Optional[float] = None
    _previous_cut: Optional[Any] = field(default=None, repr=False)
    _initial_cut: Optional[Any] = field(default=None, repr=False)
    xsec: Optional[float] = None
    _Nevents: Optional[float] = field(default=None, repr=False)
    lumi: float = -1.0

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
                    return 0.0
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
                log.warning(f"Previous entry (cut named {self._previous_cut.name}) has no MC event")
                return 0.0

        return -1

    @property
    def mc_unc(self) -> float:
        """
        Monte Carlo uncertainty
        """
        if self.Nentries > 0 and self.lumi > 0:
            return self.Nevents * sqrt(self.eff * (1.0 - self.eff) / float(self.Nentries))

        return 0.0

    @property
    def Nevents(self) -> float:
        if self._Nevents is not None:
            return self._Nevents
        else:
            if self.lumi >= 0.0:
                if self.xsec >= 0.0:
                    return self.xsec * self.eff * 1000.0 * self.lumi
                else:
                    return self.eff * self._initial_cut.Nevents
            else:
                log.warning("Luminosity haven't been set. Returning xsec X eff")
                return self.xsec * self.eff

    def __repr__(self):
        nentries = self.Nentries if self.Nentries is not None else -1
        txt = (
            f"  * {self.name} : \n"
            + f"     - Number of Entries    : {nentries:.0f}\n"
            + f"     - Number of Events     : {self.Nevents:.3f} ± {self.mc_unc:.3f}(ΔMC)\n"
            + f"     - Cut & Rel Efficiency : {self.eff:.3f}, {self.rel_eff:.3f}\n"
        )
        return txt

    def __str__(self):
        return self.__repr__()
