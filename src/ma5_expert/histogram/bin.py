class Bin:
    """
    Histogram bin object

    Parameters
    ----------
    sumw: float
        sum of weights
    bin_max: float
        maximum bin limit
    bin_min: float
        minimum bin limit
    underflow: bool
        is this underflow bin
    overflow: bool
        is this overflow bin
    """
    def __init__(
        self,
        sumw: float,
        underflow: bool = False,
        overflow: bool = False,
    ):
        self._sumw = sumw
        self._underflow = underflow
        self._overflow = overflow

    @property
    def isUnderflow(self) -> bool:
        """ Is this underflow bin? """
        return self._underflow

    @property
    def isOverflow(self) -> bool:
        """ Is this overflow bin? """
        return self._overflow

    @property
    def sumW(self) -> float:
        """ Sum of Weights """
        return self._sumw

    def eff(self, total_sumw: float) -> float:
        """ Return bin efficiency """
        return self._sumw / total_sumw if total_sumw > 0 else float("inf")
