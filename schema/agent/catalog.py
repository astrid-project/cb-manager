from marshmallow import Schema
from marshmallow.fields import Bool, Nested, Str


class AgentCatalogParameterConfigSchema(Schema):
    """Agent parameter configuration."""
    schema = Str(required=True, enum=['yaml', 'json', 'properties'],
                 description='Schema of the parameter file', example='yaml')
    source = Str(required=True, description='Path of the source parameter file',
                 example='/usr/share/filebeat/filebeat.yml')
    path = Str(required=True, many=True, description='Path of the parameter value in the file',
               example='enabled')


class AgentCatalogParameterSchema(Schema):
    """Agent parameter."""
    id = Str(required=True, dump_only=True, readonly=True,
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
    cmd = Str(required=True, description='Action command.', example='service filebeat start')
    args = Str(many=True, description='Action command argument', example='-v')
    daemon = Str(description='Key used to execute the command as daemon.', example='firewall')


class AgentCatalogActionSchema(Schema):
    """Agent action."""
    id = Str(required=True, dump_only=True, enum=['start', 'stop', 'restart'], description='Action name',
             example='start', readonly=True)
    description = Str(description='Short descripton of the agent actions.',
                      example='Start the execution.')
    status = Str(enum=['started', 'stopped', 'unknown'], example='started', default=None,
                 description='Update the status the of the agent-instance if the command is executed correctly.')
    config = Nested(AgentCatalogActionConfigSchema, required=True,
                    many=True, description='Action config.')


class AgentCatalogSchema(Schema):
    """Represents an agent in the catalog."""
    id = Str(required=True, dump_only=True, example='filebeat', readonly=True,
             description='Id of the agent in the catalog.')
    description = Str(description='Short description of the agent.',
                      example='Collect system metrics from execution environments.')
    parameters = Nested(AgentCatalogParameterSchema, many=True,
                        description='Parameter properties.')
    actions = Nested(AgentCatalogActionSchema, many=True, description='Action properties.')
