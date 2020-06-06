from http import HTTPStatus
from requests import post as post_req
from requests.auth import HTTPBasicAuth
from resource.base.handler.lcp.retrieve import from_catalog
from toolz import valmap
from utils.log import Log
from utils.sequence import expand, wrap


def prepare(type, catalog, data, filter, resp_lcp):
    log = Log.get('agent-instance-execute')
    catalog_docs = []
    req_lcp = []
    label = type
    for data_item in wrap(data):
        catalog_doc = from_catalog(catalog=catalog, id=data_item.get('id', None),
                                   type=type, label=label, resp_lcp=resp_lcp)
        if catalog_doc:
            catalog_docs.append(catalog_doc)
            config = filter(catalog_doc.config.to_dict(), data_item)
            # TODO add more useful info
            log.info(f'prepare {type}: {config}')
            req_lcp.append(config)
    return catalog_docs, req_lcp


def filter_action(action, data):
    def frmt(x):
        if isinstance(x, (list, tuple)):
            return [frmt(i) for i in x]
        else:
            return x.format(**data)

    return valmap(lambda x: frmt(x), action)


def filter_parameters(parameter, data):
    return expand(parameter, value=data.get('value', None))


def execute(instance, catalog, req, exec_env, resp_lcp):
    log = Log.get('agent-instance-execute-action')
    req_lcp = {}
    actions, req_lcp['actions'] = prepare('action', catalog.actions, req.get('actions', []),
                                           filter_action, resp_lcp)
    parameters, req_lcp['parameters'] = prepare('parameter', catalog.parameters, req.get('parameters', []),
                                                filter_parameters, resp_lcp)
    if len(req_lcp['actions']) + len(req_lcp['parameters']) > 0:
        username, password = exec_env.lcp.username, exec_env.lcp.password
        resp_req = post_req(f'http://{exec_env.hostname}:{exec_env.lcp.port}/config',
                            auth=HTTPBasicAuth(username, password), json=req_lcp)
        if resp_req.content:
            try:
                resp = resp_req.json()
                results = resp.get('results', [])
                action_results = filter(lambda r: r.get('type') == 'action', results)
                update_status = None
                for action, action_result in zip(actions, action_results):
                    action_error = action_result.get('error', False)
                    if action.status is not None:
                        update_status = action.status if not action_error else 'unknown'
                if update_status is not None:
                    instance.update(status=update_status)
                resp_lcp.append(resp)
            except Exception as exception:
                log.error(f'exception: {exception}')
                resp_lcp.append(dict(status='error', error=True, description='Response data not valid.',
                                     exception=str(exception), data=dict(response=resp_lcp.content),
                                     http_status_code=resp_req.status_code))
        else:
            # TODO add more useful info
            resp_lcp.append(dict(status='error', error=True, description='Request not executed.',
                                 http_status_code=resp_req.status_code))
