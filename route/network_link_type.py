from .base import BaseResource
from elasticsearch_dsl import Document, Text


class NetworkLinkTypeDocument(Document):
    name = Text()

    class Index:
        name = 'network-link-type'


class NetworkLinkTypeResource(BaseResource):
    doc_cls = NetworkLinkTypeDocument
    doc_name = 'Network Link Type'
    route = ['/config/network-link-type', '/config/network-link-type/{id}']

