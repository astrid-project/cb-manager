from .base import BaseResource
from elasticsearch_dsl import Document, Text


class AgentInstanceDocument(Document):
    agent_catalog_id = Text()
    exec_env_id = Text()
    status = Text()

    class Index:
        name = 'agent-instance'


class AgentInstanceResource(BaseResource):
    doc_cls = AgentInstanceDocument
    doc_name = 'Agent Instance'
    route = '/config/instance'
