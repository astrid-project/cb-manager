from .config import ConfigResource
from .exec_env_type import ExecEnvTypeDocument
from elasticsearch_dsl import Document, Text, Object


class ExecEnvDocument(Document):
    hostname = Text()
    type = Object(ExecEnvTypeDocument, required=True)

    class Index:
        name = 'exec-env'


class ExecEnvResource(ConfigResource):
    doc_cls = ExecEnvDocument
    doc_name = 'Execution Environment'
