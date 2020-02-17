from marshmallow import fields, Schema


class NetworkLinkTypeSchema(Schema):
    """
    Represents a network link type.
    """
    id = fields.String(required=True, description='ID of the network link type.', example='pnt2pnt')
    name = fields.String(required=True, description='Name of the network link type.', example='Point to point')
