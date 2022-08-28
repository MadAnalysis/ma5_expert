from dataclasses import dataclass
import os, sys

from ma5_expert.system.exceptions import MadAnalysisPath
from typing import Optional, Text, Union
from enum import Enum, auto


class PADType(Enum):
    PAD = "PAD"
    PADForSFS = "PADForSFS"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value


class ExpectationAssumption(Enum):
    APRIORI = "apriori"
    APOSTERIORI = "aposteriori"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @classmethod
    def get(cls, value):
        if isinstance(value, ExpectationAssumption):
            return value
        elif isinstance(value, str):
            if value.lower() == str(ExpectationAssumption.APRIORI):
                return ExpectationAssumption.APRIORI
            else:
                return ExpectationAssumption.APOSTERIORI


@dataclass
class MadAnalysisBackend:
    """
    Sets MadAnalysis 5 BackendManager

    madanalysis_path: str
        MadAnalysis 5 path
    debug_mode: Optional[bool]
        Run MadAnalysis in debug mode
    dev_mode: Optional[bool]
        Enable developer mode
    enforce_pad: Optional[bool]
        Enforce PAD. Note that this assumes that PAD is installed.
    enforce_padforsfs: Optional[bool]
        Enforce PADForSFS. Note that this assumes that PADForSFS is installed.
    """

    madanalysis_path: str
    debug_mode: Optional[bool] = False
    dev_mode: Optional[bool] = False
    enforce_pad: Optional[bool] = False
    enforce_padforsfs: Optional[bool] = False

    def __post_init__(self):
        # Setup MadAnalysis 5
        if self.madanalysis_path not in sys.path:
            sys.path.insert(0, self.madanalysis_path)

        # Adding the python service folder to the current PYTHONPATH
        servicedir = os.path.normpath(
            os.path.join(self.madanalysis_path, "tools/ReportGenerator/Services")
        )
        if not os.path.isdir(servicedir):
            raise MadAnalysisPath(
                f"Detected MadAnalysis 5 service folder is not correct: {self.madanalysis_path}",
                self.madanalysis_path,
            )
        sys.path.insert(0, servicedir)

        from madanalysis.core.main import Main
        from madanalysis.enumeration.ma5_running_type import MA5RunningType

        self.ma5_main = Main()
        self.ma5_main.mode = MA5RunningType.RECO

        self.ma5_main.forced = False
        self.ma5_main.script = True
        self.ma5_main.developer_mode = self.dev_mode
        self.ma5_main.debug = self.debug_mode
        self.ma5_main.InitObservables(self.ma5_main.mode)
        self.ma5_main.archi_info.ma5dir = self.madanalysis_path

        self.ma5_main.CheckConfig(debug=self.debug_mode)
        self.ma5_main.CheckConfig2(debug=self.debug_mode)
        self.ma5_main.recast = "on"
        # Enforce pad note that this requires PAD to be downloaded otherwise the code will crash
        if not self.ma5_main.session_info.has_pad:
            self.ma5_main.session_info.has_pad = self.enforce_pad
        if not self.ma5_main.session_info.has_padsfs:
            self.ma5_main.session_info.has_padsfs = self.enforce_padforsfs

    def get_run_recast(
        self,
        sample_path: Text,
        padtype: PADType,
        expectation_assumption: Union[ExpectationAssumption, Text] = ExpectationAssumption.APRIORI,
    ):
        """
        Get run recast class

        Parameters
        ----------
        sample_path: Text
            PAth of the MadAnalysis workspace
        expectation_assumption: ExpectationAssumption
            assumption on expectation

        Returns
        -------
        initialized run recast class
        """
        from logging import DEBUG
        from madanalysis.misc.run_recast import RunRecast

        self.ma5_main.recasting.expectation_assumption = str(
            ExpectationAssumption.get(expectation_assumption)
        )

        run_recast = RunRecast(self.ma5_main, sample_path)
        if padtype == PADType.PAD:
            run_recast.pad = os.path.join(self.madanalysis_path, "tools/PAD")
        elif padtype == PADType.PADForSFS:
            run_recast.pad = os.path.join(self.madanalysis_path, "tools/PADForSFS")
        if self.debug_mode:
            run_recast.logger.setLevel(DEBUG)
        return run_recast
