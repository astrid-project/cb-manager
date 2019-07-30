from app import api, log
from datetime import datetime
from error import Error
import elasticsearch
from elasticsearch_dsl import Document as DocumentElastic
from flask import request
from flask_restplus import fields
from flask_api import status

class Document(DocumentElastic):
    response_model = api.model('response-data', {
        'date': fields.DateTime(description  = 'Execution datetime', required = True),
        'target': fields.String(description  = 'Target object', required = True),
        'action': fields.String(description  = 'Execution action', required = True),
        'success': fields.Boolean(description  = 'Execution performed with success or not', required = True)
    }, description = 'Response Data object')

    def get_id(self):
        return self.meta.id

    def to_dict_with_id(self):
        return dict(self.to_dict(), id = self.get_id())

    @classmethod
    def get_by_id(cls, id):
        return cls.get(id = id)

    @classmethod
    def exists(cls, id):
        return cls.get(id = id, ignore = 404) is not None

    @classmethod
    def init_with_try(cls):
        try:
            cls.error = Error(cls)
            cls.headers = {'Powered-by': 'ASTRID'}
            cls.init()
            log.info('%s init', cls.__name__)
        except Exception as e:
            cls.error.generic(e)
        return cls

    @classmethod
    def __data(cls, action, **kwargs):
        out = {
            'date': datetime.now().strftime('%Y/%m/%d-%H:%M:%S'),
            'target': cls.get_name(),
            'action': action,
            'success': True
        }
        out.update(kwargs)
        return out

    @classmethod
    def read_all(cls):
        try:
            return [item.to_dict_with_id() for item in cls.search().execute()], status.HTTP_200_OK, cls.headers
        except Exception as e:
            cls.error.generic(e)

    @classmethod
    def read_all_id(cls):
        print(cls.read_all())
        return [item.get_id() for item in cls.search().execute()]

    @classmethod
    def read_by(cls, **properties):
        try:
            return [item.to_dict_with_id() for item in cls.search().query('match', **properties).execute()], status.HTTP_200_OK, cls.headers
        except Exception as e:
            cls.error.generic(e)

    @classmethod
    def read_by_datetime(cls, property, before = None, after = None):
        try:
            return [item.to_dict_with_id() for item in cls.search().query('match', **{ property: { 'lte' : after, 'gte': before }}).execute()], status.HTTP_200_OK, cls.headers
        except Exception as e:
            cls.error.generic(e)

    @classmethod
    def read(cls, id):
        try:
            return cls.get_by_id(id).to_dict_with_id(), status.HTTP_200_OK, cls.headers
        except elasticsearch.NotFoundError:
            cls.error.not_found(id)
        except Exception as e:
            cls.error.generic(e)

    @classmethod
    def created(cls):
        data = request.json
        cls.error.validate_properties(**data)
        id = data['id']
        del data['id']
        if hasattr(cls, 'apply'): cls.apply(data)
        try:
            cls.get_by_id(id)
        except elasticsearch.NotFoundError:
            cls(meta = {'id': id}, **data).save()
            return cls.__data('create'), status.HTTP_201_CREATED, cls.headers
        except Exception as e:
            cls.error.generic(e)
        else:
            cls.error.found(id)

    @classmethod
    def updated(cls, id):
        data = request.json
        cls.error.validate_properties(id = id, **data)
        try:
            cls.get_by_id(id).update(**data)
            return cls.__data('update'), status.HTTP_202_ACCEPTED, cls.headers
        except elasticsearch.NotFoundError:
            cls.error.not_found(id)
        except Exception as e:
            cls.error.generic(e)

    @classmethod
    def deleted(cls, id):
        cls.error.validate_properties(id = id)
        try:
            cls.get_by_id(id).delete()
            return cls.__data('delete'), status.HTTP_202_ACCEPTED, cls.headers
        except elasticsearch.NotFoundError:
            cls.error.not_found(id)
        except Exception as e:
            cls.error.generic(e)

    @classmethod
    def deleted_by(cls, **properties):
        try:
            res = cls.search().query('match', **properties).execute().delete()
            print(res)
            return cls.__data('delete', success = res > 0, deleted = res), status.HTTP_202_ACCEPTED, cls.headers
        except Exception as e:
            cls.error.generic(e)