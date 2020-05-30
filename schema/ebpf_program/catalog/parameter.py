from marshmallow import Schema
from marshmallow.fields import Boolean, List, Nested, String


class eBPFProgramParameterCatalogSchema(Schema):
    """
    eBPF program configuration.
    """
    id = String(required=True,
                description='Parameter id',
                example='log-period')
    type = String(required=True,
                  enum=['integer', 'number', 'time-duration',
                        'string', 'choice', 'boolean', 'binary'],
                  description='Parameter type.', example='integer')
    list = Boolean(description='Indicate if the parameter can have multiple values.',
                   example=True)
    values = List(String(example=['mysql', 'http']),
                  description='Possible values if the parameter type is choice.')
    example = String()
    description = String()
