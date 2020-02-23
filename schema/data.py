from marshmallow import fields, Schema


class DataSchema(Schema):
    """
    Represents stored data.
    """
    id = fields.String(required=True, description='ID of the data.',
                       example='BXrHRn5RPU55Qh9JwMZn')
    exec_env_id = fields.String(description='ID of the execution environment where the data was collected',
                                example='MUgzilTNtWbQEaPjBZyv')
    agent_instance_id = fields.String(description='ID of the agent instance in the execution environment that collected the data',
                                      example='EHiirlGzEiU29VTdovTo')
    timestamp_event = fields.DateTime(description='Timestamp of the event related to the collected data',
                                      example='#TODO')
    timestamp_agent = fields.DateTime(description='Timestamp when the agent instance collected the data',
                                      example='#TODO')
