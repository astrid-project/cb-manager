from document.agent.instance import AgentInstanceDocument
from document.ebpf_program.instance import eBPFProgramInstanceDocument
from document.data import DataDocument
from marshmallow import Schema
from marshmallow.fields import DateTime, Str
from schema.agent.instance import AgentInstanceSchema
from schema.base import BaseSchema
from schema.ebpf_program.instance import eBPFProgramInstanceSchema
from schema.validate import _in, msg_id_not_found
from utils.datetime import FORMAT


class DataSchema(BaseSchema):
    """Represents the stored data."""
    doc_cls = DataDocument

    id = Str(required=True, example='BXrHRn5RPU55Qh9JwMZn',
             description='Id of the data.')
    agent_instance_id = Str(readonly=True, example='filebeat@apache',
                            description="""Id of the agent instance in the execution environment
                                           that collected the data""",
                            validate=_in(AgentInstanceDocument.get_ids),
                            error_messages=dict(validator_failed=msg_id_not_found))
    ebpf_program_instance_id = Str(readonly=True, example='packet-capture@apache',
                                   description="""Id of the eBPF program instance in the execution
                                                  environment that collected the data""",
                                   validate=_in(eBPFProgramInstanceDocument.get_ids),
                                   error_messages=dict(validator_failed=msg_id_not_found))
    timestamp_event = DateTime(format=FORMAT, readonly=True, example='2019/02/14 15:23:30',
                               description='Timestamp of the event related to the collected data')
    timestamp_agent = DateTime(format=FORMAT, readonly=True, example='2019/02/14 15:23:30',
                               description='Timestamp when the agent instance collected the data')
