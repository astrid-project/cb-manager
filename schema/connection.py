from marshmallow import Schema
from marshmallow.fields import Str
from schema.exec_env import ExecEnvSchema
from schema.network_link import NetworkLinkSchema


class ConnectionSchema(Schema):
    """Represents an connection between execution environments and network links."""
    id = Str(required=True, dump_only=True, example='conn-1', readonly=True,
             description='Id of connection.')
    description = Str(description='Short description of the connection.',
                      example='Added to this network for debug purposes.')
    exec_env_id = Str(required=True, description='Id of the connected execution environment.',
                      example='apache', readonly=True)
    network_link_id = Str(required=True, example='net-link-1',
                          description='Id of the connected network link.', readonly=True)
