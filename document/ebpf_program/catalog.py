from document.base import BaseDocument
from elasticsearch_dsl import Boolean, InnerDoc, Nested, Text


class eBPFProgramCatalogOpenMetricsMetadataLabelInnerDoc(InnerDoc):
    """eBPF program open metrics label."""
    name = Text(required=True)
    value = Text(required=True)


class eBPFProgramCatalogOpenMetricsMetadataInnerDoc(InnerDoc):
    """eBPF program open metrics metadata."""
    type = Text(required=True)
    help = Text()
    labels = Nested(eBPFProgramCatalogOpenMetricsMetadataLabelInnerDoc)


class eBPFProgramCatalogMetricInnerDoc(InnerDoc):
    """eBPF program metric data."""
    name = Text(required=True)
    map_name = Text(required=True)
    open_metrics_metadata = Nested(
        eBPFProgramCatalogOpenMetricsMetadataInnerDoc)


class eBPFProgramConfigCatalogInnerDoc(InnerDoc):
    """eBPF program parameter configuration."""
    code = Text(required=True)
    metrics = Nested(eBPFProgramCatalogMetricInnerDoc)


class eBPFProgramParameterCatalogInnerDoc(InnerDoc):
    """eBPF program parameter."""
    id = Text(required=True)
    # possible values: integer, number, string, choice, boolean
    type = Text(required=True)
    list = Boolean()
    values = Text()  # when type = choice
    description = Text()
    example = Text()


class eBPFProgramCatalogDocument(BaseDocument):
    """Represents an eBPF program in the catalog."""
    # id already defined by Elasticsearch
    config = Nested(eBPFProgramConfigCatalogInnerDoc, required=True)
    parameters = Nested(eBPFProgramParameterCatalogInnerDoc)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'ebpf-program-catalog'
