from .config import ConfigResource
from elasticsearch_dsl import Document, Text


class ConnectionDocument(Document):
    exec_env_id = Text()
    network_link_id = Text()

    class Index:
        name = 'connection'


class ConnectionResource(ConfigResource):
    doc_cls = ConnectionDocument
    doc_name = 'Connection'
