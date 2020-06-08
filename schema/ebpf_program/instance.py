from document.ebpf_program.catalog import eBPFProgramCatalogDocument
from document.ebpf_program.instance import eBPFProgramInstanceDocument
from document.exec_env import ExecEnvDocument
from marshmallow import Schema
from marshmallow.fields import Str
from schema.base import BaseSchema
from schema.ebpf_program.catalog import eBPFProgramCatalogSchema
from schema.exec_env import ExecEnvSchema
from schema.validate import _in, msg_id_not_found, msg_id_not_in_catalog

class eBPFProgramInstanceSchema(BaseSchema):
    """Represents an eBPF program installed in an execution environment."""
    doc_cls = eBPFProgramInstanceDocument

    id = Str(required=True, example='packet-capture@apache',
             description='Id of the eBPF program installed in an execution environment.')

    ebpf_program_catalog_id = Str(required=True, readonly=True, example='packet-capture',
                                  description='Id of the agent in the catalog.',
                                  validate=_in(eBPFProgramCatalogDocument.get_ids),
                                  error_messages=dict(validator_failed=msg_id_not_in_catalog))

    exec_env_id = Str(required=True, readonly=True, example='apache',
                      description="""Id of the execution environment where the eBPF program
                                     instance is installed""",
                      validate=_in(ExecEnvDocument.get_ids),
                      error_messages=dict(validator_failed=msg_id_not_found))

    description = Str(example='Collect system metrics from Apache HTTP Web Server.',
                      description='Short description of the agent installed in the execution environment.')
