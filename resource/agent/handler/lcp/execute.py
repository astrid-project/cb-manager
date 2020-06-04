from http import HTTPStatus
from requests import post as post_req
from requests.auth import HTTPBasicAuth
from resource.base.handler.lcp.retrieve import from_catalog
from utils.log import Log
from utils.sequence import format as format_seq


def actions(instance, catalog, data, exec_env, resp_lcp):
    for action_data in data:
        action = from_catalog(catalog=catalog, id=action_data.get('id', None),
                              type='action', label='action', resp_lcp=resp_lcp)
        if action:
            action_config = format_seq(action.config.to_dict(), data=action_data)
            print(action_config)
            username, password = exec_env.lcp.username, exec_env.lcp.password
            resp_req = post_req(f'http://{exec_env.hostname}:{exec_env.lcp.port}/config',
                                auth=HTTPBasicAuth(username, password), json=dict(actions=action_config))
            if resp_req.content:
                try:
                    action_resp = resp_req.json()
                    action_results = action_resp.get('results', [])
                    if len(action_results) == 1:
                        action_error = action_results[0].get('error', False)
                    else:
                        action_error = True
                    if action.status is not None:
                        instance.update(
                            status=action.status if not action_error else 'unknown')
                    resp_lcp.append(action_resp)
                except Exception as exception:
                    Log.get('agent-instance-execute-action') \
                        .error(f'Exception: {exception}')
                    resp_lcp.append(dict(status='error', error=True, description='Response data not valid.',
                                         exception=str(exception), data=dict(response=resp_lcp.content),
                                         http_status_code=resp_req.status_code))
            else:
                resp_lcp.append(dict(status='error', error=True, description='Request not executed.',
                                     http_status_code=resp_req.status_code))


def parameters(instance, catalog, data, exec_env, resp_lcp):
    for param_data in data:
        param = from_catalog(catalog=catalog, id=param_data.get('id', None),
                             type='parameter', label='parameter', resp_lcp=resp_lcp)
        if param:
            param_config = dict(**param.config.to_dict(),
                                value=param_data['value'])
            username, password = exec_env.lcp.username, exec_env.lcp.password
            resp_req = post_req(f'http://{exec_env.hostname}:{exec_env.lcp.port}/config',
                                auth=HTTPBasicAuth(username, password), json=dict(parameters=param_config))
            if resp_req.content:
                try:
                    resp_lcp.append(resp_req.json())
                except Exception as exception:
                    Log.get(
                        'agent-instance-execute-parameter').error(f'Exception: {exception}')
                    resp_lcp.append(dict(status='error', error=True, description='Response data not valid.',
                                         exception=str(exception), data=dict(response=resp_lcp.content),
                                         http_status_code=resp_req.status_code))
            else:
                resp_lcp.append(dict(status='error', error=True, description='Request not executed.',
                                     http_status_code=resp_req.status_code))
