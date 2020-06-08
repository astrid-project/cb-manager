from document.base import BaseDocument
from elasticsearch_dsl import Date, Text


class DataDocument(BaseDocument):
    """Represents the stored data."""

    # id already defined by Elasticsearch
    agent_instance_id = Text()
    ebpf_program_instance_id = Text()
    timestamp_event = Date()
    timestamp_agent = Date()

    class Index:
        """Elasticsearch configuration."""
        name = 'data'
