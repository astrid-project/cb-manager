from .base import BaseResource
from elasticsearch_dsl import Document, Text, Date


class ExecEnvDocument(Document):
    hostname = Text()
    type_id = Text()
    # started = Date() # TODO

    class Index:
        name = 'exec-env'


class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
    route = ['/config/exec-env', '/config/exec-env/{id}']
