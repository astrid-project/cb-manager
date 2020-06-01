from marshmallow import Schema
from marshmallow.fields import String
from schema.exec_env import ExecEnvSchema
from schema.network_link import NetworkLinkSchema


class ConnectionSchema(Schema):
    """
    Represents an connection between execution environments and network links.
    """

    id = String(required=True, dump_only=True, description='Id of connection.', example='conn-1')

    exec_env_id = String(required=True, description='Id of the connected execution environment.',
                         example='apache')

    network_link_id = String(required=True, description='Id of the connected network link.',
                             example='net-link-1')

    description = String(description='Short description of the connection.',
                         example='Added to this network for debug purposes.')
