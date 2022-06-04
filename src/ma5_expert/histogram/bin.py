from dataclasses import dataclass, field


@dataclass(frozen=True)
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
    min: float
        min value of the xbin
    max: float
        max value of the xbin
    """

    sumW: float
    isUnderflow: bool
    isOverflow: bool
    min: float
    max: float

    def eff(self, total_sumw: float) -> float:
        """Return bin efficiency"""
        return self.sumW / total_sumw if total_sumw > 0 else float("inf")

    @property
    def center(self):
        return self.min + self.width / 2.0

    @property
    def width(self):
        return abs(self.max - self.min)

    def __add__(self, other):
        if (self.isUnderflow != other.isUnderflow) or (self.isOverflow != other.isOverflow):
            raise ValueError(f"Can not add different flow bins.")
        if self.max == other.min or self.min == other.max:
            return Bin(
                sumW=self.sumW + other.sumW,
                isOverflow=self.isOverflow,
                isUnderflow=self.isUnderflow,
                min=min(self.min, other.min),
                max=max(self.max, other.max),
            )
        else:
            raise ValueError(f"Can not merge non adjacent bins.\n{self}\n{other}")
