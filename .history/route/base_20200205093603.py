import falcon
from query_parser import QueryParser
import elasticsearch
from utils import wrap


class BaseResource(object):
    path = '/'

    def on_get(self, req, resp, id=None):
        try:
            res = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {}, id=id)
            ).execute()
            resp.media = [dict(item.to_dict(), id=item.meta.id)
                               for item in res]
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error, description=req_error.info)

    def on_post(self, req, resp, id=None):
        res = []
        query = req.context.get('json', [])
        if id is not None:
            if type(query) is list:
                raise falcon.HTTPBadRequest(
                    title='id provided', description=f'Request can create only 1 new {self.doc_name}')
            single = True
        else:
            single = False
        res_code = falcon.HTTP_201
        for data in wrap(query):
            data_id = data.pop('id')
            if data_id is None and not single:
                res.append({
                    'id':
                    'status': 'error',
                    'title': 'Request not valid',
                    'description': 'id property not found'
                })
                res_code = falcon.HTTP_NOT_FOUND
            elif data_id is not None and single:
                res.append({
                    'id':
                    'status': 'error',
                    'title': 'Request not valid',
                    'description': 'id provided'
                })
                res_code = falcon.HTTP_CONFLICT
            try:
                self.doc_cls.get(id=data_id)
            except elasticsearch.NotFoundError:
                res.append({'id': data_id, 'status': self.doc_cls(
                    meta={'id': data_id}, **data).save()})
            else:
                raise falcon.HTTPConflict(
                    title=f'{self.doc_name} already found', description=f'id={data_id} already present')
        resp.code = res_code
        resp.media = res

    def on_delete(self, req, resp, id=None):
        try:
            resp.media = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {})).delete(id=id).to_dict()  # TODO check delete
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error, description=req_error.info

    def on_put(self, req, resp, id=None):
        res=[]
        for data in wrap(req.context.get('json', [])):
            data_id=data.pop('id') or id
            if data_id is None:
                raise falcon.HTTPBadRequest(
                    title='Request not valid', description='id property not found')
            try:
                res.append(
                    {'id': data_id, 'status': self.doc_cls.get(id=data_id).update(**data)})
            except elasticsearch.NotFoundError:
                raise falcon.HTTPNotFound(title=f'{self.doc_name} not found',
                                        description=f'{self.doc_name} with id = {data_id} not found')
        resp.media=res
