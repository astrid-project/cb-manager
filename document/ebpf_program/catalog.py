from elasticsearch_dsl import Boolean, Document, InnerDoc, Nested, Text


class eBPFProgramCatalogOpenMetricsMetadataLabelInnerDoc(InnerDoc):
    name = Text(required=True)
    value = Text(required=True)


class eBPFProgramCatalogOpenMetricsMetadataInnerDoc(InnerDoc):
    type = Text(required=True)
    help = Text()
    labels = Nested(eBPFProgramCatalogOpenMetricsMetadataLabelInnerDoc)


class eBPFProgramCatalogMetricInnerDoc(InnerDoc):
    name = Text(required=True)
    map_name = Text(required=True)
    open_metrics_metadata = Nested(eBPFProgramCatalogOpenMetricsMetadataInnerDoc)


class eBPFProgramConfigCatalogInnerDoc(InnerDoc):
    code = Text(required=True)
    metrics = Nested(eBPFProgramCatalogMetricInnerDoc)


class eBPFProgramParameterCatalogInnerDoc(InnerDoc):
    id = Text(required=True)
    # Possible values: integer, number, string, choice, boolean
    type = Text(required=True)
    list = Boolean()
    values = Text() # when type = choice
    example = Text()
    description = Text()


class eBPFProgramCatalogDocument(Document):
    # id already defined by Elasticsearch
    description = Text()
    config = Nested(eBPFProgramConfigCatalogInnerDoc, required=True)
    parameters = Nested(eBPFProgramParameterCatalogInnerDoc)

    class Index:
        # TODO add docstring.
        name = 'ebpf-program-catalog'
