from document.agent.catalog import AgentCatalogDocument
from resource.base import BaseResource
from schema.agent.catalog import AgentCatalogSchema
from docstring import docstring


@docstring(method='get',
         sum='Agent Read (Multiple)',
         desc='Get the list of agents in the catalog filtered by the query in the request body.',
         resp='List of agents in the catalog filtered by the query in the request body.')
@docstring(method='post',
         sum='Agent Creation (Multiple)',
         desc='Add new agents to the catalog',
         resp='Agents inserted in the catalog.')
@docstring(method='delete',
         sum='Agent Delete (Multiple)',
         desc='Delete agents filtered by the query in the request body from the catalog.',
         resp='Agents filtered by the query in the request body deleted from the catalog.')
@docstring(method='put',
         sum='Agent Update (Multiple)',
         desc='Update agents in the catalog.',
         resp='Agents updated in the catalog.')
class AgentCatalogResource(BaseResource):
    doc_cls = AgentCatalogDocument
    doc_name = 'Agent Catalog'
    routes = '/catalog/agent/'
    schema_cls = AgentCatalogSchema