from document.network_link import NetworkLinkDocument, NetworkLinkTypeDocument
from marshmallow import Schema
from marshmallow.fields import Str
from schema.base import BaseSchema
from schema.validate import _in, msg_id_not_found


class NetworkLinkSchema(BaseSchema):
    """Represents a network link."""
    doc_cls = NetworkLinkDocument

    id = Str(required=True, example='net-link-1',
             description='Id of the network link.')

    type_id = Str(required=True, example='pnt2pnt',
                  description='Id of the network link type.',
                  validate=_in(NetworkLinkTypeDocument.get_ids),
                  error_messages=dict(validator_failed=msg_id_not_found))

    description = Str(example='Allow communication between front-end and back-end services.',
                      description='Short description of the network link,')


class NetworkLinkTypeSchema(BaseSchema):
    """Represents a network link type."""
    doc_cls = NetworkLinkTypeDocument

    id = Str(required=True, example='pnt2pnt',
             description='Id of the network link type.')

    name = Str(required=True, readonly=True, example='Point to point',
               description='Name of the network link type.')

    description = Str(example='Communications connection between two communication endpoints.',
                      description='Short description of the network link type,')
