from marshmallow import Schema
from marshmallow.fields import Str


class NetworkLinkSchema(Schema):
    """Represents a network link."""
    id = Str(required=True, dump_only=True, example='net-link-1',
             description='Id of the network link.', readonly=True)
    type_id = Str(required=True, description='Id of the network link type.',
                  example='pnt2pnt')
    description = Str(description='Short description of the network link,',
                      example='Allow communication between front-end and back-end services.')


class NetworkLinkTypeSchema(Schema):
    """Represents a network link type."""
    id = Str(required=True, dump_only=True, example='pnt2pnt', readonly=True,
             description='Id of the network link type.')
    name = Str(required=True, description='Name of the network link type.',
               example='Point to point')
    description = Str(description='Short description of the network link type,',
                      example='Communications connection between two communication endpoints.')
