Red = "\x1b[31m"
End = "\x1b[0m"

from typing import Optional, Text, Dict


class InvalidInput(Exception):
    """Invalid Domain Exception"""

    def __init__(self, message="Invalid Input!"):
        super(InvalidInput, self).__init__(Red + message + End)


class MadAnalysisPath(Exception):
    """Invalid MadAnalysis 5 path"""

    def __init__(self, msg: str = "Invalid path", path: Optional[str] = None):
        self.path = path if path is not None else "__unknown_path__"
        super(MadAnalysisPath, self).__init__(Red + msg + End)


class PADException(Exception):
    """An exception has occurred in PAD"""

    def __init__(
        self,
        msg: Optional[Text] = "An exception has occurred in PAD",
        details: Optional[Dict] = None,
    ) -> None:
        self.details = details
        super(PADException, self).__init__(Red + msg + End)


class InvalidSamplePath(Exception):
    """Invalid Sample path"""

    def __init__(self, msg: str = "Invalid path", path: Optional[str] = None):
        self.path = path if path is not None else "__unknown_path__"
        super(InvalidSamplePath, self).__init__(Red + msg + End)


class BackendException(Exception):
    """Invalid backend"""

    def __init__(self, msg: Text = "Please set a valid backend"):
        super(BackendException, self).__init__(Red + msg + End)


class VersionException(Exception):
    """Unsopported version"""

    def __init__(self, msg: Text = "Unsupported version detected", version: Optional[Text] = None):
        self.version = version
        super(VersionException, self).__init__(Red + msg + End)
