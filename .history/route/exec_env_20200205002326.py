from .config import ConfigResource
from elasticsearch_dsl import Document, Text, Object


class ExecEnvDocument(Document):
    hostname = Text()
    type = Object()

    class Index:
        name = 'exec-env'


class ExecEnvResource(ConfigResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
