from elasticsearch_dsl import Document
from elasticsearch_dsl.utils import AttrList
from http import HTTPStatus
from log import Log
from query_parser import QueryParser

import elasticsearch
import falcon
import utils


class BaseResource(object):
    def __init__(self):
        self.log = Log.get(self.doc_cls.Index.name)
        try:
            self.log.info(f'start initialization index {self.doc_cls.Index.name}')
            self.doc_cls.init()
        except Exception as e:
            self.log.debug(e)
            self.log.error(f'initialization index {self.doc_cls.Index.name} not possible')
            self.log.info('try again')
            self.__init()
        else:
            self.log.success(f'index {self.doc_cls.Index.name} initialized')

    def on_base_get(self, req, resp, id=None):
        try:
            response = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {}), id=id
            ).execute()
            resp.media = [dict(hit.to_dict(), id=hit.meta.id)
                          for hit in response]
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error,
                description=req_error.info
            )

    def on_base_post(self, req, resp, id=None):
        res = []
        query = req.context.get('json', [])
        if id is not None:
            if type(query) is list:
                raise falcon.HTTPBadRequest(
                    title='id provided',
                    description=f'Request can create only 1 new {self.doc_name}'
                )
            single = True
        else:
            single = False
        for data in utils.wrap(query):
            data_id = data.pop('id', None)
            if data_id is not None and single:
                res.append({
                    'status': 'error',
                    'reason': f'Request not valid: two ids provided',
                    'id': [data_id, id],
                    'http_status_code': HTTPStatus.CONFLICT
                })
            else:
                try:
                    if data_id is not None:
                        obj = self.doc_cls.get(id=data_id, ignore=404)
                        meta = { 'id': data_id }
                    else:
                        obj = None
                        meta = {}
                    if obj is None:
                        obj = self.doc_cls(meta=meta, **data)
                        status = obj.save()
                        res.append({
                            'status': status,
                            'data': { 'id': obj.meta.id, **obj.to_dict() },
                            'http_status_code': HTTPStatus.CREATED
                        })
                    else:
                        res.append({
                            'status': 'error',
                            'reason': f'{self.doc_name} with the given [id] already found',
                            'id': obj.meta.id,
                            'http_status_code': HTTPStatus.CONFLICT
                        })
                except Exception as e:
                    self.log.debug(e)
                    res.append({
                        'status': 'error',
                        'reason': f'Not possible create {self.doc_name} with the given [data]',
                        'data': { 'id': id, **data },
                        'http_status_code': HTTPStatus.UNPROCESSABLE_ENTITY
                    })
        resp.media = res

    def on_base_delete(self, req, resp, id=None):
        try:
            res = []
            response = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {}), id=id
            ).execute()
            for hit in response:
                try:
                    obj = self.doc_cls.get(id=hit.meta.id)
                    data = obj.to_dict()
                    obj.delete()
                    res.append({
                        'status': 'deleted',
                        'data': { **data, 'id': hit.meta.id },
                        'http_status_code': HTTPStatus.OK
                    })
                except Exception as e:
                    self.log.debug(e)
                    res.append({
                        'status': 'error',
                        'reason': f'Not possible to delete element with the given [id]',
                        'id': hit.meta.id,
                        'http_status_code': HTTPStatus.CONFLICT
                    })
            resp.media = res
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error,
                description=req_error.info
            )

    def on_base_put(self, req, resp, id=None):
        res = []
        query = req.context.get('json', [])
        if id is not None:
            if type(query) is list:
                raise falcon.HTTPBadRequest(
                    title='id provided',
                    description=f'Request can create only 1 new {self.doc_name}'
                )
            single = True
        else:
            single = False
        for data in utils.wrap(query):
            data_id = data.pop('id', None)
            data_add = {k: v for k, v in data.items() if k.startswith('+')}
            data = {k: v for k, v in data.items() if not k.startswith('+')}
            if data_id is None and not single:
                res.append({
                    'status': 'error',
                    'reason': 'Request not valid: id property not found',
                    'http_status_code': HTTPStatus.NOT_FOUND
                })
            elif data_id is not None and single:
                res.append({
                    'status': 'error',
                    'reason': f'Request not valid: two ids provided',
                    'id': [data_id, id],
                    'http_status_code': HTTPStatus.CONFLICT
                })
            else:
                try:
                    obj = self.doc_cls.get(id=data_id)
                    for name, values in  data_add.items():
                        for item in utils.wrap(values):
                            field = name.replace('+', '')
                            o = getattr(obj, field)
                            if not type(o) == AttrList:
                                setattr(obj, field, utils.wrap(o))
                            getattr(obj, field).append(item)
                    if len(data) > 0:
                        status = obj.update(**data)
                    else:
                        status = obj.save()
                    res.append({
                        'status': status,
                        'data': { **obj.to_dict(), 'id': data_id },
                        'http_status_code': HTTPStatus.OK
                    })
                except elasticsearch.NotFoundError as not_found_error:
                    self.log.debug(not_found_error)
                    res.append({
                        'status': 'error',
                        'reason': f'{self.doc_name} with the given [id] not found',
                        'id': data_id,
                        'http_status_code': HTTPStatus.NOT_FOUND
                    })
        resp.media = res
