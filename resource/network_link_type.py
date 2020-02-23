from .base import BaseResource
from elasticsearch_dsl import Document, Text
from utils import docstring_parameter


class NetworkLinkTypeDocument(Document):
    name = Text(required=True)

    class Index:
        name = 'network-link-type'


@docstring_parameter(docstring='base', schema='NetworkLinkTypeSchema', tag='network-link-type',
                     get_summary='Network Link Type Read (Multiple)',
                     get_description='Get the list of network link types filtered by the query in the request body.',
                     get_responses_200_description='List of network link types filtered by the query in the request body.',
                     post_summary='Network Link Type Creation (Multiple)',
                     post_description='Create new network link types.',
                     post_responses_200_description='Network link types created.',
                     delete_summary='Network Link Type Delete (Multiple)',
                     delete_description='Delete network link types filtered by the query in the request body.',
                     delete_responses_200_description='Network link types filtered by the query in the request body deleted.',
                     put_summary='Network Link Type Update (Multiple)',
                     put_description='Update network link types.',
                     put_responses_200_description='Network link types updated.')
class NetworkLinkTypeResource(BaseResource):
    doc_cls = NetworkLinkTypeDocument
    doc_name = 'Network Link Type'
    routes = '/config/network-link-type/'


@docstring_parameter(docstring='selected', schema='NetworkLinkTypeSchema', tag='network-link-type',
                     get_summary='Network Link Type Read (Single)',
                     get_description='Get the network link type with the given `id` and filtered by the query in the request body.',
                     get_responses_200_description='Network link type with the given `id` and filtered by the query in the request body.',
                     post_summary='Network Link Type Creation (Single)',
                     post_description='Create a new network link type with the given `id` .',
                     post_responses_200_description='Network link type with the given `id` created.',
                     delete_summary='Network Link Type Delete (Single)',
                     delete_description='Delete the network link type with the given `id` and filtered by the query in the request body.',
                     delete_responses_200_description='Network link type with the given `id` and filtered by the query in the request body deleted.',
                     put_summary='Network Link Type Update (Single)',
                     put_description='Update the network link type with the given `id`.',
                     put_responses_200_description='Network link type with the given `id` updated.')
class NetworkLinkTypeSelectedResource(BaseResource):
    doc_cls = NetworkLinkTypeDocument
    doc_name = 'Network Link Type'
    routes = '/config/network-link-type/{id}'
