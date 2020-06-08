from document.exec_env import ExecEnvDocument, ExecEnvTypeDocument
from marshmallow import Schema
from marshmallow.fields import DateTime, Integer, Nested, Str
from schema.base import BaseSchema
from schema.validate import _in, msg_id_not_found


class LCPSchema(Schema):
    """Configuration of the LCP running in the execution environment."""

    port = Integer(required=True, example=5000,
                   description='TCP port number of LCP in the execution environment.')

    username = Str(example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5',
                   description='Username to connect from the CB to the LCP.')

    password = Str(example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5',
                   description='Password to connect from the CB to the LCP.')

    cb_password = Str(example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5',
                      description='Hashed password assigned to LCP to connect with the CB.')

    cb_expiration = DateTime(format='%Y/%m/%d %H:%M:%S', example='2019_02_14 15:23:30',
                             description='Datetime until the authentication with the CB is valid.')

    last_hearbeat = DateTime(format='%Y/%m/%d %H:%M:%S', example='2019_02_14 15:23:30',
                             description='Timestamp of the last hearbeat between the LCP and CB.')


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

    lcp = Nested(LCPSchema, required=True,
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
