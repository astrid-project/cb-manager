from marshmallow import Schema
from marshmallow.fields import  Nested, String


class AgentCatalogActionConfigSchema(Schema):
    """
    Agent action configuration.
    """

    cmd = String(many=True, description='Action command.', example='service filebeat start')


class AgentCatalogActionSchema(Schema):
    """
    Agent action.
    """

    id = String(required=True, dump_only=True, enum=['start', 'stop', 'restart'], description='Action name',
                example='start')

    config = Nested(AgentCatalogActionConfigSchema, required=True, many=True, description='Action config.')
