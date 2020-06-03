from marshmallow import Schema
from marshmallow.fields import Nested, Nested, Str
from schema.agent.catalog import AgentCatalogSchema
from schema.exec_env import ExecEnvSchema


class AgentInstanceParameterSchema(Schema):
    """Parameter of the agent instance installed in an execution environment."""
    id = Str(required=True, dump_only=True,
             description='Parameter id.', example='period')
    value = Str(required=True, description='Paremeter value.', example='10s')


class AgentInstanceSchema(Schema):
    """Represents an agent instance installed in an execution environment."""
    id = Str(required=True, dump_only=True, example='filebeat@apache',
             description='Id of the agent instance installed in an execution environment.')
    description = Str(description='Short description of the agent installed in the execution environment.',
                      example='Collect system metrics from execution environments.')
    agent_catalog_id = Str(required=True, example='filebeat',
                           description='Id of the agent in the catalog.')
    exec_env_id = Str(required=True, example='apache',
                      description='Id of the execution environment where the agent instance is installed.')
    status = Str(required=True, example='started', description='Status of the agent instance',
                 enum=['started', 'stopped', 'unknown'])
    parameters = Nested(AgentInstanceParameterSchema, many=True,
                        description='List of agent instance parameters.')
