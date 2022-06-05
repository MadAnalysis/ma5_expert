import numpy as np
from copy import deepcopy
from .bin import Bin
from typing import Text, Union, MutableSequence
from dataclasses import dataclass, field


@dataclass
class Histogram:
    """
    Object-oriented Histogram definition
    """

    name: str = field(default="__unknown_histo__", init=False)
    ID: int = field(default=-1, repr=False, init=False)
    _nbins: int = field(default=0, repr=False, init=False)
    regions: MutableSequence[str] = field(default_factory=list, init=False)
    _nEvents: int = field(default=0, init=False, repr=False)
    _normEwEvents: float = field(init=False, default=0.0, repr=False)
    _nEntries: int = field(init=False, default=0, repr=False)
    _normEwEntries: float = field(init=False, default=0, repr=False)
    _sumWeightsSq: float = field(init=False, default=0, repr=False)
    _sumValWeight: float = field(init=False, default=0, repr=False)
    _sumValSqWeight: float = field(init=False, default=0, repr=False)
    _xmin: float = field(init=False, default=0, repr=False)
    _xmax: float = field(init=False, default=0, repr=False)
    _bins: MutableSequence[Bin] = field(default_factory=list, init=False, repr=False)
    _normalisation_frac: Union[float, Text] = field(init=False, default="_normEwEvents", repr=False)

    def __str__(self) -> Text:
        return (
            f"{self.name}: [ nbin: {self.size:.0f}, min: {self._xmin:.2f}, max: {self._xmax:.2f} ]"
        )

    @property
    def weight_normalisation(self) -> float:
        """
        Retrun the weight normalisation factor. Typically this is the value to normalise the
        sum of weights per bin, hence the total sum of weights of the sample. By default,
        weigted sum of entries are used.
        """
        if isinstance(self._normalisation_frac, str):
            return getattr(self, self._normalisation_frac)
        else:
            return self._normalisation_frac

    @weight_normalisation.setter
    def weight_normalisation(self, value: float):
        if not isinstance(value, float):
            raise ValueError("Input can only be float.")
        self._normalisation_frac = value

    @property
    def size(self):
        return len(self._bins)

    def _add_bin(self, bin_info: dict) -> None:
        """
        Add a bin to the histogram

        Parameters
        ----------
        bin_info: dict
            bin information

        Raises
        -------
        AssertionError:
            If the histogram name and ID information does not match the info can not be added.
        """
        if self.ID == -1 and self.name == "__unknown_histo__" and len(self._bins) == 0:
            self.ID = int(bin_info["ID"])
            self.name = bin_info["name"]
            self._nbins = int(bin_info["nbins"])
            self.regions = bin_info["region"]
            self._nEvents = int(bin_info["nEvents"])
            self._normEwEvents = float(bin_info["normEwEvents"])
            self._nEntries = int(bin_info["nEntries"])
            self._normEwEntries = float(
                bin_info["normEwEntries"]
            )  # sum of event-weights over entries
            self._sumWeightsSq = float(bin_info["sumWeightsSq"])  # sum weights^2
            self._sumValWeight = float(bin_info["sumValWeight"])  # sum value*weight
            self._sumValSqWeight = float(bin_info["sumValSqWeight"])  # sum value^2*weight
            self._xmin = float(bin_info["xmin"])
            self._xmax = float(bin_info["xmax"])

            bin_min, bin_max = np.linspace(self._xmin, self._xmax, self._nbins + 1)[:2]

            isFlow = bin_info["isUnderflow"] or bin_info["isOverflow"]

            if bin_info["isUnderflow"]:
                self._underflow = Bin(
                    sumW=float(bin_info["value"]),
                    isUnderflow=bin_info["isUnderflow"],
                    isOverflow=bin_info["isOverflow"],
                    min=bin_min if not isFlow else -1,
                    max=bin_max if not isFlow else -1,
                )
            elif bin_info["isOverflow"]:
                self._overflow = Bin(
                    sumW=float(bin_info["value"]),
                    isUnderflow=bin_info["isUnderflow"],
                    isOverflow=bin_info["isOverflow"],
                    min=bin_min if not isFlow else -1,
                    max=bin_max if not isFlow else -1,
                )
            else:
                self._bins.append(
                    Bin(
                        sumW=float(bin_info["value"]),
                        isUnderflow=bin_info["isUnderflow"],
                        isOverflow=bin_info["isOverflow"],
                        min=bin_min if not isFlow else -1,
                        max=bin_max if not isFlow else -1,
                    )
                )

        else:
            assert (
                self.ID == int(bin_info["ID"]) and self.name == bin_info["name"]
            ), "Merging different types of histograms are not allowed."

            if bin_info["isUnderflow"]:
                self._underflow = Bin(
                    sumW=float(bin_info["value"]),
                    isUnderflow=bin_info["isUnderflow"],
                    isOverflow=bin_info["isOverflow"],
                    min=-1,
                    max=-1,
                )
            elif bin_info["isOverflow"]:
                self._overflow = Bin(
                    sumW=float(bin_info["value"]),
                    isUnderflow=bin_info["isUnderflow"],
                    isOverflow=bin_info["isOverflow"],
                    min=-1,
                    max=-1,
                )
            else:
                if len(self._bins) == 0:
                    bin_min, bin_max = np.linspace(self._xmin, self._xmax, self._nbins + 1)[:2]
                else:
                    bin_min, bin_max = self._bins[-1].max, self._bins[-1].max + self._bins[-1].width
                self._bins.append(
                    Bin(
                        sumW=float(bin_info["value"]),
                        isUnderflow=bin_info["isUnderflow"],
                        isOverflow=bin_info["isOverflow"],
                        min=bin_min,
                        max=bin_max,
                    )
                )

    def _w(self, weight: float):
        return np.array(
            [b.eff(self.weight_normalisation) * weight for b in self._bins],
            dtype=np.float32,
        )

    @property
    def weights(self) -> np.ndarray:
        """Get weights of the histogram"""
        return self._w(1.0)

    def norm_weights(self, xsec: float) -> np.ndarray:
        """
        Normalised bin weights with respect to cross-section.
        This function does not include overflow or underflow bins

        Parameters
        ----------
        xsec: float
            cross section in pb
        """
        return self._w(xsec)

    def lumi_weights(self, xsec: float, lumi: float) -> np.ndarray:
        """
        Normalised bin weights with respect to cross section and luminosity.
        This function does not include overflow or underflow bins

        Parameters
        ----------
        xsec: float
            cross-section in pb
        lumi: float
            luminosity in 1/fb
        """
        return self._w(xsec * 1000.0 * lumi)

    @property
    def bins(self) -> np.ndarray:
        """Get upper and lower limits of binned histogram"""
        return np.array([self._bins[0].min, self._bins[0].max] + [b.max for b in self._bins[1:]])

    @property
    def xbins(self) -> np.ndarray:
        """Get central location of each bin"""
        return np.array([b.center for b in self._bins])

    def merge_tail(self, nbins: int) -> None:
        last_bin = self._bins[-1]
        bins = deepcopy(self._bins)
        for idx in range(self.size - 2, self.size - 1 - nbins, -1):
            last_bin = last_bin + self._bins[idx]
            bins.remove(self._bins[idx])
        bins[-1] = last_bin
        self._bins = bins
