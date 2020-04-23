### server.py
# basic WSGI logging example 
# usage: gunicorn launch the app via command line 
# $> cd py/logging_examples/ 
# $> gunicorn -w 4 server:app --reload
###

import logging
import json
import time
from esdemo import default_handlers
from esdemo.utils import exception
from esdemo.formatters import JsonFormatter
from request_id import RequestIdMiddleware


import urllib3

logger = logging.getLogger(__name__)
default_handlers(logger)

@exception(logger)
def getapi(url):
    http = urllib3.PoolManager()
    res = http.request('GET', url)
    time.sleep(.53)
    return res


print(getapi('http://www.google.com'))

@exception(logger)
def app(environ, start_response):
    res = getapi('http://www.google.com')
    headers = [("content-type", "application/json")]

#    data = json.dumps(data)
    start_response("200 OK", headers)
    return [res.data]


class Remapper:
    def __init__(self, **kw):
        self.kw = kw
    
    def format(self, **kw):
        """
        res = {
            "http.request.bytes": kw["bytes"],
            "event.start": kw["REQUEST_ID"],
            "source.address": kw["REMOTE_ADDR"],
            "user.name": kw["REMOTE_USER"],
            "http.method": kw["REQUEST_METHOD"],
            "http.url.original": kw["REQUEST_URI"],
            "url.path": kw["REQUEST_PATH"],
            "host.ip": kw["HTTP_HOST"],
            "http.version": kw["HTTP_VERSION"],
            "http.referrer": kw["HTTP_REFERER"],
            "user_agent.original": kw["HTTP_USER_AGENT"],
            "event.start": kw["time"],
            "event.duration": kw["duration"],  
            "http.status_code": kw["status"]
        }
        return res
        """
        return kw

app = RequestIdMiddleware(
    app
#    format=Remapper()
)


logger_mw = logging.getLogger("request_id")
default_handlers(logger_mw)

if __name__ == "__main__":
    pass