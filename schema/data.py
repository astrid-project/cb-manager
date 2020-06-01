from marshmallow import Schema
from marshmallow.fields import DateTime, Str
from schema.agent.instance import AgentInstanceSchema
from schema.ebpf_program.instance import eBPFProgramInstanceSchema


class DataSchema(Schema):
    """Represents the stored data."""
    id = Str(required=True, dump_only=True,
             description='Id of the data.', example='BXrHRn5RPU55Qh9JwMZn')
    agent_instance_id = Str(description="""Id of the agent instance in the execution environment
                                              that collected the data""", example='filebeat@apache')
    ebpf_program_instance_id = Str(description="""Id of the eBPF program instance in the execution
                                                  environment that collected the data""",
                                   example='packet-capture@apache')
    timestamp_event = DateTime(description='Timestamp of the event related to the collected data',
                               example='2019_02_14 15:23:30')
    timestamp_agent = DateTime(description='Timestamp when the agent instance collected the data',
                               example='2019_02_14 15:23:30')
