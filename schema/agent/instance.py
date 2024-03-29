from marshmallow import Schema
from marshmallow.fields import Nested, Raw, Str

from document.agent.catalog import Agent_Catalog_Document
from document.agent.instance import Agent_Instance_Document
from document.exec_env import Exec_Env_Document
from schema.agent.catalog import AGENT_STATUS
from schema.base import Base_Schema
from schema.validate import In, Unique_List

OUTPUT_FORMATS = ['plain', 'lines', 'json']


class Agent_Instance_Action_Schema(Schema):
    """Action of the agent instance installed in an execution environment."""

    id = Str(required=True, example='list', description='Action id.')
    output_format = Str(enum=OUTPUT_FORMATS, example=OUTPUT_FORMATS[1], default=OUTPUT_FORMATS[0],
                        description='Output format for stdout and stderr result of action execution.')


class Agent_Instance_Parameter_Schema(Schema):
    """Parameter of the agent instance installed in an execution environment."""

    id = Str(required=True, example='period', description='Parameter id.')
    value = Raw(required=True, example='10s', description='Paremeter value.'),


class Agent_Instance_Resource_Schema(Schema):
    """Resource of the agent instance installed in an execution environment."""

    id = Str(required=True, example='filebeat-config', description='Resource id.')
    content = Str(required=True, example='period: 10s', description='Resource content.')


class Agent_Instance_Operation_Schema(Base_Schema):
    """Represents the operations to perform with the agent instance installed in an execution environment."""

    actions = Nested(Agent_Instance_Action_Schema, many=True, unknown='INCLUDE',
                     description='List of agent instance actions.')
    parameters = Nested(Agent_Instance_Parameter_Schema, many=True, unknown='INCLUDE',
                        description='List of agent instance parameters.',
                        validate=Unique_List.apply('id'), error_messages=Unique_List.error_messages)
    resources = Nested(Agent_Instance_Resource_Schema, many=True, unknown='INCLUDE',
                       description='List of agent instance resources.',
                       validate=Unique_List.apply('id'), error_messages=Unique_List.error_messages)


class Agent_Instance_Schema(Base_Schema):
    """Represents an agent instance installed in an execution environment."""

    doc = Agent_Instance_Document
    id = Str(required=True, example='filebeat@apache',
             description='Id of the agent instance installed in an execution environment.')
    agent_catalog_id = Str(required=True, readonly=True, example='filebeat', description='Id of the agent in the catalog.',
                           validate=In.apply(Agent_Catalog_Document.get_ids), error_messages=In.error_messages)
    exec_env_id = Str(required=True, readonly=True, example='apache',
                      description='Id of the execution environment where the agent instance is installed.',
                      validate=In.apply(Exec_Env_Document.get_ids), error_messages=In.error_messages)
    status = Str(enum=AGENT_STATUS, required=True, readonly=True, example=AGENT_STATUS[0],
                 description='Status of the agent.')
    operations = Nested(Agent_Instance_Operation_Schema, many=True, unknown='INCLUDE',
                        description='List of agent instance operations.')
    description = Str(example='Collect system metrics from execution environments.',
                      description='Short description of the agent installed in the execution environment.')
