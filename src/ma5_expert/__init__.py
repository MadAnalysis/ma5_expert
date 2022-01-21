__version__ = '1.0.3'

import logging
import sys

from ma5_expert.system import logger

logger.init(LoggerStream = sys.stdout)
log = logging.getLogger("ma5_expert")
log.setLevel(logging.INFO)

from ma5_expert import cutflow

__all__ = cutflow.__all__
