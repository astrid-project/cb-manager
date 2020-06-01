from marshmallow import Schema
from marshmallow.fields import String
from schema.network_link.type import NetworkLinkTypeSchema


class NetworkLinkSchema(Schema):
    """
    Represents a network link.
    """

    id = String(required=True, dump_only=True,
                description='ID of the network link.',
                example='net-link-1')

    type_id = String(required=True,
                     description='Id of the network link type.',
                     example='pnt2pnt')

    description = String(description='Short description of the network link,',
                         example='Allow communication between front-end and back-end services.')
