import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class DataDocument(Document):
    hostname = Text()
    exec_env_id = Text()

    class Index:
        name = 'data'


ExecEnvDocument.init()


class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Data'
