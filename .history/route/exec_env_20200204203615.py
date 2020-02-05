import falcon
from query_parser import QueryParser
from schema import Query
from marshmallow import fields, Schema
import elasticsearch
from elasticsearch_dsl import Document, InnerDoc, Nested, Text


class ExecEnvDocument(Document):
    hostname = Text()
    type_id = Text()

    class Index:
        name = 'exec-env'


ExecEnvDocument.init()


class ExecEnvResource(BaseResource):
    doc_cls = ExecEnvDocument
    name = 'Execution Environment'
