__version__='0.0.1'

from ma5_expert.CutFlow.CutFlowReader import Collection as CutFlowCollection
from ma5_expert.CutFlow.CutFlowTable  import CutFlowTable

import logging
import sys

from ma5_expert.system import logger
logger.init(LoggerStream=sys.stdout)
log = logging.getLogger("ma5_expert")
log.setLevel(logging.INFO)

