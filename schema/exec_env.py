from marshmallow import fields, Schema


class ExecEnvSchema(Schema):
    """
    Represents an execution environment.
    """
    id = fields.String(required=True, description='ID of the execution environment.',
                       example='PiOIb3ABjPI5oepgse1C')
    hostname = fields.String(required=True, description='Hostname of the execution environment.',
                             example='192.168.1.2')
    lcp_port = fields.Integer(required=True, description='TCP port number of LCPs in the execution environment.',
                             example=5000)
    type_id = fields.String(required=True, description='ID of the execution environment type.',
                            example='vm')
    # started = fields.DateTime(description='Timestamp when the LCP is started in this execution environment',
    #                           example='2019_02_14-15:23:30') # TODO Not work with Elastic
