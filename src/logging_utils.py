import logging
import os
from datetime import datetime


def logger(moduleName):
    """
    Setup a log
    """
    logger = logging.getLogger(moduleName)
    logging.basicConfig(level=logging.DEBUG,
                        filename="../log/log_" +
                        datetime.now().strftime("%Y%m%d%H%M%S") + ".txt",
                        format="%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(message)s")
    return logger
