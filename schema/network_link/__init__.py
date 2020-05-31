from marshmallow import Schema
from marshmallow.fields import Pluck, String
from schema.network_link.type import NetworkLinkTypeSchema


class NetworkLinkSchema(Schema):
    """
    Represents a network link.
    """

    id = String(required=True, dump_only=True,
                description='ID of the network link.',
                example='net-link-1')

    type_id = Pluck(NetworkLinkTypeSchema, 'id', required=True,
                    description='Id of the network link type.', example='pnt2pnt')
