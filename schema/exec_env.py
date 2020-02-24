from marshmallow import fields, Schema


class LCPSchema(Schema):
    port = fields.Integer(required=True, description='TCP port number of LCPs in the execution environment.',
                          example=5000)
    username = fields.String(required=True, description='Username to connect from the CB to the LCP.',
                            example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5')
    password = fields.String(required=True, description='Password to connect from the CB to the LCP.',
                            example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5')
    cb_password = fields.String(required=True, description='Hashed password assigned to LCP to connect with the CB.',
                                example='22c6d368beabf9de1ea03e010010758a394c37c3b18aa0705b8634f5')
    cb_expiration = fields.DateTime(required=True, description='Datetime until the authentication with the CB is valid.',
                                    example='2019_02_14 15:23:30')
    last_hearbeat = fields.DateTime(description='Timestamp of the last hearbeat between the LCP and CB.',
                                    example='2019_02_14 15:23:30')


class ExecEnvSchema(Schema):
    """
    Represents an execution environment.
    """
    id = fields.String(required=True, description='ID of the execution environment.',
                       example='PiOIb3ABjPI5oepgse1C')
    hostname = fields.String(required=True, description='Hostname of the execution environment.',
                             example='192.168.1.2')
    lcp = fields.Nested(LCPSchema, required=True, description='Data related to the LCP')
    type_id = fields.String(required=True, description='ID of the execution environment type.',
                            example='vm')
