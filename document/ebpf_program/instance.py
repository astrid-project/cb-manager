from document.base import BaseDocument
from elasticsearch_dsl import Text


class eBPFProgramInstanceDocument(BaseDocument):
    """Represents an eBPF program installed in an execution environment."""
    # id already defined by Elasticsearch
    ebpf_program_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'ebpf-program-instance'
