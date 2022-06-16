from ma5_expert.backend import PADType, Backend
from ma5_expert.system.exceptions import PADException, InvalidSamplePath, BackendException
from typing import Text, Dict, Optional
import os


def compute_exclusion(
    sample_path: Text,
    analysis: Text,
    dataset_name: Text,
    xsection: float,
    padtype: PADType,
    luminosity: Optional[float] = None,
) -> Dict:
    """
    Compute exclusion limit

    Parameters
    ----------
    dataset_name
    xsection
    backend: ma5_expert.backend.MadAnalysisBackend
        MadAnalysis 5 backedn
    sample_path: Text
        Path to the executed sample
    analysis: Text
        For which analysis this computation to be held
    dataset_name: Text
        name of the dataset
    xsection: float
        cross section value in pb.
    padtype: ma5_expert.backend.PADType
        Indicates the detector backend of the analysis
    luminosity: Optional[float]
        if none, default value will be used.

    Returns
    -------
    Dictionary including exclusion information on each region
    """

    if Backend.MadAnalysis5 is None:
        raise BackendException()

    if not os.path.isdir(sample_path):
        raise InvalidSamplePath(msg=f"Can not find sample {sample_path}", path=sample_path)

    run_recast = Backend.MadAnalysis5.get_run_recast(sample_path, padtype)

    ET = run_recast.check_xml_scipy_methods()
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

    cutflow_path = os.path.join(sample_path, "Output/SAF", dataset_name, analysis, "Cutflows")
    regiondata = run_recast.read_cutflows(cutflow_path, regions, regiondata)
    if regiondata == -1:
        raise PADException(
            msg=f"Problem occured during parsing the cutflows. please check: {cutflow_path}",
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
        regiondata = run_recast.pyhf_sig95Wrapper(lumi, regiondata, 'obs')

    regiondata = run_recast.extract_cls(regiondata, regions, xsection, lumi)

    return regiondata