from document.ebpf_program.catalog import eBPFProgramCatalogDocument
from marshmallow import Schema, validate
from marshmallow.fields import Bool, Nested, Raw, Str
from schema.base import BaseSchema
from schema.validate import msg_id_unique, unique_list


parameter_types = ['integer', 'number', 'time-duration',
                   'string', 'choice', 'boolean', 'binary']


class eBPFProgramCatalogOpenMetricsMetadataLabelSchema(Schema):
    """eBPF program Open Metrics metadata label."""

    name = Str(required=True, example='IP_PROTO',
               description='Label name.')
    value = Str(required=True, example='UDP',
                description='Label value.')


class eBPFProgramCatalogOpenMetricsMetadataSchema(Schema):
    """eBPF program Open Metrics metadata."""

    type = Str(required=True, example='counter',
               description='Metric type.')
    help = Str(example='This metric represents the number of packets that has travelled trough this probe.',
               description='Metric help.')
    labels = Nested(eBPFProgramCatalogOpenMetricsMetadataLabelSchema, many=True, unknown='INCLUDE',
                    description='Labels of Open Metrics Metadata.',
                    validate=unique_list('name'),
                    error_messages=dict(validator_failed=msg_id_unique))


class eBPFProgramCatalogMetricSchema(Schema):
    """eBPF program metric."""

    name = Str(required=True, example='packets_total',
               description='Metric name.')
    map_name = Str(data_key='map-name', required=True, example='PKT_COUNTER',
                   description='Mapping value in the code.')
    open_metrics_metadata = Nested(eBPFProgramCatalogOpenMetricsMetadataSchema,
                                   data_key='open-metrics-metadata', unknown='INCLUDE',
                                   description='Open Metrics Metadata.')


class eBPFProgramConfigCatalogSchema(Schema):
    """eBPF program configuration."""

    code = Str(required=True,
               description='Code of the eBPF program.')
    metrics = Nested(eBPFProgramCatalogMetricSchema, many=True, unknown='INCLUDE',
                     description='eBPF program metrics.',
                     validate=unique_list('name'),
                     error_messages=dict(validator_failed=msg_id_unique))


class eBPFProgramParameterCatalogSchema(Schema):
    """eBPF program configuration."""

    id = Str(required=True, example='interface',
             description='Parameter id.')
    type = Str(required=True, description='Parameter type.', enum=parameter_types, example='integer',
               validate=validate.OneOf(parameter_types))
    list = Bool(default=False, example=True,
                description='Indicate if the parameter can have multiple values.')
    values = Str(many=True, example='yes',
                 description='Possible values if the parameter type is choice.')
    description = Str(example='Network Interface to attach.',
                      description='Short description of the parameter.')
    example = Raw(example='eno0',
                  description='Example of parameter value.')


class eBPFProgramCatalogSchema(BaseSchema):
    """Represents an eBPF program in the catalog."""

    doc_cls = eBPFProgramCatalogDocument

    id = Str(required=True, example='packet-capture',
             description='Id of the eBPFProgram in the catalog.')
    config = Nested(eBPFProgramConfigCatalogSchema, required=True, unknown='INCLUDE')
    parameters = Nested(eBPFProgramParameterCatalogSchema, many=True, unknown='INCLUDE',
                        validate=unique_list('id'),
                        error_messages=dict(validator_failed=msg_id_unique))
    description = Str(example="""Transparent service to capture packets flowing through the interface it
                                 is attached to, apply filters and obtain capture in .pcap format.""",
                      description='Description of eBPF program.')
