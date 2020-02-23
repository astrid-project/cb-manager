from marshmallow import fields, Schema


class NetworkLinkSchema(Schema):
    """
    Represents a network link.
    """
    id = fields.String(required=True, description='ID of the network link.',
                       example='x4fgctkm4MXQOUHYjIag')
    type_id = fields.String(required=True, description='ID of the network link type.',
                            example='pnt2pnt')
