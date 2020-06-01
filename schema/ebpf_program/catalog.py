from marshmallow import Schema
from marshmallow.fields import Bool, List, Nested, Str


class eBPFProgramCatalogOpenMetricsMetadataLabelSchema(Schema):
    """eBPF program Open Metrics metadata label."""
    name = Str(required=True, description='Label name.', example='IP_PROTO')
    value = Str(required=True, description='Label value.', example='UDP')


class eBPFProgramCatalogOpenMetricsMetadataSchema(Schema):
    """eBPF program Open Metrics metadata."""
    type = Str(required=True, description='Metric type.', example='counter')
    help = Str(description='Metric help.',
               example='This metric represents the number of packets that has traveled trough this probe.')
    labels = Nested(eBPFProgramCatalogOpenMetricsMetadataLabelSchema,
                    description='Labels of Open Metrics Metadata.')


class eBPFProgramCatalogMetricSchema(Schema):
    """eBPF program metric."""
    name = Str(required=True, description='Metric name.',
               example='packets_total')
    map_name = Str(data_key='map-name', required=True, description='Mapping value in the code.',
                   example='PKT_COUNTER')
    open_metrics_metadata = Nested(eBPFProgramCatalogOpenMetricsMetadataSchema,
                                   data_key='open-metrics-metadata', description='Open Metrics Metadata.')


class eBPFProgramConfigCatalogSchema(Schema):
    """eBPF program configuration."""
    code = Str(required=True, description='Code the eBPF program.')
    metrics = Nested(eBPFProgramCatalogMetricSchema, many=True,
                     description='eBPF program metrics.')


class eBPFProgramParameterCatalogSchema(Schema):
    """eBPF program configuration."""
    id = Str(required=True, dump_only=True,
             description='Parameter id.', example='interface')
    description = Str(description='Short description of the parameter.',
                      example='Network Interface to attach.')
    type = Str(required=True, description='Parameter type.', example='integer',
               enum=['integer', 'number', 'time-duration', 'string', 'choice', 'boolean', 'binary'])
    list = Bool(default=False, description='Indicate if the parameter can have multiple values.',
                example=True)
    values = List(Str(example=['yes', 'no']),
                  description='Possible values if the parameter type is choice.')
    example = Str(description='Example of parameter value.', example='eno0')


class eBPFProgramCatalogSchema(Schema):
    """Represents an eBPF program in the catalog."""
    id = Str(required=True, dump_only=True, description='Id of the eBPF program in the catalog.',
             example='packet-capture')
    description = Str(description='Description of eBPF program.',
                      example='Transparent service to capture packets flowing through the interface it is attached to, apply filters and obtain capture in .pcap format.')
    config = Nested(eBPFProgramConfigCatalogSchema, required=True, many=False)
    parameters = Nested(eBPFProgramParameterCatalogSchema, many=True)
