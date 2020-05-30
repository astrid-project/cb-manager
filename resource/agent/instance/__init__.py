from document.agent.instance import AgentInstanceDocument
from resource.base import BaseResource
from resource.agent.instance.lcp.post import lcp_post
from resource.agent.instance.lcp.put import lcp_put
from schema.agent.instance import AgentInstanceSchema
from docstring import docstring


@docstring(method='get',
         sum='Agent Instance Read (Multiple)',
         desc="""Get the list of agent instances installed in the execution-environments
                 filtered by the query in the request body.""",
         resp="""List of agent instances installed in the execution-environment
                 filtered by the query in the request body.""")
@docstring(method='post',
         sum='Agent Instance Creation (Multiple)',
         desc='Create new agent instances in the execution-environments.',
         resp='Agent instances installed in the execution environments.')
@docstring(method='delete',
         sum='Agent Instance Deletetion (Multiple)',
         desc="""Remove the agent instances filtered by the query in the request body from the
                 execution-environments.""",
         resp='Agent instances filtered by the query in the request body uninstalled.')
@docstring(method='put',
         sum='Agent Instance Update (Multiple)',
         desc='Update the agent instances in the execution-environments.',
         resp='Agent instances updated.')
class AgentInstanceResource(BaseResource):
    doc_cls = AgentInstanceDocument
    doc_name = 'Agent Instance'
    routes = '/instance/agent/',
    schema_cls =AgentInstanceSchema
    lcp_handler = dict(post=lcp_post, put=lcp_put)
    nested_fields = ['parameters']
