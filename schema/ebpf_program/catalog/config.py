from marshmallow import Schema
from marshmallow.fields import Nested, String
from schema.ebpf_program.catalog.open_metrics_metadata import eBPFProgramCatalogOpenMetricsMetadataSchema


class eBPFProgramCatalogMetricSchema(Schema):
    """
    eBPF program metric.
    """
    name = String(required=True, description='Metric name.', example='packets_total')
    map_name = String(data_key='map-name', required=True,
                      description='Mapping value in the code.', example='PKT_COUNTER')
    open_metrics_metadata = Nested(eBPFProgramCatalogOpenMetricsMetadataSchema,
                                   data_key='open-metrics-metadata', description='Open Metrics Metadata.')


class eBPFProgramConfigCatalogSchema(Schema):
    """
    eBPF program configuration.
    """
    code = String(required=True, description='Code the eBPF program.')
    metrics = Nested(eBPFProgramCatalogMetricSchema, many=True, description='eBPF program metrics.')
