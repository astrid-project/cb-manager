from marshmallow import Schema
from marshmallow.fields import String


class eBPFProgramInstanceSchema(Schema):
    """
    Represents an eBPF program installed in an execution environment.
    """
    id = String(required=True,
                description='ID of the eBPF program installed in an execution environment.',
                example='packet-capture@apache')
    ebpf_program_catalog_id = String(required=True,
                              description='ID of the agent in the catalog',
                              example='packet-capture')
    exec_env_id = String(required=True,
                         description='ID of the execution environment where the eBPF program instance is installed', example='apache')
    status = String(required=True,
                    enum=['install'],
                    description='Status of the eBPF program instance',
                    example='install')
