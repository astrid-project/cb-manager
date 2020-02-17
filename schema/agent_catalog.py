from marshmallow import fields, Schema


class AgentParameterSchema(Schema):
    """
    Agent parameter.
    """
    name = fields.String(required=True, description='Parameter name.', example='period')
    type = fields.String(required=True, enum=['integer', 'number', 'time-duration', 'string', 'choice', 'boolean', 'binary'],
                         description='Parameter type.', example='integer')
    list = fields.Boolean(required=True, description='Indicate if the parameter can have multiple values.', example=True)
    values = fields.List(fields.String(required=True, example=['mysql', 'http']),
                          description='Possible values if the parameter type is choice.')


class AgentCatalogSchema(Schema):
    """
    Represents an agent in the catalog.
    """
    id = fields.String(required=True, description='ID of the agent in the catalog.', example='agent-filebeat-1')
    name = fields.String(required=True, description='Agent name.', example='filebeat')
    parameters = fields.List(fields.Nested(AgentParameterSchema), required=True,
                             description='List of agent parameters')
