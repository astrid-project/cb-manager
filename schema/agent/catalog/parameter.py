from marshmallow import Schema
from marshmallow.fields import Boolean, Nested, String


class AgentCatalogParameterConfigSchema(Schema):
    """
    Agent parameter configuration.
    """

    schema = String(required=True, enum=['yaml', 'json', 'properties'],
                    description='Schema of the parameter file', example='yaml')

    source = String(required=True, description='Path of the source parameter file',
                    example='/usr/share/filebeat/filebeat.yml')

    path = String(required=True, many=True, description='Path of the parameter value in the file',
                  example='enabled')


class AgentCatalogParameterSchema(Schema):
    """
    Agent parameter.
    """

    id = String(required=True, dump_only=True, description='Parameter id.', example='log-period')

    type = String(required=True, description='Parameter type.', example='integer',
                  enum=['integer', 'number', 'time-duration', 'string', 'choice', 'boolean', 'binary'])

    list = Boolean(default=False, description='Indicate if the parameter can have multiple values.',
                   example=True)

    values = String(description='Possible values if the parameter type is choice.', example='mysql')

    example = String(description='Example of parameter value.', example='10s')

    description = String(description='Short description of the parameter.', example='Enable the agent.')

    config = Nested(AgentCatalogParameterConfigSchema,
                    required=True, many=True, description='Parameter configuration.')
