from marshmallow import Schema
from marshmallow.fields import Nested, String
from schema.ebpf_program.catalog.config import eBPFProgramConfigCatalogSchema
from schema.ebpf_program.catalog.parameter import eBPFProgramParameterCatalogSchema


class eBPFProgramCatalogSchema(Schema):
    """
    Represents an eBPF program in the catalog.
    """

    id = String(required=True, dump_only=True, description='Id of the eBPF program in the catalog.',
                example='packet-capture')

    config = Nested(eBPFProgramConfigCatalogSchema, required=True, many=False)

    parameters = Nested(eBPFProgramParameterCatalogSchema, many=True)

    description = String(description='Description of eBPF program.',
                         example='Transparent service to capture packets flowing through the interface it is attached to, apply filters and obtain capture in .pcap format.')
