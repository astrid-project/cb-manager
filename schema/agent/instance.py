from document.agent.catalog import AgentCatalogDocument
from document.agent.instance import AgentInstanceDocument
from document.exec_env import ExecEnvDocument
from marshmallow import Schema, validate, validates_schema
from marshmallow.fields import Nested, Nested, Str
from schema.agent.catalog import AgentCatalogSchema
from schema.base import BaseSchema
from schema.exec_env import ExecEnvSchema
from schema.validate import _in, _not_in, msg_id_not_found, msg_id_not_in_catalog, msg_id_unique, unique_list


agent_status = ['started', 'stopped', 'unknown']


class AgentInstanceParameterSchema(Schema):
    """Parameter of the agent instance installed in an execution environment."""

    id = Str(required=True, example='period',
             description='Parameter id.')
    value = Str(required=True, example='10s',
                description='Paremeter value.')


class AgentInstanceSchema(BaseSchema):
    """Represents an agent instance installed in an execution environment."""
    doc_cls = AgentInstanceDocument

    id = Str(required=True, example='filebeat@apache',
             description='Id of the agent instance installed in an execution environment.')
    agent_catalog_id = Str(required=True, readonly=True, example='filebeat',
                           description='Id of the agent in the catalog.',
                           validate=_in(AgentCatalogDocument.get_ids),
                           error_messages=dict(validator_failed=msg_id_not_in_catalog))
    exec_env_id = Str(required=True, readonly=True, example='apache',
                      description='Id of the execution environment where the agent instance is installed.',
                      validate=_in(ExecEnvDocument.get_ids),
                      error_messages=dict(validator_failed=msg_id_not_found))
    status = Str(required=True, readonly=True, enum=agent_status, example=agent_status[0],
                 description='Status of the agent instance',
                 validate=validate.OneOf(agent_status))
    parameters = Nested(AgentInstanceParameterSchema, many=True,
                        description='List of agent instance parameters.',
                        validate=unique_list('id'),
                        error_messages=dict(validator_failed=msg_id_unique))
    description = Str(example='Collect system metrics from execution environments.',
                      description='Short description of the agent installed in the execution environment.')
