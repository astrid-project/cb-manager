import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class ExecEnvTypeDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env-type'


ExecEnvTypeDocument.init()


class ExecEnvTypeResource(BaseResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
