#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import traceback
import os

abs_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(abs_dir + "/../src/")
from pylogger_unified import logger as pylogger_unified
try:
    from StringIO import StringIO  # noqa
except ImportError:
    # Python 3 Support
    from io import StringIO

main_extra = {
    "main_extra1": "main_value1",
    "main_extra2": "main_value2"
}

extra = {
    "extra1": "value1",
    "extra2": "value2"
}


class TestLogger(unittest.TestCase):
    # def testColorFormat(self):
    #     fct_name = sys._getframe().f_code.co_name
    #     logger = pylogger_unified.init_logger(
    #         json_formatter=False,
    #         format_color=True,
    #         log_path=abs_dir + "/logs/" + fct_name + ".log",
    #         logger_name=fct_name
    #     )
    #     logger.info("This is the " + fct_name)
    #     logger.warning("This is the " + fct_name + " with extras", extra=extra)
    #     logger.error("This is the " + fct_name)

    # def testJsonFormat(self):
    #     fct_name = sys._getframe().f_code.co_name
    #     logger = pylogger_unified.init_logger(
    #         log_path=abs_dir + "/logs/" + fct_name + ".log",
    #         logger_name=fct_name
    #     )
    #     logger.info("This is the " + fct_name + " with extras", extra=extra)
    #     logger.warning("This is the " + fct_name)
    #     logger.error("This is the " + fct_name)

    def testExtraFormat(self):
        fct_name = sys._getframe().f_code.co_name
        sys.stdout = buffer = StringIO()
        logger = pylogger_unified.init_logger(
            log_path=abs_dir + "/logs/" + fct_name + ".log",
            logger_name=fct_name
        )
        logger.warning("This is the " + fct_name + " with lot of extras", extra=extra)
        logger.error("This is the " + fct_name)
        print("---")
        logger.info(buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
