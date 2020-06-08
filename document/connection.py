from document.base import BaseDocument
from elasticsearch_dsl import Text


class ConnectionDocument(BaseDocument):
    """Represents an connection between execution environments and network links."""
    # id already defined by Elasticsearch
    exec_env_id = Text(required=True)
    network_link_id = Text(required=True)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'connection'
