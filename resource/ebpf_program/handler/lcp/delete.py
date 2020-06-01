from document.ebpf_program.catalog import eBPFProgramCatalogDocument
from document.exec_env import ExecEnvDocument
from requests import delete as delete_req
from requests.auth import HTTPBasicAuth
from resource.base.handler.lcp.retrieve import from_doc
from utils.log import Log


def lcp_delete(req, resp):
    resp['lcp'] = resp_lcp = []
    resp_data = resp.get('data')

    ebpf_program_catalog = from_doc(document=eBPFProgramCatalogDocument,
                                    id=resp_data.get('ebpf_program_catalog_id', None),
                                    name='eBPF Program Catalog',
                                    resp_lcp=resp_lcp)

    exec_env = from_doc(document=ExecEnvDocument,
                        id=resp_data.get('exec_env_id', None),
                        name='Execution Environment',
                        resp_lcp=resp_lcp)

    if all([ebpf_program_catalog, exec_env]):
        resp_req = delete_req(f'http://{exec_env.hostname}:{exec_env.lcp.port}/code',
                              auth=HTTPBasicAuth(exec_env.lcp.username, exec_env.lcp.password),
                              json=dict(id=ebpf_program_catalog.meta.id))
        if resp_req.content:
            try:
                resp_lcp.append(resp_req.json())
            except Exception as exception:
                Log.get('ebpf-program-instance-lcp').error(f'Exception: {exception}')
                resp_lcp.append(dict(status='error', error=True, description='Response data not valid.',
                                     data=dict(response=resp_lcp.content),
                                     http_status_code=resp_req.status_code))
        else:
            resp_lcp.append(dict(status='error', error=True, description='Request not executed.',
                                 http_status_code=resp_req.status_code))
