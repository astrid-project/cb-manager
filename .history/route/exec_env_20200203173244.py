import falcon
from marshmallow import fields, Schema
import elasticsearch
from elasticsearch_dsl import Document as DocumentElastic, InnerDoc as InnerDocElastic, Nested


class ExecEnvRequestSchema(Schema):
    pass


class ExecEnvResponseSchema(Schema):
    pass


class ExecEnvResource(object, DocumentElastic):
    request_schema = ExecEnvRequestSchema()
    response_schema = ExecEnvResponseSchema()

    class Index:
        name = 'exec-env'

    def on_get(self, req, resp):

    def on_post(self, req, resp):

    def on_delete(self, req, resp):

    def on_put(self, req, resp):
