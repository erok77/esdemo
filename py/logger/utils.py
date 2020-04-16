'''
Python helper class for caching properties and other things
'''
import json
from collections import namedtuple
import inspect
import pprint

class cached_property(object):
    def __init__(self, factory):
        self._attr_name = factory.__name__
        self._factory = factory

    def __get__(self, instance, owner):
        # add the attribute.
        attr = self._factory(instance)

        # Cache the value; hide ourselves.
        setattr(instance, self._attr_name, attr)

        return attr


def convert_bytes(bytes):
    bytes = float(bytes)
    magnitude = abs(bytes)
    if magnitude >= 1099511627776:
        terabytes = bytes / 1099511627776
        size = '%.2fT' % terabytes
    elif magnitude >= 1073741824:
        gigabytes = bytes / 1073741824
        size = '%.2fG' % gigabytes
    elif magnitude >= 1048576:
        megabytes = bytes / 1048576
        size = '%.2fM' % megabytes
    elif magnitude >= 1024:
        kilobytes = bytes / 1024
        size = '%.2fK' % kilobytes
    else:
        size = '%.2fb' % bytes
    return size


def get_insight():
    get_modules = inspect.getmembers('module')
    get_class = inspect.getmembers('class')
    for m in get_modules:
        print(m)
    for c in get_class:
        print(c)


import functools

def debug(func):
    """Print the function signature and return value"""
    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]                      # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)           # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")           # 4
        return value
    return wrapper_debug
#get_insight()

import time
from functools import wraps

def watch_time(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        duration = time.time() - start_time
        print(duration)
        return res
    return wrapped

import sys

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

def get_bytes(obj):
    return convert_bytes(get_size(obj))

def pp(obj):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(obj)

def remove_none(d):
    try:
        if not isinstance(d, (dict, list)):
            return d
        if isinstance(d, list):
            return [v for v in (remove_none(v) for v in d) if v]
        return {k: v for k, v in ((k, remove_none(v)) for k, v in d.items()) if v}
    except Exception as e:
        logger.exception('Issue stripping None vals from nested object')



import json
from collections import namedtuple

def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())

def json2obj(data):
    return json.loads(data, object_hook=_json_object_hook)

class DictWithAttributeAccess(dict):
    def __getattr__(self, key):
        return self[key]
 
    def __setattr__(self, key, value):
        self[key] = value

def fix_url(string):
    fix_dict = {' ':'%20','!':'%21','"':'%22','#':'%23','$':'%24',
                '&':'%26',"'":'%27','(':'%28',')':'%29',
                '*':'%2A','+':'%2b','.':'%2E','/':'%2F',':':'%3A',
                ';':'%3B','?':'%3F','@':'%40','{':'%7B','{':'%7D'}

    for k,v in fix_dict.items():
        if v in string:
            string = string.replace(v,k)

    return string

def ifkw(key, **kwargs):
    return kwargs[key] if key in kwargs else None