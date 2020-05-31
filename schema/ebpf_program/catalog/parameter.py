from marshmallow import Schema
from marshmallow.fields import Boolean, List, Nested, String


class eBPFProgramParameterCatalogSchema(Schema):
    """
    eBPF program configuration.
    """

    id = String(required=True, dump_only=True, description='Parameter id.', example='interface')

    type = String(required=True,
                  enum=['integer', 'number', 'time-duration', 'string', 'choice', 'boolean', 'binary'],
                  description='Parameter type.', example='integer')

    list = Boolean(default=False, description='Indicate if the parameter can have multiple values.',
                   example=True)

    values = List(String(example=['yes', 'no']),
                  description='Possible values if the parameter type is choice.')

    example = String(description='Example of parameter value.', example='eno0')

    description = String(description='Short description of the parameter.',
                         example='Network Interface to attach.')
