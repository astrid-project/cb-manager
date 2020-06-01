from elasticsearch_dsl import Document, Text


class NetworkLinkDocument(Document):
    """Represents a network link."""
    # id already defined by Elasticsearch
    description = Text()
    type_id = Text(required=True)

    class Index:
        """Elasticsearch configuration."""
        name = 'network-link'


class NetworkLinkTypeDocument(Document):
    """Represents a network link type."""
    # id already defined by Elasticsearch
    name = Text(required=True)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'network-link-type'
