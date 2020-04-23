### 
# On2One ESDEMO Python logging examples
# this file is piecemilled from code found in the esdemo/__init__.py, esdemo/formatters.py & esdemo/utils.py

import logging
import sys
import time
import functools
import json
import logging
import traceback
from datetime import datetime
import coloredlogs

# esdemo/formatters.py
ECS_VERSION = '1.6'
class JsonFormatter(logging.Formatter):
    '''
        JsonFormatter : extends logging.Formatter
    '''
    def __init__(self):
        pass

    def get_exc_fields(self, record):
        '''
            returns execution/exception info for log record
        '''
        if record.exc_info:
            exc_info = self.format_exception(record.exc_info)
        else:
            exc_info = record.exc_text
        return {f'exc_info': exc_info}

    @classmethod
    def format_exception(cls, exc_info):
        return ''.join(traceback.format_exception(*exc_info)) if exc_info else ''

    def format(self, record, *args, **kw):
        '''
            :param takes log record, function logging.Formatter.format\n
            :returns JSON Structured Logging Format
        '''
        json_log_object = {
            '@timestamp': datetime.utcnow().isoformat(),
            'ecs': {'version': ECS_VERSION},
            'error': {
                'stack_trace': self.get_exc_fields(record)
            },
            'event': {
                'created': datetime.utcfromtimestamp(record.created).isoformat(),
                'module': record.module
            },
            'log': {
                'level': record.levelname,
                'logger': record.name,
                'origin': {
                    'file': {
                        'line': record.lineno,
                        'name': record.filename,
                        'fullpath': record.pathname,
                    },
                    'function': record.funcName,
                }
            },            
            'message': record.getMessage(),
            'process': {
                'pid': record.process,
                'name': record.name,
                    'thread': {
                        'id': record.thread,
                        'name': record.threadName,
                    }
            }        
        }
        return json.dumps(remove_none(json_log_object))

json_formatter = JsonFormatter()

console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# esdemo/__init__.py excerpts
LOGLEVEL = logging.DEBUG
STAGE = 'dev'
SERVICE = 'svc'
DEFAULT_FORMATTER = json_formatter
DEFAULT_LOGFILEPATH = '/Users/eric77/dev/on2one/esdemo/logs/app.json' ### update this with your log path (consistent with env:APP_LOGPATH)
coloredlogs.install(level='DEBUG', microseconds=True)


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
    handler.formatter.converter = time.gmtime
    return handler 

def default_handlers(logger):
    console_handler = stream_handler(level=logging.DEBUG)
    logger.addHandler(console_handler)
    f_handler = file_handler(level=logging.DEBUG, formatter=json_formatter)
    logger.addHandler(f_handler)
    return logger


logger = logging.getLogger()
default_handlers(logger) 
logger = logging.getLogger(__name__)

# helper function for exceptions
# ref >> http://www.blog.pythonlibrary.org/2016/06/09/python-how-to-create-an-exception-logging-decorator/
# esdemo/utils.py

def exception(logger):
    """
    A decorator that wraps the passed in function and logs 
    exceptions should one occur
    
    @param logger: The logging object
    """
    def decorator(func):
    
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                logger.exception(err)
            
            # re-raise the exception
            raise
        return wrapper
    return decorator

### NO REALLY WTAF!?!?
@exception(logger)
def zero_divide():
    1 / 0


def remove_none(d):
    try:
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [v for v in (remove_none(v) for v in d) if v]
        return {k: v for k, v in ((k, remove_none(v)) for k, v in d.items()) if v}
    except Exception as e:
        logger.exception('Issue stripping None vals from nested object')




if __name__ == "__main__":    
    logger.setLevel(logging.DEBUG)
    logger = default_handlers(logger)
    logger.debug("debug message",{"extra":'test',"event":'test2'})
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")
    zero_divide()