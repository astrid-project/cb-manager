from .base import BaseResource
from elasticsearch_dsl import Document, Text


class ExecEnvDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env'


class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
    route = ['/config/exec-env', '/config/exec-env/{id}']
