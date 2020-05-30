from document.network_link.type import NetworkLinkTypeDocument
from resource.base import BaseResource
from schema.network_link.type import NetworkLinkTypeSchema
from docstring import docstring


@docstring(method='get',
         sum='Network Link Type Read (Multiple)',
         desc='Get the list of network link types filtered by the query in the request body.',
         resp='List of network link types filtered by the query in the request body.')
@docstring(method='post',
         sum='Network Link Type Creation (Multiple)',
         desc='Create new network link types.',
         resp='Network link types created.')
@docstring(method='delete',
         sum='Network Link Type Delete (Multiple)',
         desc='Delete network link types filtered by the query in the request body.',
         resp='Network link types filtered by the query in the request body deleted.')
@docstring(method='put',
         sum='Network Link Type Update (Multiple)',
         desc='Update network link types.',
         resp='Network link types updated.')
class NetworkLinkTypeResource(BaseResource):
    doc_cls = NetworkLinkTypeDocument
    doc_name = 'Network Link Type'
    routes = '/type/network-link/'
    schema_cls =NetworkLinkTypeSchema
