import falcon
from .base import BaseResource
from elasticsearch_dsl import Document, Text


class ExecEnvTypeDocument(Document):
    name = Text()

    class Index:
        name = 'exec-env-type'


class ExecEnvTypeResource(ConfigResource):
    doc_cls = ExecEnvTypeDocument
    doc_name = 'Execution Environment Type'
    route = '/config/exec-env'