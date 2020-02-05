from .config import ConfigResource
from elasticsearch_dsl import Document, Text


class NetworkLinkDocument(Document):
    type_id = Text()

    class Index:
        name = 'network-link'


NetworkLinkDocument.init()


class NetworkLinkResource(ConfigResource):
    doc_cls = NetworkLinkDocument
    doc_name = 'Network Link'
