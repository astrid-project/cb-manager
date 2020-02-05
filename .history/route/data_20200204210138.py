from .base import BaseResource
from elasticsearch_dsl import Document, Text, Date


class DataDocument(Document):
    exec_env_id = Text()
    agent_instance_id = Text()
    timestamp_event = Date()
    timestamp_agent = Date()

    class Index:
        name = 'data'


ExecEnvDocument.init()


class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Data'
    path = '/data'
