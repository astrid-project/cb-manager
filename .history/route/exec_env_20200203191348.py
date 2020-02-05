import falcon
from schema import Query
from marshmallow import fields, Schema
import elasticsearch
from elasticsearch_dsl import Document, InnerDoc, Nested, Text, Search


class ExecEnvDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env'

ExecEnvDocument.init()

class ExecEnvResource(object, ):
    def on_get(self, req, resp):
        query = req.context['json']
        try:
            s = Search(index=ExecEnvDocument.Index.name)
            if 'select' in query:
                s = .source(list(map(self.resolve_property, data)))
            res = self.s.execute()
            resp.media = [dict(item.to_dict(), id=item.meta.id) for item in res]
        except elasticsearch.RequestError as e:
            pass

    def on_post(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass
