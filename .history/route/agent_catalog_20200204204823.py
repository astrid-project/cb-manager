import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class AgentCatalogDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'agent-catalog'


AgentCatalogDocument.init()


class AgentCatalogResource(BaseResource):
    doc_cls = AgentCatalogDocument
    doc_name = 'Agent Catalog'
