import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class NetworkLinkDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env'


ExecEnvDocument.init()


class NetworkLinkResource(BaseResource):
    doc_cls = NetworkLinkDocument
    doc_name = 'Execution Environment'
