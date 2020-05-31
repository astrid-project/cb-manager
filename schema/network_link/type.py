from marshmallow import Schema
from marshmallow.fields import String


class NetworkLinkTypeSchema(Schema):
    """
    Represents a network link type.
    """

    id = String(required=True, dump_only=True, description='Id of the network link type.', example='pnt2pnt')

    name = String(required=True, description='Name of the network link type.', example='Point to point')

    description = String(description='Short description of the network link type,',
                         example='Communications connection between two communication endpoints.')
