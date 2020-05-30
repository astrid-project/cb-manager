from marshmallow import Schema
from marshmallow.fields import Nested, String
from schema.ebpf_program.catalog.config import eBPFProgramConfigCatalogSchema
from schema.ebpf_program.catalog.parameter import eBPFProgramParameterCatalogSchema


class eBPFProgramCatalogSchema(Schema):
    """
    Represents an eBPF program in the catalog.
    """

    id = String(required=True,
                description='ID of the eBPF program in the catalog.',
                example='packet-capture')

    description = String(required=False,
                         description='Description of eBPF program.',
                         example='Transparent service to capture packets flowing through the interface it is attached to, apply filters and obtain capture in .pcap format.')

    config = Nested(eBPFProgramConfigCatalogSchema,
                    required=True,
                    many=False)

    parameters = Nested(eBPFProgramParameterCatalogSchema,
                        required=True,
                        many=True)
