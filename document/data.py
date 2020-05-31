from elasticsearch_dsl import Date, Document, Text


class DataDocument(Document):
    """
    Represents the stored data.
    """

    # id already defined by Elasticsearch

    agent_instance_id = Text()

    ebpf_program_instance_id = Text()

    timestamp_event = Date()

    timestamp_agent = Date()

    class Index:
        name = 'data'
