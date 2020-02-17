from .base import BaseResource
from elasticsearch_dsl import Document, Text
from utils import docstring_parameter


class NetworkLinkDocument(Document):
    type_id = Text()

    class Index:
        name = 'network-link'


@docstring_parameter(docstring='base', schema='NetworkLinkSchema', tag='network-link',
                     get_summary='Network Link Read (Multiple)',
                     get_description='Get the list of network links filtered by the query in the request body.',
                     get_responses_200_description='List of network links filtered by the query in the request body.',
                     post_summary='Network Link Creation (Multiple)',
                     post_description='Create new network links.',
                     post_responses_200_description='Network links created.',
                     delete_summary='Network Link Delete (Multiple)',
                     delete_description='Delete network links filtered by the query in the request body.',
                     delete_responses_200_description='Network links filtered by the query in the request body deleted.',
                     put_summary='Network Link Update (Multiple)',
                     put_description='Update network links.',
                     put_responses_200_description='Network links updated.')
class NetworkLinkResource(BaseResource):
    doc_cls = NetworkLinkDocument
    doc_name = 'Network Link'
    routes = '/config/networkslink', '/config/network-link/{id}'


@docstring_parameter(docstring='selected', schema='NetworkLinkSchema', tag='network-link',
                     get_summary='Network Link Read (Single)',
                     get_description='Get the network link with the given `id` and filtered by the query in the request body.',
                     get_responses_200_description='Network link with the given `id` and filtered by the query in the request body.',
                     post_summary='Network Link Creation (Single)',
                     post_description='Create a new network link with the given `id` .',
                     post_responses_200_description='Network link with the given `id` created.',
                     delete_summary='Network Link Delete (Single)',
                     delete_description='Delete the network link with the given `id` and filtered by the query in the request body.',
                     delete_responses_200_description='Network link with the given `id` and filtered by the query in the request body deleted.',
                     put_summary='Network Link Update (Single)',
                     put_description='Update the network link with the given `id`.',
                     put_responses_200_description='Network link with the given `id` updated.')
class NetworkLinkSelectedResource(BaseResource):
    doc_cls = NetworkLinkDocument
    doc_name = 'Network Link'
    routes = '/config/networkslink', '/config/network-link/{id}'
