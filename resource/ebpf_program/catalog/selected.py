from document.ebpf_program.catalog import eBPFProgramCatalogDocument
from resource.base import BaseResource
from schema.ebpf_program.catalog import eBPFProgramCatalogSchema
from docstring import docstring


@docstring(method='get',
         sum='eBPF Program Read (Single)',
         desc='Get the eBPF program in the catalog with the given `id` and filtered by the query in the request body.',
         resp='eBPF Program in the catalog with the given `id` and filtered by the query in the request body.')
@docstring(method='post',
         sum='eBPF Program Creation (Single)',
         desc='Add a new eBPF program in the catalog with the given `id`.',
         resp='eBPF Program with the given `id` inserted in the catalog.')
@docstring(method='delete',
         sum='eBPF Program Delete (Single)',
         desc='Delete the eBPF program with the given `id` and filtered by the query in the request body.',
         resp='eBPF Program with the given `id` and filtered by the query in the request body deleted from the catalog.')
@docstring(method='put',
         sum='eBPF Program Update (Single)',
         desc='Update the eBPF program in the catalog with the given `id`',
         resp='eBPF Program with the given `id` updated in the catalog.')
class eBPFProgramCatalogSelectedResource(BaseResource):
    doc_cls = eBPFProgramCatalogDocument
    doc_name = 'eBPF Program Catalog'
    routes = '/catalog/ebpf-program/{id}'
    schema_cls =eBPFProgramCatalogSchema
