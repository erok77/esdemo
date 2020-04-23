# JSON Structured Message Example
# ref: https://docs.python.org/3/howto/logging-cookbook.html#implementing-structured-logging
from __future__ import unicode_literals

import json
import logging

# This next bit is to ensure the script runs unchanged on 2.x and 3.x
try:
    unicode
except NameError:
    unicode = str

class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return tuple(o)
        elif isinstance(o, unicode):
            return o.encode('unicode_escape').decode('ascii')
        return super(Encoder, self).default(o)

class StructuredMessage:
    def __init__(self, message, **kwargs):
        self.kwargs = kwargs
        self.kwargs['message'] = message

    def __str__(self):
        s = Encoder().encode(self.kwargs)
        return s

_ = StructuredMessage   # optional, to improve readability


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    logging.debug(_("debug message", event="WWF_MAIN"))
    logging.info(_("info message", event="WWF_MAIN"))
    logging.warning(_("warning message", event="WWF_MAIN"))
    logging.error(_("error message", event="WWF_MAIN"))
    logging.critical(_("critical message", event="WWF_MAIN"))

