"""
    On2One ESDEMO Python logging module example
    
"""
# %%
import logging
import sys
from logging import INFO, WARN, DEBUG, ERROR, CRITICAL, FileHandler, StreamHandler
from formatters import json_formatter,console_formatter
from config import ConfigContext

conf = ConfigContext()

LOGLEVEL = conf.LOGLEVEL
STAGE = conf.STAGE
SERVICE = conf.SERVICE
DEFAULT_FORMATTER = json_formatter
#DEFAULT_FORMATTER = console_formatter
DEFAULT_LOGFILEPATH = './logs/app.json'


def clear_logger(logger):
    logger.debug('init >>> logger handlers')
    logger.debug('deleting {count} handlers from {logger}'.format(
        count=len(logger.handlers), logger=logger))
    for index, h in enumerate(logger.handlers):
        handler_delete = logger.handlers[index]
        logger.debug(handler_delete)
        logger.removeHandler(handler_delete)
    logger.debug('deleted')
    logger.debug(logger.handlers)
    return logger

def get_file_handler(level=LOGLEVEL, formatter=DEFAULT_FORMATTER, destination=DEFAULT_LOGFILEPATH):
    handler=logging.FileHandler(destination)
    handler.setLevel(level)
    handler.formatter=formatter
    return handler

def get_stream_handler(level=LOGLEVEL, formatter=DEFAULT_FORMATTER, destination=sys.stdout):
    handler = StreamHandler(destination)
    handler.setLevel(level)
    handler.formatter = formatter
    return handler

def logging_config_dev(logger):
    #clear_logger(logger)
    console_handler = get_stream_handler(level=INFO, formatter=console_formatter)
    logger.addHandler(console_handler)
    console_file_handler = get_file_handler(level=DEBUG, formatter=json_formatter)
    logger.addHandler(console_file_handler)
    return logger

def logging_config_default(logger):
    clear_logger(logger)
    logger.setLevel(INFO)
    handler = get_stream_handler(level=INFO)
    logger.addHandler(handler)
    return logger


logger = logging.getLogger(SERVICE)
#logger.setLevel("DEBUG")

if STAGE == 'dev':
    logger = logging_config_dev(logger)

else: 
    logger = logging_config_default(logger)


# %%
def loglevel_tests():
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    print(LOGLEVEL)

# %%
def diag():
    logger.parent
    logger.getEffectiveLevel
    loglevel_tests()

loglevel_tests()
