from marshmallow import Schema
from marshmallow.fields import Nested, String


class eBPFProgramCatalogOpenMetricsMetadataLabelSchema(Schema):
    """
    eBPF program Open Metrics metadata label.
    """
    name = String(required=True, description='Label name.', example='IP_PROTO')
    value = String(required=True, description='Label value.', example='UDP')


class eBPFProgramCatalogOpenMetricsMetadataSchema(Schema):
    """
    eBPF program Open Metrics metadata.
    """
    type = String(required=True, description='Metric type.', example='counter')
    help = String(description='Metric help.',
                  example='This metric represents the number of packets that has traveled trough this probe.')
    labels = Nested(eBPFProgramCatalogOpenMetricsMetadataLabelSchema,
                    description='Labels of Open Metrics Metadata.')

