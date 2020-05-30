from document.connection import ConnectionDocument
from resource.base import BaseResource
from schema.connection import ConnectionSchema
from docstring import docstring


@docstring(method='get',
         sum='Connection Read (Multiple)',
         desc="""Get the list of connections between execution environments and network links filtered
                 by the query in the request body.""",
         resp="""List of connections between execution environments and network links filtered
                 by the query in the request body.""")
@docstring(method='put',
         sum='Connection Creation (Multiple)',
         desc='Install new connections between execution environments and network links.',
         resp='Connections created between execution environments and network links.')
@docstring(method='delete',
         sum='Connection Delete (Multiple)',
         desc="""Delete the connections between execution environments and network links
                 filtered by the query in the request body.""",
         resp="""Connections between execution environments and network links filtered by the
                 query in the request body deleted.""")
@docstring(method='put',
         sum='Connection Update (Multiple)',
         desc='Update the connections between execution environments and network links.',
         resp='Connections updated between execution environments and network links.')
class ConnectionResource(BaseResource):
    doc_cls = ConnectionDocument
    doc_name = 'Connection'
    routes = '/connection/',
    schema_cls =ConnectionSchema
