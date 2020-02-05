import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class NetworkLinkTypeDocument(Document):
    name = Text()

    class Index:
        name = 'network-link-type'


ExecEnvTypeDocument.init()


class ExecEnvTypeResource(BaseResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
