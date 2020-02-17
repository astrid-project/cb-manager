from marshmallow import fields, Schema


class NetworkLinkSchema(Schema):
    """
    Represents a network link.
    """
    id = fields.String(required=True, description='ID of the network link.', example='network-link-1')
    type_id = fields.String(required=True, description='ID of the network link type.', example='pnt2pnt')
