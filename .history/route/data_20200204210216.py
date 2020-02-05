from .base import BaseResource
from elasticsearch_dsl import Document, Text, Date


class DataDocument(Document):
    exec_env_id = Text()
    agent_instance_id = Text()
    timestamp_event = Date()
    timestamp_agent = Date()

    class Index:
        name = 'data'


DataDocument.init()


class DataResource(BaseResource):
    doc_cls = DataDocument
    doc_name = 'Data'
    path = '/data'
