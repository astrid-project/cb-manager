import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text, Nested, InnerDoc, Boolean

class AgentInstanceDocument(Document):
    name = Text()
    parameters = Nested(AgentParameterInnerDoc)

    class Index:
        name = 'agent-catalog'


AgentInstanceDocument.init()


class AgentInstanceResource(BaseResource):
    doc_cls = AgentInstanceDocument
    doc_name = 'Agent Catalog'
