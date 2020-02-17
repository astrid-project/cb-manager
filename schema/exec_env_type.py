from marshmallow import fields, Schema


class ExecEnvTypeSchema(Schema):
    """
    Represents an execution environment type.
    """
    id = fields.String(required=True, description='ID of the execution environment type.', example='vm')
    name = fields.String(required=True, description='Name of the execution environment.', example='Virtual Machine')
