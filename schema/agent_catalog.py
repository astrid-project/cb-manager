from .recipe import RecipeSchema
from marshmallow import fields, Schema


class AgentCatalogParameterSchema(Schema):
    """
    Agent parameter.
    """
    name = fields.String(required=True, description='Parameter name',
                         example='period')
    type = fields.String(required=True,
                         enum=['integer', 'number', 'time-duration',
                               'string', 'choice', 'boolean', 'binary'],
                         description='Parameter type.', example='integer')
    list = fields.Boolean(description='Indicate if the parameter can have multiple values.',
                          example=True)
    values = fields.List(fields.String(example=['mysql', 'http']),
                         description='Possible values if the parameter type is choice.')
    recipe = fields.Nested(RecipeSchema, required=True,
                           many=True, description='Parameter recipe')


class AgentCatalogActionSchema(Schema):
    """
    Agent action.
    """
    name = fields.String(required=True, enum=['start', 'stop', 'install', 'uninstall'],
                         description='Action name', example='start')
    recipe = fields.Nested(RecipeSchema, required=True,
                           many=True, description='Action recipe')


class AgentCatalogSchema(Schema):
    """
    Represents an agent in the catalog.
    """
    id = fields.String(required=True, description='ID of the agent in the catalog.',
                       example='uyPMaXABjPI5oepgjezR')
    name = fields.String(required=True, description='Agent name.',
                         example='filebeat')
    parameters = fields.Nested(AgentCatalogParameterSchema, required=True, many=True,
                               description='Parameter properties')
    actions = fields.Nested(AgentCatalogActionSchema, required=True, many=True,
                            description='Action properties')
