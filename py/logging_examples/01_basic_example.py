import logging
import sys

basic_format = '%(asctime)-15s %(name)s %(levelname)-8s %(message)s'
logging.basicConfig(format=basic_format)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")