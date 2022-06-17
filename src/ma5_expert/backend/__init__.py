from .ma5_backend import MadAnalysisBackend, PADType


class BackendManager:
    MadAnalysis5 = None

    @staticmethod
    def set_madanalysis_backend(
        madanalysis_path: str,
        debug_mode: bool = False,
        dev_mode: bool = False,
        enforce_pad: bool = False,
        enforce_padforsfs: bool = False,
    ) -> None:
        """
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
        BackendManager.MadAnalysis5 = MadAnalysisBackend(
            madanalysis_path,
            debug_mode,
            dev_mode,
            enforce_pad,
            enforce_padforsfs,
        )
