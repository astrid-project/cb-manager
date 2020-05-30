from document.agent.catalog import AgentCatalogDocument
from resource.base import BaseResource
from schema.agent.catalog import AgentCatalogSchema
from docstring import docstring


@docstring(method='get',
         sum='Agent Read (Single)',
         desc='Get the agent in the catalog with the given `id` and filtered by the query in the request body.',
         resp='Agent in the catalog with the given `id` and filtered by the query in the request body.')
@docstring(method='post',
         sum='Agent Creation (Single)',
         desc='Add a new agent in the catalog with the given `id`.',
         resp='Agent with the given `id` inserted in the catalog.')
@docstring(method='delete',
         sum='Agent Delete (Single)',
         desc='Delete the agent with the given `id` and filtered by the query in the request body.',
         resp='Agent with the given `id` and filtered by the query in the request body deleted from the catalog.')
@docstring(method='put',
         sum='Agent Update (Single)',
         desc='Update the agent in the catalog with the given `id`',
         resp='Agent with the given `id` updated in the catalog.')
class AgentCatalogSelectedResource(BaseResource):
    doc_cls = AgentCatalogDocument
    doc_name = 'Agent Catalog'
    routes = '/catalog/{id}'
    schema_cls =AgentCatalogSchema
