import falcon
from .config import ConfigResource
from elasticsearch_dsl import Document, Text


class ExecEnvTypeDocument(Document):
    name = Text()

    class Index:
        name = 'exec-env-type'


ExecEnvTypeDocument.init()


class ExecEnvTypeResource(ConfigResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
