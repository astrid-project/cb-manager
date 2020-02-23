from marshmallow import fields, Schema


class AgentInstanceParameterSchema(Schema):
    name = fields.String(required=True, description='Parameter name',
                         example='period')
    value = fields.String(required=True, description='Paremeter value',
                          example='10s')


class AgentInstanceSchema(Schema):
    """
    Represents an agent instance installed in an execution environment.
    """
    id = fields.String(required=True, description='ID of the agent instance installed in an execution environment.',
                       example='uyPMaXABjPI5oepgjezR')
    agent_catalog_id = fields.String(required=True, description='ID of the agent in the catalog',
                                     example='23jqlaJVPCGa4C0o6ljn')
    exec_env_id = fields.String(required=True,
                                description='ID of the execution environment where the agent instance is installed',
                                example='0xUosnMTCgO5FgVZLbQs')
    status = fields.String(required=True, enum=['start', 'stop'],
                           description='Status of the agent instance', example='start')
    parameters = fields.Nested(AgentInstanceParameterSchema, many=True,
                               description='List of agent instance parameters')
