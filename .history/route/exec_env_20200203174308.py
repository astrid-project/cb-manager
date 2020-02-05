import falcon
from marshmallow import fields, Schema
import elasticsearch
from elasticsearch_dsl import Document, InnerDoc, Nested, Text


class ExecEnvRequestSchema(Schema):
    pass


class ExecEnvResponseSchema(Schema):
    pass


class ExecEnvDocument(Document):
    hostname = Text()
    type_id = Text()

    def __init__(self):

    class Index:
        name = 'exec-env'

ExecEnvDocument.init()

class ExecEnvResource(object, ):
    request_schema = ExecEnvRequestSchema()
    response_schema = ExecEnvResponseSchema()

    def on_get(self, req, resp):
        self.s = Search(index=ExecEnvDocument.Index.name)
        res = self.s.execute()
        print(res)

    def on_post(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass
