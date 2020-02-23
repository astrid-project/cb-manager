from marshmallow import fields, Schema


class ConnectionSchema(Schema):
    """
    Represents an connection between execution environments and network links.
    """
    id = fields.String(required=True, description='ID of connection.',
                       example='aZ0aLlJ5Cq84Hsy3SyTW')
    exec_env_id = fields.String(required=True, description='ID of the connected execution environment',
                                example='1V4nbnfz981Mn95RPtTr')
    network_link_id = fields.String(required=True, description='ID of the connected network link',
                                    example='JAwfDEY7f2AtiEldMjPW')
