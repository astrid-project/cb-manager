from document.ebpf_program.instance import eBPFProgramInstanceDocument
from resource.base import BaseResource
from resource.ebpf_program.instance.lcp.post import lcp_post
from resource.ebpf_program.instance.lcp.put import lcp_put
from resource.ebpf_program.instance.lcp.delete import lcp_delete
from schema.ebpf_program.instance import eBPFProgramInstanceSchema
from docstring import docstring

@docstring(method='get',
         sum='eBPF Program Read (Multiple)',
         desc="""Get the list of eBPF program instances installed in the execution-environments
                 filtered by the query in the request body.""",
         resp="""List of eBPF program instances installed in the execution-environment
                 filtered by the query in the request body.""")
@docstring(method='post',
         sum='eBPF Program Install (Multiple)',
         desc='Install new eBPF program instances in the execution-environments.',
         resp='eBPF program installed in the execution environments.')
@docstring(method='delete',
         sum='eBPF Program Uninstall (Multiple)',
         desc="""Remove the eBPF program instances filtered by the query in the request body from the
                 execution-environments.""",
         resp='eBPF programs filtered by the query in the request body uninstalled.')
@docstring(method='put',
         sum='eBPF Program Update (Multiple)',
         desc='Update the eBPF program instances in the execution-environments.',
         resp='eBPF programs updated.')
class eBPFProgramInstanceResource(BaseResource):
    doc_cls = eBPFProgramInstanceDocument
    doc_name = 'eBPF Program'
    routes = '/instance/ebpf-program/',
    schema_cls =eBPFProgramInstanceSchema
    lcp_handler = dict(post=lcp_post, put=lcp_put, delete=lcp_delete)
    nested_fields = ['parameters']
