import logging
import sys
import coloredlogs

# Create a logger object.
logger = logging.getLogger(__name__)

# By default the install() function installs a handler on the root logger,
# this means that log messages from your code and log messages from the
# libraries that you use will all show up on the terminal.
coloredlogs.install(level='DEBUG', milliseconds=True)

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