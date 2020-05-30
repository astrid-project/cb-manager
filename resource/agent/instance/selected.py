from document.agent.instance import AgentInstanceDocument
from resource.base import BaseResource
from resource.agent.instance.lcp.post import lcp_post
from resource.agent.instance.lcp.put import lcp_put
from schema.agent.instance import AgentInstanceSchema
from docstring import docstring


@docstring(method='get',
         sum='Agent Instance Read (Single)',
         desc="""Get the agent instance with the given `id` installed in the execution-environments
                 filtered by the query in the request body.""",
         resp="""Agent instance with the given `id` installed in the execution-environment filtered
                 by the query in the request body.""")
@docstring(method='post',
         sum='Agent Instance Creation (Single)',
         desc='Install a new agent instance in the execution-environments with the given `id` .',
         resp='Agent instance with the given `id` in the execution environments created.')
@docstring(method='delete',
         sum='Agent Instance Deletion (Single)',
         desc="""Remove the agent instance with the given `id` and filtered by the query
                 in the request body from the execution-environments.""",
         resp='Agent instance with the given `id` and filtered by the query in the request body deleted.')
@docstring(method='put',
         sum='Agent Instance Update (Single)',
         desc='Update the agent instance in the execution-environments with the given `id` .',
         resp='Agent instance with the given `id` updated.')
class AgentInstanceSelectedResource(BaseResource):
    doc_cls = AgentInstanceDocument
    doc_name = 'Agent Instance'
    routes = '/instance/agent/{id}',
    schema_cls =AgentInstanceSchema
    lcp_handler = dict(post=lcp_post, put=lcp_put)
    nested_fields = ['parameters']
