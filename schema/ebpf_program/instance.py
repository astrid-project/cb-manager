from marshmallow import Schema
from marshmallow.fields import Str
from schema.ebpf_program.catalog import eBPFProgramCatalogSchema
from schema.exec_env import ExecEnvSchema


class eBPFProgramInstanceSchema(Schema):
    """Represents an eBPF program installed in an execution environment."""
    id = Str(required=True, dump_only=True, example='packet-capture@apache', readonly=True,
             description='Id of the eBPF program installed in an execution environment.')
    ebpf_program_catalog_id = Str(required=True, description='Id of the agent in the catalog.',
                                  example='packet-capture', readonly=True)
    exec_env_id = Str(required=True, description="""Id of the execution environment where the eBPF program
                                                    instance is installed""", example='apache', readonly=True)
    description = Str(description='Short description of the agent installed in the execution environment.',
                      example='Collect system metrics from Apache HTTP Web Server.')
