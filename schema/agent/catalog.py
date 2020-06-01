from marshmallow import Schema
from marshmallow.fields import Bool, Nested, Str


class AgentCatalogParameterConfigSchema(Schema):
    """Agent parameter configuration."""
    # FIXME description?
    schema = Str(required=True, enum=['yaml', 'json', 'properties'],
                 description='Schema of the parameter file', example='yaml')
    source = Str(required=True, description='Path of the source parameter file',
                 example='/usr/share/filebeat/filebeat.yml')
    path = Str(required=True, many=True, description='Path of the parameter value in the file',
               example='enabled')


class AgentCatalogParameterSchema(Schema):
    """Agent parameter."""
    id = Str(required=True, dump_only=True,
             description='Parameter id.', example='log-period')
    description = Str(example='Enable the agent.',
                      description='Short description of the parameter.', )
    type = Str(required=True, description='Parameter type.', example='integer',
               enum=['integer', 'number', 'time-duration', 'string', 'choice', 'boolean', 'binary'])
    list = Bool(default=False, description='Indicate if the parameter can have multiple values.',
                example=True)
    values = Str(example='mysql',
                 description='Possible values if the parameter type is choice.')
    example = Str(description='Example of parameter value.', example='10s')
    config = Nested(AgentCatalogParameterConfigSchema, required=True,
                    description='Parameter configuration.')


class AgentCatalogActionConfigSchema(Schema):
    """Agent action configuration."""
    description = Str(description='Short description of the agent action command',
                      example='Set the working directory.')
    cmd = Str(many=True, description='Action command.',
              example='service filebeat start')


class AgentCatalogActionSchema(Schema):
    """Agent action."""
    id = Str(required=True, dump_only=True, enum=['start', 'stop', 'restart'], description='Action name',
             example='start')
    description = Str(description='Short descripton of the agent actions.',
                      example='Start the execution.')
    config = Nested(AgentCatalogActionConfigSchema, required=True,
                    many=True, description='Action config.')


class AgentCatalogSchema(Schema):
    """Represents an agent in the catalog."""
    id = Str(required=True, dump_only=True, example='filebeat',
             description='Id of the agent in the catalog.')
    description = Str(description='Short description of the agent.',
                      example='Collect system metrics from execution environments.')
    parameters = Nested(AgentCatalogParameterSchema, required=True, many=True,
                        description='Parameter properties.')
    actions = Nested(AgentCatalogActionSchema, required=True,
                     many=True, description='Action properties.')
