
#    On2One ESDEMO Python logging examples

import logging
import sys
import time
from esdemo.formatters import json_formatter,console_formatter
from esdemo.config import ConfigContext
from esdemo.utils import exception
import coloredlogs

coloredlogs.install(level='DEBUG', microseconds=True)

conf = None #ConfigContext()

LOGLEVEL = logging.DEBUG
STAGE = 'dev'
SERVICE = 'svc'
DEFAULT_FORMATTER = json_formatter
#DEFAULT_FORMATTER = console_formatter
DEFAULT_LOGFILEPATH = '/Users/eric77/dev/on2one/esdemo/logs/app.json'

def stream_handler(level=LOGLEVEL, formatter=DEFAULT_FORMATTER, destination=sys.stdout):
    handler = logging.StreamHandler(destination)
    handler.setLevel(level)
    handler.formatter = formatter
    handler.formatter.converter = time.gmtime
    return handler

def file_handler(level=LOGLEVEL, formatter=DEFAULT_FORMATTER, destination=DEFAULT_LOGFILEPATH):
    handler=logging.FileHandler(destination)
    handler.setLevel(level)
    handler.formatter=formatter
    return handler 

def default_handlers(logger):
    console_handler = stream_handler(level=logging.DEBUG)
    logger.addHandler(console_handler)
    f_handler = file_handler(level=logging.DEBUG, formatter=json_formatter)
    logger.addHandler(f_handler)
    return logger


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger = default_handlers(logger)

def loglevel_tests():   

    logger.debug("debug message",{"extra":'test',"event":'test2'})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    zero_divide()


### usage, place the following at the top of your code
# import logging
logger = logging.getLogger()
default_handlers(logger)

#loglevel_tests()