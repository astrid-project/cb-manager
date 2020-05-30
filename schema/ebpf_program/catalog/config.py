from marshmallow import Schema
from marshmallow.fields import List, Nested, String


class eBPFProgramCatalogMetricSchema(Schema):
    """
    eBPF program metric.
    """

    id = String(required=True,
                description='Metric name',
                example='packets_total')

    map_name = String(required=True, description='Mapping value in the code', example='PKT_COUNTER')

    type = String(required=True, description='Metric type', example='counter')

    help = String(description='Metric help',
                  example='This metric represents the number of packets that has traveled trough this probe.')

    labels = List(String(description='Metric label'))


class eBPFProgramConfigCatalogSchema(Schema):
    """
    eBPF program configuration.
    """
    code = String(required=True, description='Code the eBPF program')

    metrics = Nested(eBPFProgramCatalogMetricSchema,
                     required=True, many=True,
                     description='eBPF program metrics.')
