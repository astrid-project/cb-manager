from document.agent.catalog import AgentCatalogDocument
from marshmallow import Schema, validate
from marshmallow.fields import Bool, List, Nested, Raw, Str
from schema.base import BaseSchema, NestedSchema
from schema.validate import msg_id_unique, unique_list


action_status = ['started', 'stopped', 'unknown']
parameter_schemas = ['yaml', 'json', 'properties']
parameter_types = ['integer', 'number', 'time-duration',
                   'string', 'choice', 'boolean', 'binary']


class AgentCatalogActionConfigSchema(Schema):
    """Agent action configuration."""

    cmd = Str(required=True, example='service filebeat start',
              description='Action command.')
    args = Str(many=True, example='-v',
               description='Action command argument')
    daemon = Str(example='firewall',
                 description='Key used to execute the command as daemon.')


class AgentCatalogActionSchema(Schema):
    """Agent action."""

    id = Str(required=True, example='start',
             description='Action name')
    config = Nested(AgentCatalogActionConfigSchema, unknown='INCLUDE', required=True,
                    description='Action config.') # TODO unique?
    status = Str(enum=action_status, example=action_status[0],
                 description='Update the status the of the agent-instance if the command is executed correctly.',
                 validate=validate.OneOf(action_status))
    description = Str(example='Start the execution of the agent.',
                      description='Short descripton of the agent actions.')
    example = Raw(example='forward',
                  description='Example of action parameter.')


class AgentCatalogParameterConfigSchema(Schema):
    """Agent parameter configuration."""

    schema = Str(required=True, enum=parameter_schemas, example=parameter_schemas[0],
                 description='Schema of the parameter file',
                 validate=validate.OneOf(parameter_schemas))
    source = Str(required=True, example='/usr/share/filebeat/filebeat.yml',
                 description='Path of the source parameter file')
    path = List(Str(required=True, example='enabled',
               description='Path of the parameter value in the file'))


class AgentCatalogParameterSchema(Schema):
    """Agent parameter."""

    id = Str(required=True, example='log-period',
             description='Parameter id.')
    type = Str(required=True, enum=parameter_types, example=parameter_types[0],
               description='Parameter type.',
               validate=validate.OneOf(parameter_types))
    config = Nested(AgentCatalogParameterConfigSchema, unknown='INCLUDE', required=True,
                    description='Parameter configuration.')
    list = Bool(default=False, example=True,
                description='Indicate if the parameter can have multiple values.')
    values = Str(many=True, example='mysql',
                 description='Possible values if the parameter type is choice.')
    description = Str(example='Enable the agent.',
                      description='Short description of the parameter.')
    example = Raw(example='10s',
                  description='Example of parameter value.')


class AgentCatalogResourceConfigSchema(Schema):
    """Agent resource configuration."""

    path = Str(required=True, example='/usr/share/filebeat/filebeat.yml',
               description='File path')


class AgentCatalogResourceSchema(NestedSchema):
    """Agent resource."""

    id = Str(required=True, example='filebeat-config',
             description='Resource id.')
    config = Nested(AgentCatalogResourceConfigSchema, unknown='INCLUDE', required=True,
                    description='Resource configuration.')
    description = Str(example='Enable the agent.',
                      description='Short description of the parameter.', )
    example = Raw(example='10s',
                  description='Example of parameter value.')


class AgentCatalogSchema(BaseSchema):
    """Represents an agent in the catalog."""
    doc_cls = AgentCatalogDocument

    id = Str(required=True, example='filebeat',
             description='Id of the agent in the catalog.')
    actions = Nested(AgentCatalogActionSchema, many=True, unknown='INCLUDE',
                     description='Action properties.',
                     validate=unique_list('id'),
                     error_messages=dict(validator_failed=msg_id_unique))
    parameters = Nested(AgentCatalogParameterSchema, many=True, unknown='INCLUDE',
                        description='Parameter properties.',
                        validate=unique_list('id'),
                        error_messages=dict(validator_failed=msg_id_unique))
    resources = Nested(AgentCatalogResourceSchema, many=True, unknown='INCLUDE',
                       description='Resource properties.',
                       validate=unique_list('id'),
                       error_messages=dict(validator_failed=msg_id_unique))
    description = Str(example='Collect system metrics from execution environments.',
                      description='Short description of the agent.')
