import os, re
import numpy as np
from decimal import Decimal
from typing import Text, MutableSequence, Union, Iterable, Tuple

from collections import OrderedDict

from .histo import Histo


class Collection:
    """
    Histogram collection
    Parameters
    ----------
    xsection: float
        Cross-section value in pb
    lumi: float
        Luminosity value in 1/fb
    fileLoc: Text
        exact path to MadAnalysis histogram output
    """

    histograms: MutableSequence[Histo]

    def __init__(self, fileLoc: Text, xsection: float, lumi: float) -> None:
        self._histograms = OrderedDict()
        self.xsection = xsection
        self.luminosity = lumi
        self.original_file = fileLoc

        rows = self._readHistos(fileLoc)
        for idx in np.unique([r["ID"] for r in rows]):
            current_histo = Histo()
            for hbin in rows:
                if hbin["ID"] == idx:
                    current_histo._add_bin(hbin)
            self.append(current_histo)

    @property
    def xsection(self) -> float:
        """Cross-section value in pb"""
        return self._xsection

    @xsection.setter
    def xsection(self, value: float):
        if value <= 0.0:
            raise ValueError("Cross section value can not be less or equal to zero.")
        self._xsection = value

    @property
    def luminosity(self) -> float:
        """Luminosity value in 1/fb"""
        return self._lumi

    @luminosity.setter
    def luminosity(self, value: float):
        if value <= 0.0:
            raise ValueError("Luminosity value can not be less or equal to zero.")
        self._lumi = value

    def __repr__(self) -> Text:
        txt = f"Collection of {self.size} histograms from {os.path.dirname(self.original_file)}\n"
        for key, item in self.items():
            txt += "   * " + item.__repr__() + "\n"
        return txt

    def set_weight_normalisation(self, sumW: float) -> None:
        """
        Set weight normalisation to sum of weights
        Parameters
        ----------
        sumW: float
            sum of weights
        """
        for key, item in self.items():
            item.weight_normalisation(sumW)

    def append(self, histogram: Histo):
        assert isinstance(histogram, Histo), "Wrong type of input."
        if histogram.name in self.histo_names:
            raise ValueError("Histogram already exists.")
        self._histograms.update({histogram.name: histogram})

    @property
    def histo_names(self) -> MutableSequence[Text]:
        return list(self._histograms.keys())

    @property
    def size(self) -> int:
        """Number of histograms"""
        return len(self.histo_names)

    def __getitem__(self, item: Union[Text, int]) -> Histo:
        if isinstance(item, int):
            if item < self.size:
                return self._histograms[self.histo_names[item]]
            else:
                raise ValueError("Input can not be larger than number of histograms.")

        return self._histograms.get(item, Histo())

    def items(self) -> Iterable:
        return self._histograms.items()

    def normalised_histogram(
        self, histo: Union[Text, int]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get Cross-section normalised histogram

        Parameters
        ----------
        histo: Union[Text, int]
            histogram name or ID

        Returns
        -------
        xbins, bins, weights which are normalised to cross section
        """
        histogram = self[histo]
        return histogram.xbins, histogram.bins, histogram.norm_weights(self.xsection)

    def lumi_histogram(self, histo: Union[Text, int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get luminosity normalised histogram

        Parameters
        ----------
        histo: Union[Text, int]
            histogram name or ID

        Returns
        -------
        xbins, bins, weights which are normalised to cross section
        """
        histogram = self[histo]
        return (
            histogram.xbins,
            histogram.bins,
            histogram.lumi_weights(self.xsection, self.luminosity),
        )

    def get_histogram(self, histo: Union[Text, int]) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get luminosity normalised histogram

        Parameters
        ----------
        histo: Union[Text, int]
            histogram name or ID

        Returns
        -------
        xbins, bins, weights which are normalised to cross section
        """
        histogram = self[histo]
        return histogram.xbins, histogram.bins, histogram.weights

    @staticmethod
    def _readHistos(fileLoc: Text) -> MutableSequence[dict]:
        """
        Utility function which parses a MadAnalysis5 *.saf file describing one
        or more histograms and is capable of translating them to a tidy format for
        further data analysis

        Actually read the file and produce a pandas dataframe representing it in
        a Tidy, denormalized table
        Keyword arguments:
        fileLoc -- the path and filename of the *.saf file

        Adapted from https://github.com/effofex/ma5-histo

        Returns: MutableSequence[dict]
        """
        # *.saf files are XML-ish, but not valid xml.  Also, the way we want to
        # represent them as a csv file will involve some derived values.  It's
        # probably not a good idea to just regex our way through this, but a
        # builtin XML parser isn't going to do the trick either, so let's try
        # a finite state machine approach first.

        # Overall goal is to populate a collection of dictionaries, with keys
        # corresponding to columns in our target pandas dataframe
        NONHISTO = 1
        HISTO = 2
        DESC = 3
        STATS = 4
        DATA = 5

        # both description and stats have some formatting too
        # to avoid nested state machines, we'll start with just keeping
        # track of line numbers.
        descLine = 0
        statsLine = 0

        # data is also line dependent, but very mildly, need to know line # to
        # determine the bin # and range
        dataLine = 0

        # it's not gauranteed that we'll get a unique descriptor for each histo, so
        # let's track an ID code
        ID = 0

        # the list of rows we'll eventually turn into a datframe and the dictionary
        # which represents a row (built as we go through the FSM)
        rows = []
        row = dict()
        readState = NONHISTO

        if not os.path.isfile(fileLoc):
            raise FileNotFoundError(f"Can not find {fileLoc}")

        with open(fileLoc) as fh:
            for l in fh:
                # We could be more elegant, for example do this as a dictionary
                # mapping of states and parse funcs.
                # First, let's just bang out a solution

                # Start in a state where we know we're not within a <Histo> tag
                # usually this means the SAF header or footer
                if readState == NONHISTO:
                    if re.search("<Histo>", l):
                        ID = ID + 1
                        row["ID"] = ID
                        readState = HISTO
                # A <Histo> tag can contain <Description>, <Statistics>, or <Data>
                # tags. Detect when those tags crop up or when the <Histo> element
                # closes
                elif readState == HISTO:
                    if re.search("</Histo>", l):
                        readState = NONHISTO
                    elif re.search("<Description>", l):
                        readState = DESC
                        # need to reset the line # of the description
                        # thus the entanglement of a large FSM begins
                        descLine = 0
                    elif re.search("<Statistics>", l):
                        readState = STATS

                        # similar element-level state reset as with description
                        statsLine = 0
                    elif re.search("<Data>", l):
                        readState = DATA
                        dataLine = 0
                # Handle a <Description> element. Assumes we  go back to a parent
                # <Histo> element when done.
                elif readState == DESC:
                    if re.search("</Description>", l):
                        readState = HISTO
                    else:
                        # description elements contain a few lines, each of which
                        # describe different bits of the histogram. For a rough
                        # implementation, we just keep track of the line # we're
                        # on, and parse accordingly

                        # TODO handle cases where these assumptions don't work
                        if descLine == 0:
                            m = re.search('"(.*)"', l)
                            row["name"] = m.group(1)
                        elif descLine == 2:
                            row["nbins"], row["xmin"], row["xmax"] = l.split()
                            row["xmin"] = "%.6E" % Decimal(row["xmin"])
                            row["xmax"] = "%.6E" % Decimal(row["xmax"])
                        elif descLine >= 4:
                            if "region" not in row.keys():
                                row["region"] = [l.split()[0]]
                            else:
                                row["region"].append(l.split()[0])
                        descLine = descLine + 1
                # Handle a <Statistics> element. Assumes we  go back to a parent
                # <Histo> element when done.
                elif readState == STATS:
                    if re.search("</Statistics>", l):
                        readState = HISTO
                    else:
                        # statistics elements are multi-line, handle similar to
                        # description elements

                        # TODO handle cases where these assumptions don't work
                        # TODO find out from @lemouth if we're handling second col
                        # correctly
                        if statsLine == 0:
                            lhs, rhs = map(int, l.split()[0:2])
                            row["nEvents"] = lhs - rhs
                        elif statsLine == 1:
                            lhs, rhs = map(float, l.split()[0:2])
                            row["normEwEvents"] = "%.6E" % Decimal((lhs - rhs))
                        elif statsLine == 2:
                            lhs, rhs = map(int, l.split()[0:2])
                            row["nEntries"] = lhs - rhs
                        elif statsLine == 3:
                            lhs, rhs = map(float, l.split()[0:2])
                            row["normEwEntries"] = "%.6E" % Decimal((lhs - rhs))
                        elif statsLine == 4:
                            lhs, rhs = map(float, l.split()[0:2])
                            row["sumWeightsSq"] = "%.6E" % Decimal((lhs - rhs))
                        elif statsLine == 5:
                            lhs, rhs = map(float, l.split()[0:2])
                            row["sumValWeight"] = "%.6E" % Decimal((lhs - rhs))
                        elif statsLine == 6:
                            lhs, rhs = map(float, l.split()[0:2])
                            row["sumValSqWeight"] = "%.6E" % Decimal((lhs - rhs))
                        statsLine = statsLine + 1

                # TODO retain diagnostic prints as 'verbose' output option?
                # Handle a <Data> element. Assumes we  go back to a parent
                # <Histo> element when done.
                elif readState == DATA:
                    if re.search("</Data>", l):
                        # at the end of the data element, we should have everything
                        # we need to write out a row for the dataframe, so let'saf
                        # store it in a dictionary, then add that to our collection
                        # TODO
                        readState = HISTO
                    else:
                        lhs, rhs = map(float, l.split()[0:2])
                        binWidth = (float(row["xmax"]) - float(row["xmin"])) / float(row["nbins"])
                        row["isUnderflow"] = dataLine == 0
                        row["isOverflow"] = dataLine > float(row["nbins"])
                        if row["isUnderflow"]:
                            binLbInc = -1 * np.inf
                            binUbExc = float(row["xmin"])
                            row["isUnderflow"] = True
                        elif row["isOverflow"]:
                            binLbInc = float(row["xmax"])
                            binUbExc = np.inf
                        else:
                            binLbInc = float(row["xmin"]) + binWidth * (dataLine - 1)
                            binUbExc = binLbInc + binWidth
                        tol = 1e-10
                        if abs(binLbInc) < tol:
                            binLbInc = 0e0
                        if abs(binUbExc) < tol:
                            binUbExc = 0e0
                        row["value"] = "%.6E" % Decimal(lhs - rhs)
                        row["binMin"] = "%.6E" % Decimal(binLbInc)
                        row["binMax"] = "%.6E" % Decimal(binUbExc)
                        rows.append(dict(row))
                        dataLine = dataLine + 1

        return rows
