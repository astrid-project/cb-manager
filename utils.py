from args import Args
from colorama import Fore, Style
from datetime import datetime

import hashlib
import importlib
import types
import uuid


def copy_func(func, name=None):
    """
    Copy function with a new name.

    :param func: function to copy
    :param name: new name
    :returns: copied function
    """
    return types.FunctionType(func.__code__, func.__globals__, name or func.__name__, func.__defaults__, func.__closure__)


def docstring_parameter(**kwrd_params):
    """
    Generate automatic docstring for the class with a decorator.

    :returns: decorator
    """
    def decorator(self):
        for method in 'get', 'post', 'delete', 'put':
            base_mth = getattr(self, f'on_base_{method}')
            mth = getattr(self, f'on_{method}', None)
            if not callable(mth):
                setattr(self, f'on_{method}', copy_func(base_mth, f'on_{method}'))
                mth = getattr(self, f'on_{method}', None)
            with open(f'./api/{kwrd_params.get("docstring", "base")}/{method}.docstring', 'r') as file:
                mth.__doc__ = file.read().format(**kwrd_params)
            module = importlib.import_module('schema')
            schema = getattr(module, kwrd_params.get('schema', ''))
            setattr(self, 'tag', { 'name': kwrd_params.get('tag', ''), 'description': schema.__doc__.strip(' \n') })
        return self
    return decorator


def fix_target(prop):
    """
    Fix the field name for ElasticSearch.

    :param prop: field name to fix
    :returns: field name fixed
    """
    return '_id' if prop == 'id' else prop


def generate_password():
    """
    Generate a random password.

    :returns: random password
    """
    return hash(str(uuid.uuid1()))


def get_timestamp(ts = datetime.now()):
    """
    Set the timestamp in format %Y/%m/%d %H:%M:%S.

    :params ts: Timestamp to format
    :returns: Timestamp in format %Y/%m/%d %H:%M:%S
    """
    return ts.strftime('%Y/%m/%d %H:%M:%S')


def hash(text):
    """
    Make a hash of the text

    :param text: text to make the hash
    :returns: hashed version of the text
    """
    return hashlib.sha224(text.encode('utf-8')).hexdigest()


def wrap(data):
    """
    Wrap the data if an array if it is ont a list of tuple.

    :param data: data to wrap
    :returns: wrapped data
    """
    return data if type(data) is list or type(data) is tuple else [data]

