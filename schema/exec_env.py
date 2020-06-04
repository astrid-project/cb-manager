from marshmallow import Schema
from marshmallow.fields import DateTime, Integer, Nested, Str


class LCPSchema(Schema):
    """Configuration of the LCP running in the execution environment."""
    port = Integer(required=True, description='TCP port number of LCP in the execution environment.',
                   example=5000)
    username = Str(description='Username to connect from the CB to the LCP.',
                   example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5')
    password = Str(description='Password to connect from the CB to the LCP.',
                   example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5')
    cb_password = Str(description='Hashed password assigned to LCP to connect with the CB.',
                      example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5')
    cb_expiration = DateTime(description='Datetime until the authentication with the CB is valid.',
                             example='2019_02_14 15:23:30')
    last_hearbeat = DateTime(description='Timestamp of the last hearbeat between the LCP and CB.',
                             example='2019_02_14 15:23:30')


class ExecEnvSchema(Schema):
    """Represents an execution environment."""
    id = Str(required=True, dump_only=True, example='apache',
             description='Id of the execution environment.', readonly=True)
    hostname = Str(required=True, example='192.168.1.2',
                   description='Hostname of the execution environment.')
    type_id = Str(required=True, example='vm',
                  description='Id of the execution environment type.')
    lcp = Nested(LCPSchema, required=True,
                 description='Data related to the LCP.')
    description = Str(description='Short description of the execution environment,',
                      example='Apache HTTP Web Server.')


class ExecEnvTypeSchema(Schema):
    """Represents an execution environment type."""
    id = Str(required=True, dump_only=True, example='vm',
             description='Id of the execution environment type.', readonly=True)
    name = Str(required=True, description='Name of the execution environment.',
               example='Virtual Machine')
    description = Str(example='Linux container.',
                      description='Short description of the type.')
