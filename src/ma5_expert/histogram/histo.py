import numpy as np

from .bin import Bin
from typing import Sequence, Text, Union, MutableSequence


class Histo:
    """
    Object oriented Histogram definition
    """

    name: Text
    ID: int
    _nbins: int
    regions: Sequence[Text]
    _nEvents: int
    _normEwEvents: float
    _nEntries: float
    _normEwEntries: float
    _sumWeightsSq: float
    _sumValWeight: float
    _sumValSqWeight: float
    _xmin: float
    _xmax: float
    _bins: MutableSequence[Bin]
    _normalisation_frac: Union[float, Text]

    def __init__(self):
        self.ID = -1
        self.name = "__unknown_histo__"
        self._nbins = 0
        self.regions = []
        self._nEvents = 0
        self._normEwEvents = 0
        self._nEntries = 0
        self._normEwEntries = 0
        self._sumWeightsSq = 0
        self._sumValWeight = 0
        self._sumValSqWeight = 0
        self._xmin = 0
        self._xmax = 0
        self._bins = []
        self._normalisation_frac = "_normEwEvents"

    def __repr__(self):
        return f"MadAnalysis 5 Histogram: {self.name}"

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
        return self._nbins

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
        if self.ID == -1 and self.name == "__unknown_histo__":
            self.ID = int(bin_info["ID"])
            self.name = bin_info["name"]
            self._nbins = int(bin_info["nbins"])
            self.regions = bin_info["region"]
            self._nEvents = int(bin_info["nEvents"])
            self._normEwEvents = float(bin_info["normEwEvents"])
            self._nEntries = float(bin_info["normEwEvents"])
            self._normEwEntries = float(bin_info["normEwEntries"])
            self._sumWeightsSq = float(bin_info["sumWeightsSq"])
            self._sumValWeight = float(bin_info["sumValWeight"])
            self._sumValSqWeight = float(bin_info["sumValSqWeight"])
            self._xmin = float(bin_info["xmin"])
            self._xmax = float(bin_info["xmax"])
            self._bins.append(
                Bin(
                    sumW=float(bin_info["value"]),
                    isUnderflow=bin_info["isUnderflow"],
                    isOverflow=bin_info["isOverflow"],
                )
            )

        else:
            assert (
                self.ID == int(bin_info["ID"]) and self.name == bin_info["name"]
            ), "Merging different types of histograms are not allowed."
            self._bins.append(
                Bin(
                    sumW=float(bin_info["value"]),
                    isUnderflow=bin_info["isUnderflow"],
                    isOverflow=bin_info["isOverflow"],
                )
            )

    def _w(self, weight: float):
        return np.array(
            [
                b.eff(self.weight_normalisation) * weight
                for b in self._bins
                if not (b.isOverflow or b.isUnderflow)
            ],
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
        return np.linspace(self._xmin, self._xmax, self.size + 1)

    @property
    def xbins(self) -> np.ndarray:
        """Get central location of each bin"""
        bins = self.bins
        return np.array(
            [bins[idx] + (bins[idx + 1] - bins[idx]) / 2.0 for idx in range(len(bins) - 1)],
            dtype=np.float32,
        )
