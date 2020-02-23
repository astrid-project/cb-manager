# cspell:ignore kwrd

import importlib
import types


def copy_func(func, name=None):
    return types.FunctionType(func.__code__, func.__globals__, name or func.__name__, func.__defaults__, func.__closure__)

def fix_target(prop):
    return '_id' if prop == 'id' else prop


def wrap(data):
    return data if type(data) is list or type(data) is tuple else [data]


def docstring_parameter(**kwrd_params):
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
