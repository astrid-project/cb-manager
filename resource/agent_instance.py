from .agent_catalog import AgentCatalogDocument
from .base import BaseResource
from .exec_env import ExecEnvDocument

from args import Args
from elasticsearch_dsl import Boolean, Document, InnerDoc, Nested, Text
from http import HTTPStatus
from requests.auth import HTTPBasicAuth
from string import Template
from utils import docstring_parameter

import falcon
import json
import requests
import utils


class AgentInstanceParameterInnerDoc(InnerDoc):
    name = Text(required=True)
    value = Text(required=True)


class AgentInstanceDocument(Document):
    agent_catalog_id = Text(required=True)
    exec_env_id = Text(required=True)
    install = Boolean(required=False)
    status = Text(required=True)
    parameters = Nested(AgentInstanceParameterInnerDoc)

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
    routes = '/config/agent/',

    def resolve(self, recipe, lcp):
        t = Template(json.dumps(recipe.to_dict()))
        return json.loads(t.substitute(USERNAME=lcp.username, PASSWORD=lcp.password,
                                       HOST=Args.db.host, PORT=Args.db.port))

    def execute_action(self, name, agent_catalog, exec_env):
        action = list(filter(lambda x: x.name == name, agent_catalog.actions))
        if len(action) == 1:
            action = action[0]
            ret = requests.post(f'http://{exec_env.hostname}:4000/config',
                        auth=HTTPBasicAuth(exec_env.lcp.username, exec_env.lcp.password),
                        json=self.resolve(action.recipe, lcp=exec_env.lcp))
            return ret.json()
        return None

    def has_error(self, data):
        error = False
        for result in utils.wrap(data['results']):
            error = error or result.get('error', False)
        return error

    def operations(self, req, resp, match_status, action):
        for query, res in list(zip(utils.wrap(req.context.get('json', [])), resp.media)):
            if res.get('status', None) == match_status:
                res_data = res.get('data')
                try:
                    agent_instance = AgentInstanceDocument.get(id=res_data.get('id', None))
                except Exception as e:
                    self.log.debug(e)
                    agent_instance = None
                agent_catalog = AgentCatalogDocument.get(id=res_data.get('agent_catalog_id', None))
                exec_env = ExecEnvDocument.get(id=res_data.get('exec_env_id', None))
                res['operations'] = []
                if action is not None:
                    action_data = self.execute_action(action, agent_catalog, exec_env)
                    if action_data is not None:
                        if agent_instance is not None:
                            setattr(agent_instance, action, not self.has_error(action_data))
                        res['operations'].append(action_data)
                status = query.get('status', None)
                if status in ['start', 'stop']:
                    status_data = self.execute_action(status, agent_catalog, exec_env)
                    if status_data is not None:
                        if agent_instance is not None:
                            agent_instance.status = status if not self.has_error(status_data) else 'stop'
                        res['operations'].append(status_data)
                for param in utils.wrap(query.get('parameters', [])):
                    param_name = param.get('name', None)
                    param_catalog = list(filter(lambda x: x.name == param_name, agent_catalog.parameters))
                    if len(param_catalog) == 1:
                        param_catalog = param_catalog[0]
                        ret = requests.post(f'http://{exec_env.lcp.host}:{exec_env.lcp.port}/config',
                            auth=HTTPBasicAuth(exec_env.lcp.username, exec_env.lcp.password),
                            json=self.resolve(param_catalog.recipe))
                        res['operations'].append(ret.json())
                    else:
                        res['operations'].append({
                            'type': 'parameter',
                            'status': 'error',
                            'reason': f'Parameter {param_name} unknown.',
                            'http_status_code': HTTPStatus.NOT_FOUND
                        })
                if agent_instance is not None:
                    agent_instance.save()

    def on_post(self, req, resp, id=None):
        self.on_base_post(req, resp, id)
        self.operations(req, resp, match_status='created', action='install')

    def on_put(self, req, resp, id=None):
        self.on_base_put(req, resp, id)
        self.operations(req, resp, match_status='updated', action=None)

    def on_delete(self, req, resp, id=None):
        self.on_base_delete(req, resp, id)
        self.operations(req, resp, match_status='deleted', action='uninstall')


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
