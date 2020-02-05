import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class DataDocument(Document):
    exec_env_id = Text()
    agent_instance_id = Text()

    class Index:
        name = 'data'


ExecEnvDocument.init()


class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Data'
