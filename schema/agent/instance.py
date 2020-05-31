from marshmallow import Schema
from marshmallow.fields import Nested, Pluck, String
from schema.agent.catalog import AgentCatalogSchema
from schema.exec_env import ExecEnvSchema


class AgentInstanceParameterSchema(Schema):
    """
    Parameter of the agent instance installed in an execution environment.
    """

    id = String(required=True, dump_only=True, description='Parameter id.', example='period')

    value = String(required=True, description='Paremeter value.', example='10s')


class AgentInstanceSchema(Schema):
    """
    Represents an agent instance installed in an execution environment.
    """

    id = String(required=True, dump_only=True,
                description='Id of the agent instance installed in an execution environment.',
                example='filebeat@apache')

    agent_catalog_id = Pluck(AgentCatalogSchema, 'id', required=True,
                             description='Id of the agent in the catalog.', example='filebeat')

    exec_env_id = Pluck(ExecEnvSchema, 'id', required=True,
                         description='Id of the execution environment where the agent instance is installed.',
                         example='apache')

    status = String(required=True, enum=['start', 'stop', 'restart'],
                    description='Status of the agent instance', example='start')

    parameters = Nested(AgentInstanceParameterSchema,
                        many=True, description='List of agent instance parameters.')
