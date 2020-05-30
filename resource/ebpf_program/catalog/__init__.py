from document.ebpf_program.catalog import eBPFProgramCatalogDocument
from resource.base import BaseResource
from schema.ebpf_program.catalog import eBPFProgramCatalogSchema
from docstring import docstring


@docstring(method='get',
         sum='eBPF Program Read (Multiple)',
         desc='Get the list of eBPF programs in the catalog filtered by the query in the request body.',
         resp='List of eBPF programs in the catalog filtered by the query in the request body.')
@docstring(method='post',
         sum='eBPF Program Creation (Multiple)',
         desc='Add new eBPF programs to the catalog',
         resp='eBPF programs inserted in the catalog.')
@docstring(method='delete',
         sum='eBPF Program Delete (Multiple)',
         desc='Delete eBPF Programs filtered by the query in the request body from the catalog.',
         resp='eBPF programs filtered by the query in the request body deleted from the catalog.')
@docstring(method='put',
         sum='eBPF Program Update (Multiple)',
         desc='Update eBPF programs in the catalog.',
         resp='eBPF programs updated in the catalog.')
class eBPFProgramCatalogResource(BaseResource):
    doc_cls = eBPFProgramCatalogDocument
    doc_name = 'eBPF Program Catalog'
    routes = '/catalog/ebpf-program/'
    schema_cls = eBPFProgramCatalogSchema
