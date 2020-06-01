from marshmallow import Schema
from marshmallow.fields import Nested, String
from schema.agent.catalog.parameter import AgentCatalogParameterSchema
from schema.agent.catalog.action import AgentCatalogActionSchema


class AgentCatalogSchema(Schema):
    """
    Represents an agent in the catalog.
    """

    id = String(required=True, dump_only=True, description='ID of the agent in the catalog.',
                example='filebeat')

    description = String(description='Short description of the agent.',
                         example='Collect system metrics from execution environments.')

    parameters = Nested(AgentCatalogParameterSchema,
                        required=True, many=True, description='Parameter properties.')

    actions = Nested(AgentCatalogActionSchema, required=True, many=True, description='Action properties.')
