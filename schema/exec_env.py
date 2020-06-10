from document.exec_env import ExecEnvDocument, ExecEnvTypeDocument
from marshmallow import Schema
from marshmallow.fields import DateTime, Integer, Nested, Str
from schema.base import BaseSchema
from schema.validate import _in, msg_id_not_found
from utils.datetime import FORMAT


class LCPSchema(Schema):
    """Configuration of the LCP running in the execution environment."""

    port = Integer(required=True, example=5000,
                   description='TCP port number of LCP in the execution environment.')
    started = Str(example='2019/02/14 15:23:30',
                       description='Timestamp when the LCP is started')
    last_heartbeat = Str(example='2019/02/14 15:23:33',
                              description='Timestamp of the expiration of the API access configuration.')
    username = Str(description='Username for the CB to connect to this LCP.') # FIXME DateTime
    password = Str(description='Password for the CB to connect to this LCP.') # FIXME DateTime


class ExecEnvSchema(BaseSchema):
    """Represents an execution environment."""
    doc_cls = ExecEnvDocument

    id = Str(required=True, example='apache',
             description='Id of the execution environment.')
    hostname = Str(required=True, example='192.168.1.2',
                   description='Hostname of the execution environment.')
    type_id = Str(required=True, example='vm',
                  description='Id of the execution environment type.',
                  validate=_in(ExecEnvTypeDocument.get_ids),
                  error_messages=dict(validator_failed=msg_id_not_found))
    lcp = Nested(LCPSchema, required=True, unknown='INCLUDE',
                 description='Data related to the LCP.')
    description = Str(example='Apache HTTP Web Server.',
                      description='Short description of the execution environment,')


class ExecEnvTypeSchema(BaseSchema):
    """Represents an execution environment type."""
    doc_cls = ExecEnvTypeDocument

    id = Str(required=True, example='vm',
             description='Id of the execution environment type.')
    name = Str(required=True, example='Virtual Machine',
               description='Name of the execution environment.')
    description = Str(example='Linux container.',
                      description='Short description of the type.')
