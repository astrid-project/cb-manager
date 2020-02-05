from .config import ConfigResource
from elasticsearch_dsl import Document, Text, Nested, InnerDoc, Boolean

class AgentParameterInnerDoc(InnerDoc):
    name = Text()
    type = Text()
    list = Boolean()


class AgentCatalogDocument(Document):
    name = Text()
    parameters = Nested(AgentParameterInnerDoc)

    class Index:
        name = 'agent-catalog'


AgentCatalogDocument.init()


class AgentCatalogResource(ConfigResource):
    doc_cls = AgentCatalogDocument
    doc_name = 'Agent Catalog'