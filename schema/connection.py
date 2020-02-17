from marshmallow import fields, Schema


class ConnectionSchema(Schema):
    """
    Represents an connection between execution environments and network links.
    """
    id = fields.String(required=True, description='ID of connection.', example='connection-1')
    exec_env_id = fields.String(required=True, description='ID of the connected execution environment', example='exec-env-1')
    network_link_id = fields.String(required=True, description='ID of the connected network link', example='network-link-1')
