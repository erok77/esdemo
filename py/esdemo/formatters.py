'''

o2o python json logging module example

format adherent to Elastic Common Schema (https://www.elastic.co/guide/en/ecs/current/ecs-field-reference.html#ecs-field-reference)


todo:
    implement decorator for event 
    implement one line config for console vs file formatting, etc
    integrate filepaths with logstash/filebeat


'''
# %%
import json
import logging
import sys
import traceback
from datetime import datetime
import time
from esdemo.utils import cached_property, exception, remove_none
from esdemo.config import AppConfigContext


__all__ = ['json_formatter','console_formatter']

app = AppConfigContext()

ECS_VERSION = '1.6'

class AppLogContext(object):
    
    def __init__(self, **kargs):
        self.app = {}
        self.app['code'] = app.code
        self.app['build_version'] = app.build_version
        self.app['git_branch'] = app.git_branch
        self.app['git_commit'] = app.git_commit
        self.app['name'] = app.name
        self.app['stage'] = app.stage

    @cached_property
    def applog(self):
        return self.app

def extra(**kw):
    ''' extra properties '''
    return {'extra': {'props': kw}}

class JsonFormatter(logging.Formatter):
    '''
        JsonFormatter : extends logging.Formatter
    '''
    def __init__(self):
        '''
            return: AppLogContext
        '''
        pass
        #self.app = AppLogContext()

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



if __name__ == "__main__":
    import doctest
    doctest.testmod()


"""
{
    "name": "esdemo.config",
    "msg": "Issue finding key SERVICE",
    "args": [],
    "levelname": "DEBUG",
    "levelno": 10,
    "pathname": "/Users/eric77/dev/on2one/esdemo/py/esdemo/config.py",
    "filename": "config.py",
    "module": "config",
    "exc_info": null,
    "exc_text": null,
    "stack_info": null,
    "lineno": 121,
    "funcName": "__getattr__",
    "created": 1587612497.436446,
    "msecs": 436.445951461792,
    "relativeCreated": 182.89494514465332,
    "thread": 4365325760,
    "threadName": "MainThread",
    "processName": "MainProcess",
    "process": 44253
}
"""
