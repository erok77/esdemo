
import logging

from esdemo import default_handlers
from esdemo.utils import exception

logger = logging.getLogger('generator')
#default_handlers(logger)

import urllib3

@exception(logger)
def func1():
    http = urllib3.PoolManager()
    url = 'htetp://webcode.me'

    resp = http.request('GET', url)
    print(resp.status)

logger.debug("test",extra={"event":"test123"})

@exception(logger)
def zero_divide():
    1 / 0
if __name__ == '__main__':
    pass
    #zero_divide()


func1()
#def func1():
#    logger.debug("debug called from base.func1()")
#    logger.critical("critical called from base.func1()")

#func1()




# goals 
### > produce 1 simple unstructured logging example (add color)
### > produce 1 simple structured logging example (json)
### > pull up 1 structured logging example, with urllib (add exception)
### > demonstrate use of request-id via request-id package

#https://github.com/mmerickel/request-id