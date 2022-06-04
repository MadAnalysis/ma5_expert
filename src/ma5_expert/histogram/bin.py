from dataclasses import dataclass


@dataclass
class Bin:
    """
    Histogram bin object

    Parameters
    ----------
    sumW: float
        sum of weights
    isUnderflow: bool
        is this underflow bin
    isOverflow: bool
        is this overflow bin
    """

    sumW: float
    isUnderflow: bool
    isOverflow: bool

    def eff(self, total_sumw: float) -> float:
        """Return bin efficiency"""
        return self.sumW / total_sumw if total_sumw > 0 else float("inf")
