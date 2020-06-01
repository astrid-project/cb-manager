from marshmallow import Schema
from marshmallow.fields import String
from schema.ebpf_program.catalog import eBPFProgramCatalogSchema
from schema.exec_env import ExecEnvSchema


class eBPFProgramInstanceSchema(Schema):
    """
    Represents an eBPF program installed in an execution environment.
    """

    id = String(required=True, dump_only=True,
                description='Id of the eBPF program installed in an execution environment.',
                example='packet-capture@apache')

    ebpf_program_catalog_id = String(required=True, description='Id of the agent in the catalog.',
                                     example='packet-capture')

    exec_env_id = String(required=True, description="""Id of the execution environment where the eBPF program
                                                       instance is installed""", example='apache')

    description = String(description='Short description of the agent installed in the execution environment.',
                         example='Collect system metrics from Apache HTTP Web Server.')
