import falcon
from query_parser import QueryParser
from schema import Query
from marshmallow import fields, Schema
import elasticsearch
from elasticsearch_dsl import Document, InnerDoc, Nested, Text


class ExecEnvDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env'

ExecEnvDocument.init()

class ExecEnvResource(object, ):
    def on_get(self, req, resp):
        res = QueryParser(index=ExecEnvDocument.Index.name).parse(query=req.context['json']).execute()
        resp.media = [dict(item.to_dict(), id=item.meta.id) for item in res]

    def on_post(self, req, resp):
        data = req.context['json']
        id = data.pop('id', None)
        if id is None:
            pass # TODO error id not found
        try:
            ExecEnvDocument.get(id=id)
        except elasticsearch.NotFoundError:
            resp.media = ExecEnvDocument(meta={'id': id}, **data).save().to_dict()
        else:
            pass # TODO error id already found

    def on_delete(self, req, resp):
        query = req.context['json']
        resp.media = QueryParser(index=ExecEnvDocument.Index.name).parse(query=query).delete().to_dict()

    def on_put(self, req, resp):
        data = req.context['json']
        id = data.pop('id', None)
        if id is None:
            pass # TODO error id not found
        try:
            resp.media = ExecEnvDocument.get(id=id).update(**data).to_dict()
        except elasticsearch.NotFoundError:
            raise falcon.HTTPNotFound()

