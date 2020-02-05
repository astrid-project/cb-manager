import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text, Nested, InnerDoc, Boolean

class AgentParameterDocument(InnerDoc):
    name = Text()
    type = Text()
    list = Boolean()


class AgentCatalogDocument(Document):
    name = Text()
    parameters = Nested(AgentParameterDocument)

    class Index:
        name = 'agent-catalog'


AgentCatalogDocument.init()


class AgentCatalogResource(BaseResource):
    doc_cls = AgentCatalogDocument
    doc_name = 'Agent Catalog'
