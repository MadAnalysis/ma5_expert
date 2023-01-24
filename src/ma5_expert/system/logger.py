import logging
import sys


class ColoredFormatter(logging.Formatter):
    def __init__(self, msg):
        logging.Formatter.__init__(self, msg)

    def format(self, record):
        if record.levelno >= 40:  # ERROR
            color = (
                f"\x1b[31m Ma5 Expert - ERROR ({record.module}.{record.funcName}() "
                f"in {record.filename}::L{record.lineno}): "
            )
        elif record.levelno >= 30:  # WARNING
            color = (
                f"\x1b[35m Ma5 Expert - WARNING ({record.module}.{record.funcName}() "
                f"in {record.filename}::L{record.lineno}): "
            )
        elif record.levelno >= 20:  # INFO
            color = "\x1b[0m Ma5 Expert: "
        elif record.levelno >= 10:  # DEBUG
            color = (
                f"\x1b[36m Ma5 Expert - DEBUG ({record.module}.{record.funcName}() "
                f"in {record.filename}::L{record.lineno}): "
            )
        else:  # ANYTHING ELSE
            color = "\x1b[0m Ma5 Expert: "

        record.msg = color + str(record.msg) + "\x1b[0m"
        return logging.Formatter.format(self, record)


def init(LoggerStream=sys.stdout):
    rootLogger = logging.getLogger()
    hdlr = logging.StreamHandler()
    fmt = ColoredFormatter("%(message)s")
    hdlr.setFormatter(fmt)
    rootLogger.addHandler(hdlr)

    # we need to replace all root loggers by ma5 loggers for a proper
    # interface with madgraph5
    ma5Logger = logging.getLogger("ma5_expert")
    for hdlr in ma5Logger.handlers:
        ma5Logger.removeHandler(hdlr)
    hdlr = logging.StreamHandler(LoggerStream)
    fmt = ColoredFormatter("%(message)s")
    hdlr.setFormatter(fmt)
    ma5Logger.addHandler(hdlr)
    ma5Logger.propagate = False
