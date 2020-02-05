import falcon
from marshmallow import fields, Schema

class ExecEnvRequestSchema(Schema):
    pass


class ExecEnvResponseSchema(Schema):
    pass


class ExecEnvResource(object):
    request_schema = ExecEnvRequestSchema()
    response_schema = ExecEnvResponseSchema()