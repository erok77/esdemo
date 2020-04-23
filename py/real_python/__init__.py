# __init__.py
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def add_module_handler(logger):
    logger.addHandler(stream_handler)


def stream_handler(destination=sys.stdout):
    handler = logging.StreamHandler(destination)
    return handler
