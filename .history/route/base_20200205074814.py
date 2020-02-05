import falcon
from query_parser import QueryParser
import elasticsearch
from utils import wrap


class BaseResource(object):
    path = '/'

    def on_get(self, req, resp, id=None):
        try:
            res = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {})).execute()
            resp.media = [dict(item.to_dict(), id=item.meta.id)
                               for item in res if (id is not None and item.meta.id == id) or id is None]
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error, description=req_error.info)

    def on_post(self, req, resp, id=None):
        res = []
        for data in wrap(req.context.get('json', [])):
            data_id = data.pop('id') or id
            if data_id is None:
                raise falcon.HTTPBadRequest(
                    title='Request not valid', description='id property not found')
            try:
                self.doc_cls.get(id=data_id)
            except elasticsearch.NotFoundError:
                res.append({'id': data_id, 'status': self.doc_cls(
                    meta={'id': data_id}, **data).save()})
            else:
                raise falcon.HTTPConflict(
                    title=f'{self.doc_name} already found', description=f'id={data_id} already present')
        resp.media = res

    def on_delete(self, req, resp, id=None):
        try:
            resp.media = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {})).delete().to_dict()
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(
                title=req_error.error(), description=req_error.info())

    def on_put(self, req, resp, id=None):
        res = []
        for data in wrap(req.context.get('json', [])):
            data_id = data.pop('id')
            if id is None:
                raise falcon.HTTPBadRequest(
                    title='Request not valid', description='id property not found')
            try:
                res.append(
                    {'id': id, 'status': self.doc_cls.get(id=id).update(**data)})
            except elasticsearch.NotFoundError:
                raise falcon.HTTPNotFound(title=f'{self.doc_name} not found',
                                        description=f'{self.doc_name} with id = {id} not found')
        resp.media = res
