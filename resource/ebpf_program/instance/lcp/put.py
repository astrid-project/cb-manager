from document.ebpf_program.catalog import eBPFProgramCatalogDocument
from document.exec_env import ExecEnvDocument
from requests import put as put_req
from requests.auth import HTTPBasicAuth
from resource.base.lcp.retrieve import from_doc


def lcp_put(req, resp):
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
        resp_req = put_req(f'http://{exec_env.hostname}:{exec_env.lcp.port}/code',
                           auth=HTTPBasicAuth(exec_env.lcp.username, exec_env.lcp.password),
                           json=dict(id=ebpf_program_catalog.meta.id,
                                     interface=resp_data.get('interface', None),
                                     **ebpf_program_catalog.config.to_dict()))
        if resp_req.content:
            resp_lcp.append(resp_req.json())
        else:
            resp_lcp.append(dict(error=True,
                                 reason='Unknown'))
