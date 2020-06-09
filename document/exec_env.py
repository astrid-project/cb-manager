from document.base import BaseDocument
from elasticsearch_dsl import Date, InnerDoc, Integer, Nested, Text


class LCPDocument(InnerDoc):
    """LCP configuration data."""
    port = Integer(required=True)
    started = Date()
    last_heartbeat = Date()
    username = Text()
    password = Text()


class ExecEnvDocument(BaseDocument):
    """Represents an execution environment."""
    # id already defined by Elasticsearch
    hostname = Text(required=True)
    type_id = Text(required=True)
    lcp = Nested(LCPDocument, required=True)
    description = Text()

    class Index:
        """Elasticsearch configuration."""
        name = 'exec-env'


class ExecEnvTypeDocument(BaseDocument):
    """Type of execution environment. Example: virtual machine or container."""
    # id already defined by Elasticsearch
    name = Text(required=True)
    description = Text()

    class Index:
        """Elasticseach configuration."""
        name = 'exec-env-type'
