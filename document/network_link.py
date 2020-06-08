from document.base import BaseDocument
from elasticsearch_dsl import Text


class NetworkLinkDocument(BaseDocument):
    """Represents a network link."""
    # id already defined by Elasticsearch
    type_id = Text(required=True)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'network-link'


class NetworkLinkTypeDocument(BaseDocument):
    """Represents a network link type."""
    # id already defined by Elasticsearch
    name = Text(required=True)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'network-link-type'
