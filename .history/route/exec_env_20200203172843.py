import falcon
from marshmallow import fields, Schema



class ExecEnvResponseSchema(Schema):
    pass


class ExecEnvResponseSchema(Schema):
    pass


class ExecEnvResource(object):
    request_schema = ExecEnvRequestSchema()
    response_schema = ExecEnvResponseSchema()