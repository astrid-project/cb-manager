import falcon
from query_parser import QueryParser
import elasticsearch


def wrap(data):
    return data if data is list else [data]


class BaseResource(object):
    path = '/'

    def on_get(self, req, resp):
        try:
            res = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {})).execute()
            resp.media = [dict(item.to_dict(), id=item.meta.id) for item in res]
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(title=req_error.error, description=req_error.info)

    def on_post(self, req, resp):
        for data in wrap(req.context.get('json', [])):
            id = data.pop('id', None)
            if id is None:
                raise falcon.HTTPBadRequest(title='Request not valid', description='id property not found')
            try:
                self.doc_cls.get(id=id)
            except elasticsearch.NotFoundError:
                resp.media = self.doc_cls(
                    meta={'id': id}, **data).save()
            else:
                raise falcon.HTTPConflict(title=f'{self.doc_name} already found', description=f'id={id} already present')

    def on_delete(self, req, resp):
        try:
            resp.media = QueryParser(index=self.doc_cls.Index.name).parse(
                query=req.context.get('json', {})).delete().to_dict()
        except elasticsearch.RequestError as req_error:
            raise falcon.HTTPBadRequest(title=req_error.error(), description=req_error.info())

    def on_put(self, req, resp):
        for data in wrap(req.context.get('json', [])):
            id = data.pop('id', None)
            if id is None:
                raise falcon.HTTPBadRequest(title='Request not valid', description='id property not found')
            try:
                resp.media = self.doc_cls.get(id=id).update(**data).to_dict()
            except elasticsearch.NotFoundError:
                raise falcon.HTTPNotFound(title=f'{self.doc_name} not found',
                                        description=f'{self.doc_name} with id = {id} not found')
