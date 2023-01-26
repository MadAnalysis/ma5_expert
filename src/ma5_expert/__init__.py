import logging
import sys

from ma5_expert.system import logger

logger.init(LoggerStream=sys.stdout)
log = logging.getLogger("ma5_expert")
log.setLevel(logging.INFO)

from ma5_expert import cutflow
from ma5_expert import histogram
from ma5_expert import pad
from ma5_expert.backend import BackendManager, PADType
from ._version import __version__


__all__ = cutflow.__all__ + histogram.__all__ + pad.__all__ + ["BackendManager", "PADType"]
