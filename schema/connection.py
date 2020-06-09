from document.connection import ConnectionDocument
from document.exec_env import ExecEnvDocument
from document.network_link import NetworkLinkDocument
from marshmallow import Schema
from marshmallow.fields import Str
from schema.exec_env import ExecEnvSchema
from schema.network_link import NetworkLinkSchema
from schema.base import BaseSchema
from schema.validate import _in, msg_id_not_found


class ConnectionSchema(BaseSchema):
    """Represents an connection between execution environments and network links."""
    doc_cls = ConnectionDocument

    id = Str(required=True, example='conn-1',
             description='Id of connection.')
    exec_env_id = Str(required=True, readonly=True, example='apache',
                      description='Id of the connected execution environment.',
                      validate=_in(ExecEnvDocument.get_ids),
                      error_messages=dict(validator_failed=msg_id_not_found))
    network_link_id = Str(required=True, readonly=True, example='net-link-1',
                          description='Id of the connected network link.',
                          validate=_in(NetworkLinkDocument.get_ids),
                          error_messages=dict(validator_failed=msg_id_not_found))
    description = Str(example='Added to this network for debug purposes.',
                      description='Short description of the connection.')
