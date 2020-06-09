from document.exec_env import ExecEnvDocument
from http import HTTPStatus
from reader.arg import ArgReader
from resource.base import BaseResource
from requests import put as put_req
from requests.auth import HTTPBasicAuth
from utils.log import Log


class ServiceGraphResource(BaseResource):
    routes = '/service-graph/'

    def on_post(self, req, resp):
        data = req.media
        spec = data.get('spec', {})
        policies = spec.get('policies', [])
        results = []
        for policy in policies:
            default = self.__get_default(policy, results)
            if default:
                set_default(default.replace('All', ''), results)
            else:
                exec_env_from = self.__get_exec_env(policy, 'from', results)
                exec_env_to = self.__get_exec_env(policy, 'to', results)
                action = self.__get_action(policy, results)
                if all([action, exec_env_from, exec_env_to]):
                    if self.__set_action(exec_env_from.meta.id, 'egress',
                                         exec_env_from.hostname, exec_env_to.hostname, action, results):
                        self.__set_action(exec_env_to.meta.id, 'ingress',
                                          exec_env_from.hostname, exec_env_to.hostname, action, results)
        resp.media = results

    @staticmethod
    def __get_default(policy, results):
        default = policy.get('default', None)
        if default is not None and default not in ['forwardAll']:
            results.append(dict(status='error', error=True, description='Default action unknown.',
                                data=policy, http_status_code=HTTPStatus.CONFLICT))
        return default

    @staticmethod
    def __get_exec_env(policy, direction, results):
        exec_env_id = policy.get(direction, None)
        if exec_env_id is None:
            results.append(dict(status='error', error=True, description=f'Missing [{direction}] service in the policy.',
                                data=policy, http_status_code=HTTPStatus.CONFLICT))
            return None
        exec_env = ExecEnvDocument.get(id=exec_env_id, ignore=404)
        if exec_env is None:
            results.append(dict(status='error', error=True, description=f'[{direction}] service not found.',
                                data=policy, http_status_code=HTTPStatus.CONFLICT))
        return exec_env

    @staticmethod
    def __get_action(policy, results):
        action = policy.get('action', None)
        if action is None:
            results.append(dict(status='error', error=True, description='Missing [action] in the policy.',
                                data=policy, http_status_code=HTTPStatus.CONFLICT))
        elif action not in ['forward', 'deny']:
            results.append(dict(status='error', error=True, description=f'Action policy unknown.',
                                data=policy, http_status_code=HTTPStatus.CONFLICT))
        return action

    @staticmethod
    def __set(data, results):
        db = ArgReader.db
        resp_req = put_req(f'http://{db.host}:{db.port}/instance/agent',
                        auth=HTTPBasicAuth('cb-manager', 'astrid'), json=data)
        if resp_req.content:
            try:
                resp_data = resp_req.json()  # TODO add YAML and XML support
                results.append(resp_data[0])
                return not resp_data[0].get('error', False)
            except Exception as exception:
                Log.get('service-graph.apply').error(f'Exception: {exception}')
                results.append(dict(status='error', error=True, description='Response data not valid.',
                                    exception=str(exception), data=dict(response=resp_req.content),
                                    http_status_code=resp_req.status_code))
                return False
        else:
            results.append(dict(status='error', error=True, description='Request not executed.',
                                http_status_code=resp_req.status_code))
            return False

    @staticmethod
    def __set_action(target, chain, src, dst, action, results):
        data = dict(id=f'firewall@{target}', actions=dict(
            id=chain, src=src, dst=dst, action=action.upper()))
        return __set(data, results)

    @staticmethod
    def __set_default(action, results):
        s = ExecEnvDocument.search()
        for exec_env in s.execute():
            data = dict(id=f'firewall@{exec_env.meta.id}',
                        actions=dict(action=action.upper()))
            data['actions']['id'] = 'egress-default'
            if __set(data, results):
                data['actions']['id'] = 'ingress-default'
                __set(data, results)
        return results
