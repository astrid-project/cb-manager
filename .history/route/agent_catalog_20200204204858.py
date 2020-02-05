import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text, Nested, InnerDoc


class AgentCatalogDocument(Document):
    name = Text()
    type_id = Nested(AgentParameterDocument)

    class Index:
        name = 'agent-catalog'


AgentCatalogDocument.init()


class AgentCatalogResource(BaseResource):
    doc_cls = AgentCatalogDocument
    doc_name = 'Agent Catalog'
