import falcon
from marshmallow import fields, Schema

class ExecEnvRequestSchema(Schema):
    pass


class ExecEnvResponseSchema(Schema):
    pass


class ExecEnvResource(object):
    request_schema = ExecEnvRequestSchema()
    response_schema = ExecEnvResponseSchema()

    def on_get(self, req, resp):

    def on_post(self, req, resp):

    def on_delete(self, req, resp, id):

    def on_put(self, req, resp):
