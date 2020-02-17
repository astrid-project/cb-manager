from marshmallow import fields, Schema


class DataSchema(Schema):
    """
    Represents stored data.
    """
    id = fields.String(required=True, description='ID of the data.', example='data-1')
    exec_env_id = fields.String(required=True, description='ID of the execution environment where the data was collected',
                                example='exec-env-1')
    agent_instance_id = fields.String(required=True, description='ID of the agent instance in the execution environment that collected the data',
                                      example='agent-filebeat-1')
    timestamp_event = fields.DateTime(required=True, description='Timestamp of the event related to the collected data', example='#TODO')
    timestamp_agent = fields.DateTime(required=True, description='Timestamp when the agent instance collected the data', example='#TODO')
