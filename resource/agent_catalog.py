from .base import BaseResource
from elasticsearch_dsl import Document, Text, Nested, InnerDoc, Boolean
from utils import docstring_parameter


class AgentCatalogRecipeActionInnerDoc(InnerDoc):
    cmd = Text(required=True)
    args = Text()


class AgentCatalogRecipeParameterInnerDoc(InnerDoc):
    destination = Text(required=True)
    name = Text(required=True)
    sep = Text(required=True)
    value = Text(required=True)


class AgentCatalogRecipeResourceInnerDoc(InnerDoc):
    destination = Text(required=True)
    content = Text(required=True)


class AgentCatalogRecipeInnerDoc(InnerDoc):
    actions = Nested(AgentCatalogRecipeActionInnerDoc)
    parameters = Nested(AgentCatalogRecipeParameterInnerDoc)
    resources = Nested(AgentCatalogRecipeResourceInnerDoc)


class AgentCatalogParameterInnerDoc(InnerDoc):
    name = Text(required=True)
    # Possible values: integer, number, time-duration, string, choice, boolean, binary
    type = Text(required=True)
    list = Boolean()
    values = Text()
    recipe = Nested(AgentCatalogRecipeInnerDoc, required=True)


class AgentCatalogActionInnerDoc(InnerDoc):
    name = Text(required=True)
    recipe = Nested(AgentCatalogRecipeInnerDoc, required=True)


class AgentCatalogDocument(Document):
    name = Text(required=True)
    parameters = Nested(AgentCatalogParameterInnerDoc, required=True)
    actions = Nested(AgentCatalogActionInnerDoc, required=True)

    class Index:
        name = 'agent-catalog'


@docstring_parameter(docstring='base', schema='AgentCatalogSchema', tag='agent-catalog',
                     get_summary='Agent Read (Multiple)',
                     get_description='Get the list of agents in the catalog filtered by the query in the request body.',
                     get_responses_200_description='List of agents in the catalog filtered by the query in the request body.',
                     post_summary='Agent Creation (Multiple)',
                     post_description='Add new agents to the catalog',
                     post_responses_200_description='Agents inserted in the catalog.',
                     delete_summary='Agent Delete (Multiple)',
                     delete_description='Delete agents filtered by the query in the request body from the catalog.',
                     delete_responses_200_description='Agents filtered by the query in the request body deleted from the catalog.',
                     put_summary='Agent Update (Multiple)',
                     put_description='Update agents in the catalog.',
                     put_responses_200_description='Agents updated in the catalog.')
class AgentCatalogResource(BaseResource):
    doc_cls = AgentCatalogDocument
    doc_name = 'Agent Catalog'
    routes = '/catalog/', '/catalog/ebpf/'


@docstring_parameter(docstring='selected', schema='AgentCatalogSchema', tag='agent-catalog',
                     get_summary='Agent Read (Single)',
                     get_description='Get the agent in the catalog with the given `id` and filtered by the query in the request body.',
                     get_responses_200_description='Agent in the catalog with the given `id` and filtered by the query in the request body.',
                     post_summary='Agent Creation (Single)',
                     post_description='Add a new agent in the catalog with the given `id`.',
                     post_responses_200_description='Agent with the given `id` inserted in the catalog.',
                     delete_summary='Agent Delete (Single)',
                     delete_description='Delete the agent with the given `id` and filtered by the query in the request body.',
                     delete_responses_200_description='Agent with the given `id` and filtered by the query in the request body deleted from the catalog.',
                     put_summary='Agent Update (Single)',
                     put_description='Update the agent in the catalog with the given `id`',
                     put_responses_200_description='Agent with the given `id` updated in the catalog.')
class AgentCatalogSelectedResource(BaseResource):
    doc_cls = AgentCatalogDocument
    doc_name = 'Agent Catalog'
    routes = '/catalog/{id}', '/catalog/ebpf/{id}'
