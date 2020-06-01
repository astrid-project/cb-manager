from elasticsearch_dsl import Document, Text


class ConnectionDocument(Document):
    """Represents an connection between execution environments and network links."""
    # id already defined by Elasticsearch
    description = Text()
    exec_env_id = Text(required=True)
    network_link_id = Text(required=True)

    class Index:
        """Elasticsearch configuration."""
        name = 'connection'
