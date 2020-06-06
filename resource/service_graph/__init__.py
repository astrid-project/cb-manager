from http import HTTPStatus
from resource.base import BaseResource
from resource.service_graph.get import get_default, get_exec_env, get_action
from resource.service_graph.set import set_default, set_action


class ServiceGraphResource(BaseResource):
    routes = '/service-graph/'

    def on_post(self, req, resp):
        data = req.context.get('json', {})
        spec = data.get('spec', {})
        policies = spec.get('policies', [])
        results = []
        for policy in policies:
            default = get_default(policy, results)
            if default:
                set_default(default.replace('All', ''), results)
            else:
                exec_env_from = get_exec_env(policy, 'from', results)
                exec_env_to = get_exec_env(policy, 'to', results)
                action = get_action(policy, results)
                if all([action, exec_env_from, exec_env_to]):
                    if set_action(exec_env_from.meta.id, 'egress',
                                  exec_env_from.hostname, exec_env_to.hostname, action, results):
                        set_action(exec_env_to.meta.id, 'ingress',
                                   exec_env_from.hostname, exec_env_to.hostname, action, results)
        resp.media = results
