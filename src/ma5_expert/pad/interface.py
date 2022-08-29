from ma5_expert.backend import PADType, BackendManager
from ma5_expert.system.exceptions import PADException, InvalidSamplePath, BackendException
from typing import Text, Dict, Optional, Callable, List
import os
from dataclasses import dataclass

CustomCutFlowReader = Callable[
    [Text, List[Text], Dict[Text, Dict[Text, float]]], Dict[Text, Dict[Text, float]]
]


@dataclass
class PADInterface:
    """
    PAD Interface

    sample_path: Text
        Path to the executed sample
    dataset_name: Text
        name of the dataset

    """

    __slots__ = "sample_path", "dataset_name"

    sample_path: Text
    dataset_name: Text

    def compute_exclusion(
        self,
        analysis: Text,
        xsection: float,
        padtype: PADType,
        luminosity: Optional[float] = None,
        info_file: Optional[Text] = None,
        custom_cutflow_reader: Optional[CustomCutFlowReader] = None,
        expectation_assumption: Text = "apriori",
    ) -> Dict:
        """
        Compute exclusion limit

        Parameters
        ----------
        analysis: Text
            For which analysis this computation to be held
        xsection: float
            cross section value in pb.
        padtype: ma5_expert.backend.PADType
            Indicates the detector backend of the analysis
        luminosity: Optional[float]
            if none, default value will be used.
        info_file: Optional[Text]
            Optional info file path. if None it will be read from PAD.
        custom_cutflow_reader: Callable
            A user defined function that takes cutflow path, list of regions and region data
            and returns updated region data.
        expectation_assumption: Text
            assumption on expectation value computation.

        Returns
        -------
        Dictionary including exclusion information on each region
        """

        if BackendManager.MadAnalysis5 is None:
            raise BackendException()

        if not os.path.isdir(self.sample_path) and custom_cutflow_reader is not None:
            raise InvalidSamplePath(
                msg=f"Can not find sample {self.sample_path}", path=self.sample_path
            )

        run_recast = BackendManager.MadAnalysis5.get_run_recast(
            self.sample_path, padtype, expectation_assumption
        )

        ET = run_recast.check_xml_scipy_methods()
        run_recast.SetCLsCalculator()

        lumi: float
        regions: List[Text]
        regiondata: Dict[Text, Dict[Text, float]]

        if info_file:
            if not os.path.isfile(info_file):
                raise PADException(f"Can not find info file: {info_file}")
            with open(info_file, "r") as info_input:
                info_tree = ET.parse(info_input)
            lumi, regions, regiondata = run_recast.header_info_file(
                info_tree, analysis, "default" if luminosity is None else luminosity
            )
        else:
            lumi, regions, regiondata = run_recast.parse_info_file(
                ET, analysis, "default" if luminosity is None else luminosity
            )

        if -1 in [lumi, regions, regiondata]:
            info_path = os.path.join(
                run_recast.pad, "Build/SampleAnalyzer/User/Analyzer", analysis + ".info"
            )
            raise PADException(
                msg=f"Problem with info file. please check: {info_path}",
                details={
                    "lumi": lumi,
                    "regions": regions,
                    "regiondata": regiondata,
                    "info_path": info_path,
                },
            )

        cutflow_path = os.path.join(
            self.sample_path, "Output/SAF", self.dataset_name, analysis, "Cutflows"
        )

        if custom_cutflow_reader is not None:
            regiondata = custom_cutflow_reader(cutflow_path, regions, regiondata)
        else:
            if not os.path.isdir(cutflow_path):
                raise InvalidSamplePath(
                    msg=f"Can not find cutflows at {cutflow_path}", path=cutflow_path
                )
            regiondata = run_recast.read_cutflows(cutflow_path, regions, regiondata)
            if regiondata == -1:
                raise PADException(
                    msg=f"Problem occurred during parsing the cutflows. please check: {cutflow_path}",
                    details={"cutflow_path": cutflow_path},
                )

        regiondata = run_recast.extract_sig_cls(regiondata, regions, lumi, "exp")
        if run_recast.cov_config != {}:
            regiondata = run_recast.extract_sig_lhcls(regiondata, lumi, "exp")
        elif run_recast.pyhf_config != {}:
            # CLs calculation for pyhf
            regiondata = run_recast.pyhf_sig95Wrapper(lumi, regiondata, "exp")
        regiondata = run_recast.extract_cls(regiondata, regions, xsection, lumi)

        if luminosity is None:
            if run_recast.cov_config != {}:
                regiondata = run_recast.extract_sig_lhcls(regiondata, lumi, "obs")
            regiondata = run_recast.extract_sig_cls(regiondata, regions, lumi, "obs")
            regiondata = run_recast.pyhf_sig95Wrapper(lumi, regiondata, "obs")

        regiondata = run_recast.extract_cls(regiondata, regions, xsection, lumi)

        return regiondata
