from marshmallow import fields, Schema


class ExecEnvSchema(Schema):
    """
    Represents an execution environment.
    """
    id = fields.String(required=True, description='ID of the execution environment.', example='exec-env-type')
    hostname = fields.String(required=True, description='Hostname of the execution environment.', example='192.168.1.2')
    type_id = fields.String(required=True, description='ID of the execution environment type.', example='vm')
