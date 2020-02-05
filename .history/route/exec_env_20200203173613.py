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
    self.s = Search(index=self.Index.name)

    class Index:
        name = 'exec-env'


class ExecEnvResource(object, ):
    request_schema = ExecEnvRequestSchema()
    response_schema = ExecEnvResponseSchema()

    def on_get(self, req, resp):

    def on_post(self, req, resp):

    def on_delete(self, req, resp):

    def on_put(self, req, resp):
