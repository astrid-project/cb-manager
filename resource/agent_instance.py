from .base import BaseResource
from elasticsearch_dsl import Document, Text
from utils import docstring_parameter


class AgentInstanceDocument(Document):
    agent_catalog_id = Text()
    exec_env_id = Text()
    status = Text()

    class Index:
        name = 'agent-instance'

@docstring_parameter(docstring='base', schema='AgentInstanceSchema', tag='agent-instance',
                     get_summary='Agent Instance Read (Multiple)',
                     get_description='Get the list of agent instances installed in the execution-environments filtered by the query in the request body.',
                     get_responses_200_description='List of agent instances installed in the execution-environment filtered by the query in the request body.',
                     post_summary='Agent Instance Install (Multiple)',
                     post_description='Install new agent instances in the execution-environments.',
                     post_responses_200_description='Agent instances installed in the execution environments.',
                     delete_summary='Agent Instance Uninstall (Multiple)',
                     delete_description='Remove the agent instances filtered by the query in the request body from the execution-environments.',
                     delete_responses_200_description='Agent instances filtered by the query in the request body uninstalled.',
                     put_summary='Agent Instance Update (Multiple)',
                     put_description='Update the agent instances in the execution-environments.',
                     put_responses_200_description='Agent instances updated.')
class AgentInstanceResource(BaseResource):
    doc_cls = AgentInstanceDocument
    doc_name = 'Agent Instance'
    routes = '/config/agent',


@docstring_parameter(docstring='selected', schema='AgentInstanceSchema', tag='agent-instance',
                     get_summary='Agent Instance Read (Single)',
                     get_description='Get the agent instance with the given `id` installed in the execution-environments filtered by the query in the request body.',
                     get_responses_200_description='Agent instance with the given `id` installed in the execution-environment filtered by the query in the request body.',
                     post_summary='Agent Instance Install (Single)',
                     post_description='Install a new agent instance in the execution-environments with the given `id` .',
                     post_responses_200_description='Agent instance with the given `id`  installed in the execution environments.',
                     delete_summary='Agent Instance Uninstall (Single)',
                     delete_description='Remove the agent instance with the given `id` and filtered by the query in the request body from the execution-environments.',
                     delete_responses_200_description='Agent instance with the given `id` and filtered by the query in the request body uninstalled.',
                     put_summary='Agent Instance Update (Single)',
                     put_description='Update the agent instance in the execution-environments with the given `id` .',
                     put_responses_200_description='Agent instance with the given `id` updated.')
class AgentInstanceSelectedResource(BaseResource):
    doc_cls = AgentInstanceDocument
    doc_name = 'Agent Instance'
    routes = '/config/agent/{id}',
