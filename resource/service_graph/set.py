from document.exec_env import ExecEnvDocument
from reader.arg import ArgReader
from requests import put as put_req
from requests.auth import HTTPBasicAuth
from utils.log import Log


def __set(data, results):
    db = ArgReader.db
    resp_req = put_req(f'http://{db.host}:{db.port}/instance/agent',
                       auth=HTTPBasicAuth('cb-manager', 'astrid'), json=data)
    if resp_req.content:
        try:
            resp_data = resp_req.json()
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


def set_action(target, chain, src, dst, action, results):
    data = dict(id=f'firewall@{target}', actions=dict(
           id=chain, src=src, dst=dst, action=action.upper()))
    return __set(data, results)


def set_default(action, results):
    s = ExecEnvDocument.search()
    for exec_env in s.execute():
        data = dict(id=f'firewall@{exec_env.meta.id}', actions=dict(action=action.upper()))
        data['actions']['id'] = 'egress-default'
        if __set(data, results):
            data['actions']['id'] = 'ingress-default'
            __set(data, results)
    return results
