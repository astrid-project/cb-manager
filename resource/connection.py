from .base import BaseResource
from elasticsearch_dsl import Document, Text
from utils import docstring_parameter


class ConnectionDocument(Document):
    exec_env_id = Text()
    network_link_id = Text()

    class Index:
        name = 'connection'


@docstring_parameter(docstring='base', schema='ConnectionSchema', tag='connection',
                     get_summary='Connection Read (Multiple)',
                     get_description='Get the list of connections between execution environments and network links filtered by the query in the request body.',
                     get_responses_200_description='List of connections between execution environments and network links filtered by the query in the request body.',
                     post_summary='Connection Creation (Multiple)',
                     post_description='Install new connections between execution environments and network links.',
                     post_responses_200_description='Connections created between execution environments and network links.',
                     delete_summary='Connection Delete (Multiple)',
                     delete_description='Delete the connections between execution environments and network links filtered by the query in the request body.',
                     delete_responses_200_description='Connections between execution environments and network links filtered by the query in the request body deleted.',
                     put_summary='Connection Update (Multiple)',
                     put_description='Update the connections between execution environments and network links.',
                     put_responses_200_description='Connections updated between execution environments and network links.')
class ConnectionResource(BaseResource):
    doc_cls = ConnectionDocument
    doc_name = 'Connection'
    routes = '/config/connection', '/config/connection/{id}'


@docstring_parameter(dpcstring='selected', schema='ConnectionSchema', tag='connection',
                     get_summary='Connection Read (Single)',
                     get_description='Get the connection between execution environments with the given `id` and network links filtered by the query in the request body.',
                     get_responses_200_description='Connection between execution environments and network links with the given `id` and filtered by the query in the request body.',
                     post_summary='Connection Creation (Single)',
                     post_description='Install a new connection between execution environments and network links with the given `id`.',
                     post_responses_200_description='Connections created between execution environments and network links.',
                     delete_summary='Connection Delete (Single)',
                     delete_description='Delete the connection between execution environments and network links with the given `id` and filtered by the query in the request body.',
                     delete_responses_200_description='Connection between execution environments and network links with the given `id` filtered by the query in the request body deleted.',
                     put_summary='Connection Update (Single)',
                     put_description='Update the connection between execution environments and network links with the given `id`.',
                     put_responses_200_description='Connection between execution environments and network links with the given `id` updated.')
class ConnectionSelectedResource(BaseResource):
    doc_cls = ConnectionDocument
    doc_name = 'Connection'
    routes = '/config/connection', '/config/connection/{id}'
