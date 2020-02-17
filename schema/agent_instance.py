from marshmallow import fields, Schema


class AgentInstanceSchema(Schema):
    """
    Represents an agent instance installed in an execution environment.
    """
    id = fields.String(required=True, description='ID of the agent instance installed in an execution environment.',
                       example='agent-instance-1')
    agent_catalog_id = fields.String(required=True, description='ID of the agent in the catalog', example='agent-filebeat-1')
    exec_env_id = fields.String(required=True,
                                description='ID of the execution environment where the agent instance is installed',
                                example='exec-env-1')
