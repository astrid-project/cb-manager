from http import HTTPStatus
from requests import post as post_req
from requests.auth import HTTPBasicAuth
from resource.base.lcp.retrieve import from_catalog


def action(catalog, id, exec_env, resp_lcp):
    if id:
        action = from_catalog(catalog=catalog,
                              id=id,
                              type='action',
                              label='action',
                              resp_lcp=resp_lcp)
        if action:
            resp_req = post_req(f'http://{exec_env.hostname}:{exec_env.lcp.port}/config',
                        auth=HTTPBasicAuth(exec_env.lcp.username, exec_env.lcp.password),
                        json=dict(actions=action.config.to_dict()))
            if resp_req.content:
                resp_lcp.append(resp_req.json())
            else:
                resp_lcp.append(dict(status='error', reason='Unknown'))


def parameters(catalog, data, exec_env, resp_lcp):
    for param_data in data:
        param = from_catalog(catalog=catalog,
                             id=param_data.get('id', None),
                             type='parameter',
                             label='parameter',
                             resp_lcp=resp_lcp)
        if param:
            resp_req = post_req(f'http://{exec_env.hostname}:{exec_env.lcp.port}/config',
                                auth=HTTPBasicAuth(exec_env.lcp.username, exec_env.lcp.password),
                                json=dict(parameters=dict(**param.config.to_dict(),
                                                          value=param_data['value'])))
            if resp_req.content:
                resp_lcp.append(resp_req.json())
            else:
                res_lcp.append(dict(status='error', reason='Unknown'))
