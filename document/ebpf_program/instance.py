from elasticsearch_dsl import Document, Text


class eBPFProgramInstanceDocument(Document):
    """Represents an eBPF program installed in an execution environment."""
    # id already defined by Elasticsearch
    description = Text()
    ebpf_program_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)

    class Index:
        """Elasticsearch configuration."""
        name = 'ebpf-program-instance'
