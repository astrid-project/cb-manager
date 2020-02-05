import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text

class AgentInstanceDocument(Document):
    name = Text()
    agent_catalog_id = Text()

    class Index:
        name = 'agent-catalog'


AgentInstanceDocument.init()


class AgentInstanceResource(BaseResource):
    doc_cls = AgentInstanceDocument
    doc_name = 'Agent Catalog'
