from datetime import datetime
import json

__all__ = [
    'dumps',
    'loads'
]


def __converter(obj):
    if isinstance(obj, datetime):
        return obj.__str__()


def dumps(data, *args, **kwargs):
    return json.dumps(data, *args, default=__converter, **kwargs)


def loads(data, *args, **kwargs):
    return json.loads(data, *args, **kwargs)
