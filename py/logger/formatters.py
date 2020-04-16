'''

o2o python json logging module example

todo:
    implement decorator for event 
    implement one line config for console vs file formatting, etc
    integrate filepaths with logstash/filebeat


'''
# %%
import json
from logging import Formatter
import sys
import traceback
from datetime import datetime
from k72.helpers.utils import cached_property
from k72.helpers.config import AppConfigContext

app = AppConfigContext()

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



class JsonFormatter(Formatter):
    '''
        JsonFormatter : extends logging.Formatter
    '''

    def __init__(self):
        '''
            return: AppLogContext
        '''
        self.app = AppLogContext()

    def get_event_args(self, record):
        '''
            input: record
            return: event_args
        '''
        event_args = {}
        event_args['module'] = record.module
        event_args['pathname'] = record.pathname
        event_args['funcName'] = record.funcName
        event_args['lineno'] = record.lineno
        event_args['thread'] = f'{record.threadName}[{record.thread}]'
        event_args['pid'] = record.process
        if record.exc_info or record.exc_text:
            event_args.update(self.get_exc_fields(record))
        return event_args

    def get_context(self, record):
        context = {}
        if hasattr(record, 'context'):
            context.update(record.context)
        return context

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

    def format(self, record):
        '''
            :param takes log record, function logging.Formatter.format\n
            :returns JSON Structured Logging Format
        '''

        json_log_object = {
            'app': self.app.applog,
            'event': record.event if hasattr(record, 'event') else 'UNKNOWN',
            'event_args': self.get_event_args(record),
            'created_at': datetime.utcnow().isoformat(),
            'logger': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
            'context': self.get_context(record)
        }

        return json.dumps(json_log_object)


json_formatter = JsonFormatter()

console_formatter = Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    import doctest
    doctest.testmod()

# %%
